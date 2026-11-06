#!/usr/bin/env node
/**
 * tts-doubao.mjs · Doubao speech TTS (Volcengine openspeech)
 *
 * ⚠️ Optional cloud capability: this script sends the text to be voiced to ByteDance's
 * official TTS endpoint (openspeech.bytedance.com), using your own key; the endpoint
 * is hard-validated against a hostname allowlist. The first call requires explicit
 * confirmation via --yes or HUASHU_CLOUD_OK=1. See the data-flow statement in SECURITY.md
 * at the repo root.
 *
 * Usage:
 *   node scripts/cloud/tts-doubao.mjs --text "Hello" --out demo.mp3 --yes
 *   node scripts/cloud/tts-doubao.mjs --text-file script.txt --out out.mp3 --speed 1.0 --yes
 *   node scripts/cloud/tts-doubao.mjs --text "Hello" --out demo.mp3 --timestamps --yes   # with character-level timestamps
 *
 * Output:
 *   - the mp3 file is written to the --out path
 *   - stdout prints one line of JSON: {"path":"...","duration":12.34,"bytes":54321}
 *   - with --timestamps it additionally contains words: [{text,start,end,confidence}]
 *     (seconds, relative to the start of this audio segment)
 *     Note: the timestamp text is post-TN text (e.g. "2025" becomes "二零二五"), with
 *     punctuation attached to the preceding character; requires a 2.0 resource
 *     (seed-tts-2.0 / seed-icl-2.0), CN/EN only.
 *
 * Dependencies: Node 18+ (built-in fetch/crypto), ffprobe (for duration; brew install ffmpeg)
 *
 * env (read automatically from the .env at the skill root; process.env takes precedence):
 *   DOUBAO_TTS_API_KEY     optional (new-style API Key auth)
 *   DOUBAO_APP_ID          optional (console App ID, paired with DOUBAO_ACCESS_KEY)
 *   DOUBAO_ACCESS_KEY      optional (console Access Token, paired with DOUBAO_APP_ID)
 *   DOUBAO_TTS_VOICE_ID    required (voice id)
 *   DOUBAO_TTS_RESOURCE_ID optional (auto-inferred from the voice by default)
 *   DOUBAO_TTS_ENDPOINT    default https://openspeech.bytedance.com/api/v3/tts/unidirectional
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..', '..');

function loadEnv() {
  const envPath = path.join(SKILL_ROOT, '.env');
  if (!fs.existsSync(envPath)) return;
  const text = fs.readFileSync(envPath, 'utf8');
  for (const line of text.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx < 0) continue;
    const key = trimmed.slice(0, idx).trim();
    let val = trimmed.slice(idx + 1).trim();
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (!(key in process.env)) process.env[key] = val;
  }
}
loadEnv();

function parseArgs(argv) {
  const args = { speed: '1.0', encoding: 'mp3' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--text') args.text = argv[++i];
    else if (a === '--text-file') args.textFile = argv[++i];
    else if (a === '--out') args.out = argv[++i];
    else if (a === '--speed') args.speed = argv[++i];
    else if (a === '--voice') args.voice = argv[++i];
    else if (a === '--encoding') args.encoding = argv[++i];
    else if (a === '--timestamps') args.timestamps = true;
    else if (a === '--yes') args.yes = true;
    else if (a === '--help' || a === '-h') args.help = true;
  }
  return args;
}

function usage() {
  console.error(`
tts-doubao.mjs · Doubao speech TTS

  --text <str>          text to synthesize
  --text-file <path>    read the text from a file (either this or --text)
  --out <path>          output mp3 path (required)
  --speed <float>       speed multiplier, default 1.0 (0.5-2.0)
  --voice <voice_id>    override the voice id from .env
  --encoding <ext>      mp3 / wav / pcm, default mp3
  --timestamps          request character-level timestamps (enable_subtitle); the result JSON gains a words array
  --yes                 confirm sending the text to the official Doubao TTS endpoint (or set HUASHU_CLOUD_OK=1)
`.trim());
  process.exit(1);
}

function getDuration(filePath) {
  try {
    const out = execFileSync('ffprobe', [
      '-v', 'error',
      '-show_entries', 'format=duration',
      '-of', 'default=noprint_wrappers=1:nokey=1',
      filePath,
    ], { encoding: 'utf8' });
    return parseFloat(out.trim());
  } catch (e) {
    return null;
  }
}

function inferResourceId(voiceId) {
  // Cloned voices default to 2.0: this account only has seed-icl-2.0 enabled
  // (1.0 returns 403 resource not granted), and character-level timestamps
  // (enable_subtitle) are only supported by 2.0 resources.
  if (voiceId.startsWith('S_')) return 'seed-icl-2.0';
  if (voiceId.includes('uranus')) return 'seed-tts-2.0';
  return 'seed-tts-1.0';
}

function speedToSpeechRate(speed) {
  const ratio = parseFloat(speed);
  if (!Number.isFinite(ratio)) return 0;
  return Math.max(-50, Math.min(100, Math.round((ratio - 1) * 100)));
}

function buildAuthHeaders({ requestId, resourceId }) {
  const apiKey = process.env.DOUBAO_TTS_API_KEY;
  const appId = process.env.DOUBAO_APP_ID;
  const accessKey = process.env.DOUBAO_ACCESS_KEY;
  const headers = {
    'Content-Type': 'application/json',
    'X-Api-Resource-Id': resourceId,
    'X-Api-Request-Id': requestId,
  };

  if (apiKey) {
    headers['X-Api-Key'] = apiKey;
    return headers;
  }

  if (!appId) throw new Error('Missing DOUBAO_TTS_API_KEY or DOUBAO_APP_ID (check .env)');
  if (!accessKey) throw new Error('Missing DOUBAO_ACCESS_KEY (check .env)');

  headers['X-Api-App-Id'] = appId;
  headers['X-Api-Access-Key'] = accessKey;
  return headers;
}

async function readV3Audio(res) {
  const text = await res.text();
  const chunks = [];
  const words = []; // character-level timestamps (with enable_subtitle on, the server returns sentence.words per sentence)
  let finalCode = null;
  let finalMessage = '';

  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    let json;
    try {
      json = JSON.parse(trimmed);
    } catch (e) {
      throw new Error(`API response line is not JSON: ${trimmed.slice(0, 200)}`);
    }

    const code = json.code ?? 0;
    if (code === 20000000) {
      finalCode = code;
      finalMessage = json.message || '';
      break;
    }
    if (code !== 0) {
      throw new Error(`API returned an error code=${code} msg=${json.message || JSON.stringify(json)}`);
    }
    if (json.data) chunks.push(Buffer.from(json.data, 'base64'));
    if (json.sentence && Array.isArray(json.sentence.words)) {
      for (const w of json.sentence.words) {
        words.push({
          text: w.word,
          start: w.startTime,
          end: w.endTime,
          confidence: w.confidence,
        });
      }
    }
  }

  if (!chunks.length) {
    const detail = finalCode ? `final code ${finalCode} ${finalMessage}` : text.slice(0, 500);
    throw new Error(`API response contained no audio data: ${detail}`);
  }
  return { audio: Buffer.concat(chunks), words };
}

// Endpoint hostname allowlist: the key and the text may only go to official ByteDance
// domains, so a tampered .env cannot redirect them elsewhere
const ALLOWED_ENDPOINT_HOSTS = /(^|\.)(bytedance\.com|volces\.com)$/;

async function tts({ text, voice, speed, encoding, timestamps }) {
  const endpoint = process.env.DOUBAO_TTS_ENDPOINT || 'https://openspeech.bytedance.com/api/v3/tts/unidirectional';
  const host = new URL(endpoint).hostname;
  if (!ALLOWED_ENDPOINT_HOSTS.test(host)) {
    throw new Error(`DOUBAO_TTS_ENDPOINT host ${host} is not on the allowlist (*.bytedance.com / *.volces.com); refusing to send`);
  }
  const voiceId = voice || process.env.DOUBAO_TTS_VOICE_ID || process.env.DOUBAO_SPEAKER;
  const resourceId = process.env.DOUBAO_TTS_RESOURCE_ID || inferResourceId(voiceId || '');
  const requestId = randomUUID();

  if (!voiceId) throw new Error('Missing DOUBAO_TTS_VOICE_ID (check .env, or pass it via --voice)');

  const body = {
    user: { uid: 'huashu-design' },
    req_params: {
      text,
      speaker: voiceId,
      audio_params: {
        format: encoding,
        sample_rate: 24000,
        speech_rate: speedToSpeechRate(speed),
        // Character-level timestamps: only supported by 2.0 resources (seed-tts-2.0 / seed-icl-2.0), CN/EN only
        ...(timestamps ? { enable_subtitle: true } : {}),
      },
    },
  };

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: buildAuthHeaders({ requestId, resourceId }),
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`HTTP ${res.status}: ${errText.slice(0, 500)}`);
  }

  return readV3Audio(res);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) usage();

  let text = args.text;
  if (!text && args.textFile) {
    text = fs.readFileSync(args.textFile, 'utf8').trim();
  }
  if (!text) {
    console.error('Error: missing --text or --text-file');
    usage();
  }
  if (!args.out) {
    console.error('Error: missing --out');
    usage();
  }

  if (!args.yes && process.env.HUASHU_CLOUD_OK !== '1') {
    const host = new URL(process.env.DOUBAO_TTS_ENDPOINT || 'https://openspeech.bytedance.com').hostname;
    console.error(
      `[Cloud capability consent] This run will send ~${text.length} characters of text to ${host} (the official Doubao TTS endpoint, using your own key to synthesize speech).\n` +
      `Re-run with --yes to confirm, or set the environment variable HUASHU_CLOUD_OK=1. See the data-flow statement in SECURITY.md.`,
    );
    process.exit(2);
  }

  const outPath = path.resolve(args.out);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  const { audio, words } = await tts({
    text,
    voice: args.voice,
    speed: args.speed,
    encoding: args.encoding,
    timestamps: args.timestamps,
  });

  fs.writeFileSync(outPath, audio);
  const duration = getDuration(outPath);
  const result = {
    path: outPath,
    bytes: audio.length,
    duration,
    text_chars: text.length,
  };
  if (args.timestamps) result.words = words;
  console.log(JSON.stringify(result));
}

main().catch((err) => {
  console.error(`TTS failed: ${err.message}`);
  process.exit(1);
});
