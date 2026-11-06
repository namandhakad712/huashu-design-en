#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
AI video review loop — feed the rendered animation MP4 to a video understanding
model (seed-2.0-lite): each segment is submitted against a fixed checklist, plus
one low-res pass over the whole film, and everything is merged into a structured
markdown review report.

⚠️ Optional cloud capability: compressed segments of the finished video are sent
to the official Volcengine Ark endpoint (ark.cn-beijing.volces.com) for
video-understanding review, using your own ARK_API_KEY. The first call requires
explicit confirmation via --yes or HUASHU_CLOUD_OK=1. For the data-flow statement
see SECURITY.md at the repo root. Free local alternative:
scripts/verify-video.sh extracts frames for manual viewing.

Usage:
    uv run ai-review-video.py --video final.mp4 --yes
    uv run ai-review-video.py --video final.mp4 --context 导演稿.md --yes
    uv run ai-review-video.py --video final.mp4 --segment-len 60 --output report.md --yes

Call pipeline:
    1. ffprobe probes duration / audio track
    2. If an audio track exists → ffmpeg silencedetect extracts an SFX onset
       timeline (the model cannot hear the video's audio track; verified
       2026-07-17: input_video carries picture only. A/V alignment check =
       local onsets + the model cross-checking the picture)
    3. Split into --segment-len segments and compress (1280 wide / 15fps /
       crf28, ~0.5MB/minute for flat animation)
    4. Submit each segment for review (checklist ①-⑧); each segment's prompt
       is annotated with its original-video time range
    5. Compress one more low-res version of the whole film (960 wide / 10fps)
       and submit it on its own, specifically to check cross-segment narrative
       coherence / hero continuity
    6. A text synthesis call merges the findings item by item along the
       checklist into the final report; raw per-segment findings are kept in
       the appendix

API key: read from the ARK_API_KEY environment variable first, then from the
.env at the skill root (only that single variable is extracted); never hardcoded.
Proxy: the requests session disables trust_env (does not inherit local proxy
settings), immune to TLS errors caused by leftover ALL_PROXY-style proxies.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from base64 import b64encode
from pathlib import Path

import requests

API_URL = "https://ark.cn-beijing.volces.com/api/v3/responses"
DEFAULT_MODEL = "doubao-seed-2-0-lite-260215"
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"  # .env at the skill root (gitignored)
MAX_SEGMENT_MB = 8  # if a compressed segment exceeds this, compress one notch harder

# NOTE: CHECKLIST / SEVERITY_RULE, the *_prompt() string builders below, and the
# Chinese fallback placeholder handed to synthesis_prompt() are the request payload
# sent to the video-understanding model — kept in Chinese, byte-identical to the
# parent skill's production prompts. Do not translate without re-validating.
CHECKLIST = """\
① 黑帧/空窗/渲染残缺：整帧或大面积黑屏、白屏、元素未渲染出来、明显破图
② 文字问题：字卡/标签被裁切、溢出容器、错字、乱码、字叠字
③ 元素重叠遮挡：不该重叠的元素互相遮挡、层级错误、穿模
④ 叙事连贯性：场景过渡分三类——硬切（前后帧整页突变，无任何衔接）、
   交叉淡入淡出（旧场景透明度渐隐）、morph（元素连续变形/位移到新场景）。
   报告时必须写明你看到的是哪一类，不要把淡入淡出误报成硬切；
   硬切=⚡，淡入淡出在导演稿要求morph时=💡「过渡偷懒」
⑤ hero/主体贯穿性：如果有贯穿全片的主体元素，它是否在场景切换中断裂、消失、突变位置
⑥ 节奏死段：见下方「静止段客观检测表」（ffmpeg逐帧检测，≥3秒完全静止的区间）。
   你的任务不是找死段，而是对表中每个区间判断：是刻意hold（字卡阅读/弹幕停留/收尾定格）
   还是真死段（画面无信息可读还停着）。刻意hold=不报或💡，真死段=⚡
⑦ 音效打点（见下方onset时间表）：核对每个音效时间点画面是否有对应事件
⑧ 构图：明显失衡、大片无意义空白、重要元素贴边或被挤到角落"""

