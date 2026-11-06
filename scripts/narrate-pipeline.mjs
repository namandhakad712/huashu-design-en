#!/usr/bin/env node
/**
 * narrate-pipeline.mjs · L2 long-narration pipeline orchestrator
 *
 * Input:  a markdown narration script (## scene-id sections, [[cue:id]] marks key lines)
 * Output: voiceover.mp3 (the full concatenated voice track) + timeline.json (per-scene start/end + absolute cue times)
 *
 * Usage:
 *   node scripts/narrate-pipeline.mjs --script demo.md --out-dir _narration_demo
 *
 * Narration script format:
 *   ---
 *   title: What is LLM
 *   voice: S_JSdgdWk22   # optional; falls back to .env if omitted
 *   speed: 1.0           # optional
 *   gap: 0.3             # seconds of silence between scenes, default 0.3
 *   ---
 *
 *   ## intro
 *   Hello everyone, I'm Peanut. Today we'll make clear what an LLM is in 5 minutes.
 *
 *   ## what-is
 *   LLM stands for Large Language Model, [[cue:bigmodel]] it's a neural network
 *   with hundreds of billions of parameters. At its core, a text-continuation predictor.
 *
 * Output file layout (under out-dir):
 *   audio/
 *     intro.mp3
 *     what-is.mp3
 *   voiceover.mp3       full voice track concatenating all scenes
 *   timeline.json       schema in references/voiceover-pipeline.md
 *
 * Depends on: tts-doubao.mjs, ffmpeg, ffprobe
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..');
const TTS_SCRIPT = path.join(__dirname, 'cloud', 'tts-doubao.mjs');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--script') args.script = argv[++i];
    else if (a === '--out-dir') args.outDir = argv[++i];
    else if (a === '--no-timestamps') args.noTimestamps = true;
    else if (a === '--yes') args.yes = true;
    else if (a === '--help' || a === '-h') args.help = true;
  }
  return args;
}

function usage() {
  console.error(`
narrate-pipeline.mjs · L2 long-narration pipeline orchestrator

  --script <path>     narration script .md file (required)
  --out-dir <path>    output directory (required)
  --no-timestamps     skip character-level timestamps (requested by default; chunks carry words for karaoke subtitles)
  --yes               confirm sending the narration script text to the official Doubao TTS API (or set HUASHU_CLOUD_OK=1)

Output: <out-dir>/voiceover.mp3 + <out-dir>/timeline.json
`.trim());
  process.exit(1);
}

/**
 * Parse frontmatter + scene blocks from markdown
 * Returns { meta, scenes: [{ id, raw }] }
 */
function parseScript(md) {
  const meta = {};
  let body = md;
  const fmMatch = md.match(/^---\n([\s\S]*?)\n---\n/);
  if (fmMatch) {
    for (const line of fmMatch[1].split('\n')) {
      const idx = line.indexOf(':');
      if (idx < 0) continue;
      const key = line.slice(0, idx).trim();
      const val = line.slice(idx + 1).trim();
      meta[key] = val;
    }
    body = md.slice(fmMatch[0].length);
  }
  const scenes = [];
  const re = /^##\s+([\w-]+)\s*\n([\s\S]*?)(?=^##\s+[\w-]+\s*\n|$(?![\r\n]))/gm;
  let m;
  while ((m = re.exec(body)) !== null) {
    scenes.push({ id: m[1], raw: m[2].trim() });
  }
  return { meta, scenes };
}

/**
 * Split a scene's text by [[cue:id]] markers into chunks.
 * Returns: { chunks: [{ text, cueAfter? }] }
 *   cueAfter is the cue id that follows this chunk (chunk's end = cue position)
 *
 * Example: "A[[cue:x]]B[[cue:y]]C" =>
 *   chunks: [
 *     { text: "A", cueAfter: "x" },
 *     { text: "B", cueAfter: "y" },
 *     { text: "C" }
 *   ]
 */
function splitByCues(text) {
  const chunks = [];
  const re = /\[\[cue:([\w-]+)\]\]/g;
  let lastIdx = 0;
  let m;
  while ((m = re.exec(text)) !== null) {
    const before = text.slice(lastIdx, m.index).trim();
    chunks.push({ text: before, cueAfter: m[1] });
    lastIdx = m.index + m[0].length;
  }
  const tail = text.slice(lastIdx).trim();
  chunks.push({ text: tail });
  // Filter out empty text chunks (when a cue sits flush at a section's start/end)
  return chunks.filter((c) => c.text.length > 0 || c.cueAfter);
}

function getDuration(filePath) {
  const out = execFileSync('ffprobe', [
    '-v', 'error',
    '-show_entries', 'format=duration',
    '-of', 'default=noprint_wrappers=1:nokey=1',
    filePath,
  ], { encoding: 'utf8' });
  return parseFloat(out.trim());
}

