// News-image entry for 18 November 2026 (Node 22, standard library only).
// The image is the entry.png beside this file: a 1024x1024 infographic I drew
// with a small Python/PIL script (draw.py, kept in this repo) summing up the
// day's world news — Gulf strikes, the Kerch Bridge, the Shenzhen summit and
// the Alaska Senate result. This program copies it to /output/entry.png and
// checks the PNG magic bytes and the 1 MiB size cap before it finishes, so a
// broken file fails loudly instead of reaching the gate.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dst = join(outDir, 'entry.png');

copyFileSync(src, dst);

const bytes = readFileSync(dst);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG file');
}
if (statSync(dst).size > 1048576) {
  throw new Error('entry.png is over the 1 MiB cap');
}
// IHDR chunk: width and height are the first two big-endian uint32s after
// the 8-byte signature and the 8-byte chunk header.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}
