#!/usr/bin/env python3
"""
Fetch real images (public domain / CC) from Wikimedia Commons for huashu-design's
"content-driven designs must use real images" rule (Phase 3.5).

Why this script exists: content-driven designs (parrots/coffee/Malaysia…) must use real
photos, not CSS color blocks faking it. Having the model write image-fetching logic from
scratch every time is slow and error-prone (forgetting to clear the proxy → TLS blowups /
forgetting the compliant UA → 429s). So it is all pinned down here — next time you only
change the keywords.

Usage:
  python3 scripts/fetch_images.py --query "Petronas Towers" "Langkawi beach" "George Town street" \
      --out <project>/assets/img --count 2 --width 1600

For each query, take the first count hits, scale to width, download into out, and print
a manifest (path | license | artist | source page) for the honesty review.
If nothing can be fetched → exit code 1, prompting you to fall back to Phase 3.5's
three-tier image fallback (Unsplash/Pexels → generated images → honest placeholder).
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

# ① Clear proxies: routing curl/urllib through the local proxy causes TLS blowups (see memory feedback_gemini_proxy)
for _k in ("ALL_PROXY", "all_proxy", "HTTP_PROXY", "http_proxy", "HTTPS_PROXY", "https_proxy"):
    os.environ.pop(_k, None)

API = "https://commons.wikimedia.org/w/api.php"
# ② A compliant User-Agent is mandatory, otherwise Wikimedia returns 429
UA = "huashu-design-image-fetcher/1.0 (https://huasheng.ai; skill contact)"


def _api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def _safe(name):
    return re.sub(r"[^\w\-.]", "_", name)[:60]


def fetch(query, out, count, width):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": count,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": width,
    }
    try:
        data = _api_get(params)
    except Exception as e:
        print(f"[FAIL search] {query}: {e}", file=sys.stderr)
        return []
    pages = (data.get("query", {}) or {}).get("pages", {})
    got = []
    for p in list(pages.values())[:count]:
        ii = (p.get("imageinfo") or [{}])[0]
        thumb = ii.get("thumburl") or ii.get("url")
        if not thumb:
            continue
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "?")
        artist = re.sub("<[^>]+>", "", (meta.get("Artist", {}) or {}).get("value", "?")).strip()
        ext = os.path.splitext(thumb)[1].split("?")[0] or ".jpg"
        fn = _safe(query) + "_" + _safe(p.get("title", "img").replace("File:", ""))
        fn = os.path.splitext(fn)[0][:55] + ext
        path = os.path.join(out, fn)
        try:
            req = urllib.request.Request(thumb, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                f.write(r.read())
            got.append(path)
            print(f"[OK] {path}  | {lic} | {artist} | {ii.get('descriptionurl','')}")
        except Exception as e:
            print(f"[FAIL dl] {thumb}: {e}", file=sys.stderr)
    if not got:
        print(f"[EMPTY] Nothing fetched for '{query}' — try different keywords, or fall back to the Phase 3.5 image tiers", file=sys.stderr)
    return got


def main():
    ap = argparse.ArgumentParser(description="Fetch real images from Wikimedia Commons (huashu-design Phase 3.5)")
    ap.add_argument("--query", nargs="+", required=True, help="One or more English keywords (English gives the best hit rate)")
    ap.add_argument("--out", required=True, help="Output directory (recommended: <project>/assets/img)")
    ap.add_argument("--count", type=int, default=2, help="How many images to fetch per keyword (default 2)")
    ap.add_argument("--width", type=int, default=1600, help="Resize width in px (default 1600)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    allgot = []
    for q in a.query:
        allgot += fetch(q, a.out, a.count, a.width)
    print(f"\n=== Downloaded {len(allgot)} images to {a.out} ===")
    print("⚠️ Honesty review: would dropping any image lose information? Does its license permit this use? Delete anything unsuitable.")
    if not allgot:
        print("❌ All queries failed → fall back to Phase 3.5's three-tier image pipeline (Unsplash/Pexels → generated image → honest placeholder); don't stall over it", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