let timestampsBroken = false; // once one timestamp request fails, all later chunks downgrade to avoid repeated retries

function callTTS(text, outPath, opts) {
  // The consent gate was already passed at this pipeline's entry (see main); the subprocess gets --yes directly
  const args = ['--text', text, '--out', outPath, '--yes'];
  if (opts.voice) args.push('--voice', opts.voice);
  if (opts.speed) args.push('--speed', String(opts.speed));
  const wantTimestamps = opts.timestamps && !timestampsBroken;
  if (wantTimestamps) args.push('--timestamps');
  try {
    const out = execFileSync('node', [TTS_SCRIPT, ...args], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'inherit'],
    });
    return JSON.parse(out.trim());
  } catch (e) {
    if (!wantTimestamps) throw e;
    // Character-level timestamps may not be supported by the current voice/resource
    // (2.0 resources + CN/EN only) — degrade and retry without timestamps
    timestampsBroken = true;
    console.error('[narrate] ⚠ TTS with --timestamps failed; downgrading to no-timestamps mode (timeline will lack words; karaoke subtitles unavailable)');
    const out = execFileSync('node', [TTS_SCRIPT, ...args.filter((a) => a !== '--timestamps')], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'inherit'],
    });
    return JSON.parse(out.trim());
  }
}

function ffmpegConcat(inputs, output) {
  // Merge same-codec mp3s with the concat demuxer
  const listFile = output + '.list';
  fs.writeFileSync(
    listFile,
    inputs.map((p) => `file '${p.replace(/'/g, "'\\''")}'`).join('\n'),
  );
  execFileSync(
    'ffmpeg',
    ['-y', '-f', 'concat', '-safe', '0', '-i', listFile, '-c', 'copy', output],
    { stdio: ['ignore', 'pipe', 'pipe'] },
  );
  fs.unlinkSync(listFile);
}