SEVERITY_RULE = """\
严重度分三级：
- ⚠️致命：交付前必须修（黑帧、错字、文字被裁、元素叠死、明显破图）
- ⚡重要：观感明显受损（硬切感、hero断裂、超3秒死段、构图明显失衡）
- 💡建议：锦上添花的改进点"""


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def load_api_key():
    key = os.getenv("ARK_API_KEY")
    if not key and ENV_PATH.exists():
        # Extract only the ARK_API_KEY variable; never load the whole .env into the environment
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ARK_API_KEY") and "=" in line:
                key = line.split("=", 1)[1].strip().strip("'\"")
                break
    if not key or key.startswith("your_"):
        sys.exit("Error: ARK_API_KEY is not configured (skill-root .env or environment variable); refusing to continue. Review results are never fabricated.")
    return key


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r


def probe(video: Path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-show_entries", "stream=codec_type", "-of", "json", str(video)])
    info = json.loads(r.stdout)
    duration = float(info["format"]["duration"])
    has_audio = any(s.get("codec_type") == "audio" for s in info.get("streams", []))
    return duration, has_audio


def detect_audio_onsets(video: Path, noise_db=-45, min_silence=0.3):
    """Derive SFX onsets from silencedetect output. Returns a list of original-video seconds."""
    r = subprocess.run(
        ["ffmpeg", "-i", str(video), "-af",
         f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-"],
        capture_output=True, text=True)
    onsets = [round(float(m), 1) for m in
              re.findall(r"silence_end:\s*([\d.]+)", r.stderr)]
    # If the head is non-silent (sound right at the start), prepend 0
    starts = re.findall(r"silence_start:\s*([\d.-]+)", r.stderr)
    if starts and float(starts[0]) > min_silence:
        onsets.insert(0, 0.0)
    return onsets


def detect_static_segments(video: Path, noise=0.001, min_dur=3.0):
    """freezedetect finds fully static intervals of at least min_dur seconds. Returns [(start, end)] in original-video seconds."""
    r = subprocess.run(
        ["ffmpeg", "-i", str(video), "-vf",
         f"freezedetect=n={noise}:d={min_dur}", "-f", "null", "-"],
        capture_output=True, text=True)
    starts = re.findall(r"freeze_start:\s*([\d.]+)", r.stderr)
    durs = re.findall(r"freeze_duration:\s*([\d.]+)", r.stderr)
    return [(round(float(s), 1), round(float(s) + float(d), 1))
            for s, d in zip(starts, durs)]


def compress(src: Path, dst: Path, ss=None, t=None, width=1280, fps=15, crf=28):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if ss is not None:
        cmd += ["-ss", str(ss)]
    if t is not None:
        cmd += ["-t", str(t)]
    cmd += ["-i", str(src), "-vf", f"scale={width}:-2,fps={fps}",
            "-c:v", "libx264", "-crf", str(crf), "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-an", str(dst)]
    run(cmd)


def fmt_ts(sec: float) -> str:
    return f"{int(sec) // 60}:{int(sec) % 60:02d}"


def ask_model(session, api_key, model, prompt, video_path: Path | None = None, retries=1):
    content = []
    if video_path is not None:
        b64 = b64encode(video_path.read_bytes()).decode()
        content.append({"type": "input_video", "video_url": f"data:video/mp4;base64,{b64}"})
    content.append({"type": "input_text", "text": prompt})
    payload = {"model": model, "input": [{"role": "user", "content": content}]}
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = session.post(
                API_URL, json=payload, timeout=600,
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"})
            if resp.status_code != 200:
                last_err = f"API {resp.status_code}: {resp.text[:500]}"
                continue
            data = resp.json()
            usage = data.get("usage", {})
            text = ""
            out = data.get("output")
            if isinstance(out, list):
                for item in out:
                    if isinstance(item, dict) and item.get("type") == "message":
                        for c in item.get("content", []):
                            if isinstance(c, dict) and c.get("type") == "output_text":
                                text += c.get("text", "")
            elif isinstance(out, str):
                text = out
            if not text:
                choices = data.get("choices", [])
                if choices:
                    text = choices[0].get("message", {}).get("content", "")
            if text:
                return text, usage
            last_err = f"Response contained no text: {json.dumps(data, ensure_ascii=False)[:500]}"
        except requests.RequestException as e:
            last_err = f"Network error: {e}"
        if attempt < retries:
            log(f"  Retrying ({last_err[:120]})...")
            time.sleep(3)
    raise RuntimeError(last_err)


def segment_prompt(seg_start, seg_end, duration, context_text, onsets_in_seg,
                   statics_in_seg):
    p = [f"你是动画成片质检员，任务是严格挑毛病，不夸片子。",
         f"这段视频是一部总长{fmt_ts(duration)}的动画成片的一个片段，"
         f"对应原片 {fmt_ts(seg_start)}–{fmt_ts(seg_end)}。"
         f"片段内第t秒 = 原片第{fmt_ts(seg_start)}+t秒，报告里一律用原片时间（分:秒）。"]
    if context_text:
        p.append("以下是全片导演稿（评审上下文，用来判断叙事意图和该出现什么）：\n"
                 "<导演稿>\n" + context_text + "\n</导演稿>")
    p.append("逐项检查以下checklist，只报本片段内的发现：\n" + CHECKLIST)
    if statics_in_seg:
        ts = "、".join(f"{fmt_ts(a)}–{fmt_ts(b)}（{b - a:.1f}s）" for a, b in statics_in_seg)
        p.append(f"⑥的静止段客观检测表（本段内，原片时间）：{ts}。逐个判断刻意hold还是真死段。")
    else:
        p.append("本片段内无≥3秒静止段，⑥直接写「未发现」。")
    if onsets_in_seg:
        ts = "、".join(f"{fmt_ts(t)}({t}s)" for t in onsets_in_seg)
        p.append(f"⑦的onset时间表（本段内音效实际出现的原片时间）：{ts}。"
                 f"你听不到声音，只需核对这些时间点画面上是否有值得配音效的事件"
                 f"（转场/字卡落定/撞击/元素出现），没有对应事件的时间点=音效打空，要报。")
    else:
        p.append("本片段内没有检测到音效onset，⑦跳过；但如果本段有强烈画面事件"
                 "（撞击/字卡/转场）却无音效覆盖，可在⑦下用💡提出。")
    p.append(SEVERITY_RULE)
    p.append("输出格式：markdown。按①-⑧逐项，每项下用列表：\n"
             "- [原片分:秒] 严重度emoji 具体描述\n"
             "该项无问题就写「未发现」。只报你真正看到的，不确定的标「存疑」，不编造。")
    return "\n\n".join(p)


def global_prompt(duration, context_text):
    p = ["你是动画成片质检员。这是一部动画成片的全片低清版（评审用压缩，画质低是正常的，"
         "不要报画质/清晰度问题），总长" + fmt_ts(duration) + "。"]
    if context_text:
        p.append("导演稿：\n<导演稿>\n" + context_text + "\n</导演稿>")
    p.append("只做三件事（细节问题已有分段评审负责，你不用管）：\n"
             "A. 叙事连贯性：从头到尾看，哪些时间点是PowerPoint式硬切（整页突变无过渡）？\n"
             "B. hero/主体贯穿性：贯穿全片的主体元素在哪些切换处断裂、消失或突变？\n"
             "C. 整体节奏：哪些区间拖（长时间无新信息）、哪些区间赶？\n\n"
             + SEVERITY_RULE +
             "\n\n输出markdown，A/B/C三节，发现带[分:秒]时间点。无问题写「未发现」。不编造。")
    return "\n\n".join(p)


def synthesis_prompt(duration, seg_reports, global_report):
    parts = ["你是评审报告主编。下面是同一部" + fmt_ts(duration) +
             "动画成片的分段评审 + 全片评审原始记录，把它们合并成一份最终报告正文。",
             "要求：\n"
             "1. 按checklist①-⑧逐项组织，每项下按时间顺序列发现：- [分:秒] 严重度 描述\n"
             "2. 同一问题被多段重复报的合并成一条；分段与全片评审矛盾时两说并存标「存疑」\n"
             "3. 保留每条发现的时间点和严重度emoji（⚠️/⚡/💡），不新增原始记录里没有的发现\n"
             "4. 开头给一个「问题总数：⚠️x ⚡y 💡z」的统计行和三句话以内的总评\n"
             "5. 只输出报告正文markdown，不要客套话",
             "<全片评审>\n" + global_report + "\n</全片评审>"]
    for (s, e, text) in seg_reports:
        parts.append(f"<分段评审 原片{fmt_ts(s)}–{fmt_ts(e)}>\n{text}\n</分段评审>")
    return "\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="AI video review: animation MP4 → structured checklist review report")
    ap.add_argument("--video", required=True, help="path to the finished video (mp4)")
    ap.add_argument("--context", help="path to the director's notes (导演稿.md) / scene-breakdown md (optional, used as review context)")
    ap.add_argument("--segment-len", type=int, default=60, help="segment length in seconds (default 60)")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"model (default {DEFAULT_MODEL})")
    ap.add_argument("--output", "-o", help="report path (default: <video-name>-AI-review.md next to the video)")
    ap.add_argument("--yes", action="store_true",
                    help="confirm sending compressed video segments to the official Volcengine Ark endpoint (or set HUASHU_CLOUD_OK=1)")
    args = ap.parse_args()

    video = Path(args.video).resolve()
    if not video.exists():
        sys.exit(f"Error: video does not exist: {video}")

    if not args.yes and os.getenv("HUASHU_CLOUD_OK") != "1":
        sys.exit(
            f"[Cloud capability consent] This run will send {video.name}, compressed and split into segments, to ark.cn-beijing.volces.com"
            " (the official Volcengine Ark endpoint, using your own ARK_API_KEY for video-understanding review).\n"
            "Re-run with --yes to confirm, or set the environment variable HUASHU_CLOUD_OK=1."
            " See the data-flow statement in SECURITY.md; free local alternative: scripts/verify-video.sh.")
    out_path = Path(args.output) if args.output else video.parent / f"{video.stem}-AI-review.md"

    context_text = ""
    if args.context:
        ctx = Path(args.context)
        if not ctx.exists():
            sys.exit(f"Error: context file does not exist: {ctx}")
        context_text = ctx.read_text(encoding="utf-8")[:12000]

    api_key = load_api_key()
    session = requests.Session()
    session.trust_env = False  # immune to ALL_PROXY-style proxy pitfalls

    duration, has_audio = probe(video)
    log(f"Video {fmt_ts(duration)}, audio track={'yes' if has_audio else 'no'}")

    onsets = detect_audio_onsets(video) if has_audio else []
    if has_audio:
        log(f"SFX onset detection: {len(onsets)} → {['%.1f' % t for t in onsets]}")

    # Objective static-segment detection (adjacent intervals merged)
    raw_statics = detect_static_segments(video)
    statics = []
    for a, b in raw_statics:
        if statics and a - statics[-1][1] < 0.2:
            statics[-1] = (statics[-1][0], b)
        else:
            statics.append((a, b))
    log(f"Static-segment detection (≥3s): {len(statics)} → "
        f"{[f'{a:.0f}-{b:.0f}s' for a, b in statics]}")

    total_usage = {"input_tokens": 0, "output_tokens": 0}

    def add_usage(u):
        for k in total_usage:
            total_usage[k] += u.get(k, 0) or 0

    seg_reports, failures = [], []
    with tempfile.TemporaryDirectory(prefix="ai-review-") as tmp:
        tmp = Path(tmp)
        # Segmenting
        bounds = []
        t0 = 0.0
        while t0 < duration - 1:
            bounds.append((t0, min(t0 + args.segment_len, duration)))
            t0 += args.segment_len
        log(f"Segments: {len(bounds)} × ≤{args.segment_len}s")

        for i, (s, e) in enumerate(bounds, 1):
            seg = tmp / f"seg{i}.mp4"
            compress(video, seg, ss=s, t=e - s)
            if seg.stat().st_size > MAX_SEGMENT_MB * 1024 * 1024:
                compress(video, seg, ss=s, t=e - s, width=960, fps=10, crf=32)
            mb = seg.stat().st_size / 1048576
            onsets_in = [t for t in onsets if s <= t < e]
            statics_in = [(a, b) for a, b in statics if a < e and b > s]
            log(f"Segment {i} {fmt_ts(s)}–{fmt_ts(e)} ({mb:.1f}MB, onsets×{len(onsets_in)}, "
                f"static segments×{len(statics_in)}) submitted for review...")
            try:
                text, usage = ask_model(session, api_key, args.model,
                                        segment_prompt(s, e, duration, context_text,
                                                       onsets_in, statics_in),
                                        seg)
                add_usage(usage)
                seg_reports.append((s, e, text))
            except RuntimeError as err:
                log(f"  Segment {i} submission failed: {err}")
                failures.append((s, e, str(err)))

        # Low-res full-video pass
        log("Submitting the low-res full video (narrative / hero / pacing)...")
        full = tmp / "full.mp4"
        compress(video, full, width=960, fps=10, crf=30)
        global_report, global_fail = "", None
        try:
            global_report, usage = ask_model(session, api_key, args.model,
                                             global_prompt(duration, context_text), full)
            add_usage(usage)
        except RuntimeError as err:
            global_fail = str(err)
            log(f"  Full-video pass failed: {err}")

    if not seg_reports and not global_report:
        sys.exit("Error: all review submissions failed; no report can be produced. Review results are never fabricated.\n" +
                 "\n".join(f"{fmt_ts(s)}–{fmt_ts(e)}: {m}" for s, e, m in failures))

    # Synthesis
    log("Synthesizing the final report...")
    try:
        body, usage = ask_model(session, api_key, args.model,
                                synthesis_prompt(duration, seg_reports,
                                                 global_report or "（全片pass调用失败，无记录）"))
        add_usage(usage)
    except RuntimeError as err:
        log(f"Synthesis call failed ({err}); falling back to raw-record concatenation")
        body = "> Synthesis call failed; below are the raw records of each pass concatenated directly.\n\n" + \
               (global_report or "") + "\n\n" + \
               "\n\n".join(f"## Segment {fmt_ts(s)}–{fmt_ts(e)}\n{t}" for s, e, t in seg_reports)

    lines = [f"# {video.name} · AI Review Report",
             "",
             f"> Model: {args.model} | Reviewed at: {time.strftime('%Y-%m-%d %H:%M')} | "
             f"Video length: {fmt_ts(duration)} | Segments: {len(seg_reports)} ok / {len(failures)} failed | "
             f"SFX onsets: {len(onsets)} / static segments ≥3s: {len(statics)}"
             f" (all from local objective ffmpeg detection; the model hears no audio — A/V alignment = onsets + picture cross-check) | "
             f"tokens: in {total_usage['input_tokens']} / out {total_usage['output_tokens']}",
             ""]
    if failures:
        lines.append("> ⚠️ The following time ranges failed submission and were not covered by the review: " +
                     "; ".join(f"{fmt_ts(s)}–{fmt_ts(e)} ({m[:100]})" for s, e, m in failures))
        lines.append("")
    if global_fail:
        lines.append(f"> ⚠️ Full-video continuity pass call failed: {global_fail[:200]}")
        lines.append("")
    lines.append(body)
    lines.append("\n\n---\n\n## Appendix · Objective detection data (ffmpeg, not model judgment)\n")
    lines.append("Static segments ≥3s: " + ("; ".join(
        f"{fmt_ts(a)}–{fmt_ts(b)} ({b - a:.1f}s)" for a, b in statics) or "none"))
    lines.append("\nSFX onsets: " + ("; ".join(fmt_ts(t) for t in onsets) or "none / no audio track"))
    lines.append("\n## Appendix · Raw per-segment review records\n")
    if global_report:
        lines.append("### Full-video pass (narrative / hero / pacing)\n\n" + global_report + "\n")
    for s, e, t in seg_reports:
        lines.append(f"### Segment, original video {fmt_ts(s)}–{fmt_ts(e)}\n\n{t}\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"Report written to: {out_path}")
    print(out_path)


if __name__ == "__main__":
    main()