function makeSilence(duration, outPath) {
  execFileSync(
    'ffmpeg',
    ['-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', String(duration),
     '-q:a', '9', '-acodec', 'libmp3lame', outPath],
    { stdio: ['ignore', 'pipe', 'pipe'] },
  );
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.script || !args.outDir) usage();

  if (!args.yes && process.env.HUASHU_CLOUD_OK !== '1') {
    console.error(
      '[Cloud capability consent] This pipeline sends the narration script text, segment by segment, to the official Doubao TTS API (openspeech.bytedance.com, ' +
      'synthesizing the voiceover with your own key).\nIf this is OK, rerun with --yes, or set the environment variable HUASHU_CLOUD_OK=1. ' +
      'See SECURITY.md for the data-flow statement.',
    );
    process.exit(2);
  }

  const scriptPath = path.resolve(args.script);
  const outDir = path.resolve(args.outDir);
  const audioDir = path.join(outDir, 'audio');
  const tmpDir = path.join(outDir, '.tmp');
  fs.mkdirSync(audioDir, { recursive: true });
  fs.mkdirSync(tmpDir, { recursive: true });

  const md = fs.readFileSync(scriptPath, 'utf8');
  const { meta, scenes } = parseScript(md);
  if (scenes.length === 0) {
    console.error('Error: the narration script has no ## scene sections; at least one is required.');
    process.exit(1);
  }

  const voice = meta.voice || undefined;
  const speed = meta.speed ? parseFloat(meta.speed) : 1.0;
  const gap = meta.gap ? parseFloat(meta.gap) : 0.3;
  const timestamps = !args.noTimestamps && meta.timestamps !== 'false';

  console.error(`[narrate] script=${path.basename(scriptPath)} scenes=${scenes.length} voice=${voice || '(env)'} speed=${speed} gap=${gap}s`);

  // The between-scenes silence file (one shared copy)
  const gapFile = path.join(tmpDir, 'gap.mp3');
  if (gap > 0) makeSilence(gap, gapFile);

  const timeline = {
    title: meta.title || path.basename(scriptPath, '.md'),
    voice: voice || null,
    speed,
    gap,
    totalDuration: 0,
    scenes: [],
  };

  let cursor = 0;
  const sceneAudioFiles = [];

  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    console.error(`[narrate] (${i + 1}/${scenes.length}) scene="${scene.id}"`);

    const chunks = splitByCues(scene.raw);
    const chunkFiles = [];
    const cueRecords = [];
    const chunkRecords = []; // measured in-scene start/end per chunk, used for subtitle display
    let sceneInternalCursor = 0;

    for (let j = 0; j < chunks.length; j++) {
      const chunk = chunks[j];
      if (!chunk.text) {
        // Empty text chunk (cue glued to a boundary): skip TTS but still record the cue position
        if (chunk.cueAfter) {
          cueRecords.push({
            id: chunk.cueAfter,
            offset: sceneInternalCursor,
          });
        }
        continue;
      }
      const chunkPath = path.join(tmpDir, `${scene.id}-${j}.mp3`);
      const result = callTTS(chunk.text, chunkPath, { voice, speed, timestamps });
      const chunkStart = sceneInternalCursor;
      chunkFiles.push(chunkPath);
      sceneInternalCursor += result.duration;
      chunkRecords.push({
        text: chunk.text,
        start: chunkStart,
        end: sceneInternalCursor,
        duration: result.duration,
        // Character-level timestamps (TTS-measured, on TN-normalized text): converted to scene-relative times
        words: (result.words || []).map((w) => ({
          text: w.text,
          start: chunkStart + w.start,
          end: chunkStart + w.end,
        })),
      });
      console.error(`  chunk ${j}: ${result.duration.toFixed(2)}s · ${chunk.text.length} chars · ${chunk.text.slice(0, 30)}${chunk.text.length > 30 ? '…' : ''}`);
      if (chunk.cueAfter) {
        cueRecords.push({
          id: chunk.cueAfter,
          offset: sceneInternalCursor,
        });
      }
    }

    // Merge the in-scene chunks
    const sceneAudio = path.join(audioDir, `${scene.id}.mp3`);
    if (chunkFiles.length === 1) {
      fs.copyFileSync(chunkFiles[0], sceneAudio);
    } else {
      ffmpegConcat(chunkFiles, sceneAudio);
    }
    const sceneDuration = getDuration(sceneAudio);

    // Append to the master track: gap first (except before the first scene), then the scene
    if (i > 0 && gap > 0) {
      sceneAudioFiles.push(gapFile);
      cursor += gap;
    }
    sceneAudioFiles.push(sceneAudio);

    timeline.scenes.push({
      id: scene.id,
      start: cursor,
      end: cursor + sceneDuration,
      duration: sceneDuration,
      audio: path.relative(outDir, sceneAudio),
      text: scene.raw.replace(/\[\[cue:[\w-]+\]\]/g, ''),
      // chunks: drives sentence-by-sentence subtitle display. start/end are scene-relative
      // times; absoluteStart/absoluteEnd are absolute times on the full track
      // words: character-level timestamps (for karaoke subtitles; TN-normalized text, may
      // not exactly match chunk.text). Empty array = unavailable
      chunks: chunkRecords.map((c) => ({
        text: c.text,
        start: c.start,
        end: c.end,
        absoluteStart: cursor + c.start,
        absoluteEnd: cursor + c.end,
        words: (c.words || []).map((w) => ({
          text: w.text,
          start: w.start,
          end: w.end,
          absoluteStart: cursor + w.start,
          absoluteEnd: cursor + w.end,
        })),
      })),
      cues: cueRecords.map((c) => ({
        id: c.id,
        offset: c.offset,
        absoluteTime: cursor + c.offset,
      })),
    });

    cursor += sceneDuration;
  }

  // Merge the full track
  const voiceoverPath = path.join(outDir, 'voiceover.mp3');
  ffmpegConcat(sceneAudioFiles, voiceoverPath);
  timeline.totalDuration = getDuration(voiceoverPath);
  timeline.voiceover = 'voiceover.mp3';

  fs.writeFileSync(
    path.join(outDir, 'timeline.json'),
    JSON.stringify(timeline, null, 2),
  );

  // Clean up tmp
  fs.rmSync(tmpDir, { recursive: true, force: true });

  console.error(`\n[narrate] Done.`);
  console.error(`  voiceover:     ${voiceoverPath}`);
  console.error(`  timeline:      ${path.join(outDir, 'timeline.json')}`);
  console.error(`  total duration: ${timeline.totalDuration.toFixed(2)}s (${(timeline.totalDuration / 60).toFixed(2)} min)`);
  console.error(`  scenes:        ${timeline.scenes.length}`);
  const totalCues = timeline.scenes.reduce((sum, s) => sum + s.cues.length, 0);
  console.error(`  cues:          ${totalCues}`);
  const totalWords = timeline.scenes.reduce(
    (sum, s) => sum + s.chunks.reduce((a, c) => a + (c.words ? c.words.length : 0), 0), 0);
  console.error(`  char timestamps: ${totalWords > 0 ? `${totalWords} words (usable by <Subtitles karaoke />)` : 'none'}`);
}

main().catch((err) => {
  console.error(`narrate-pipeline failed: ${err.message}`);
  console.error(err.stack);
  process.exit(1);
});
