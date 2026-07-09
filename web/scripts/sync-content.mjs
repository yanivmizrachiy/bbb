// Make the Next app self-contained: copy each subject's generated worksheet
// artifacts (A4 page images + the PDF) from the Python build output into
// web/public/worksheets/<key>/, so the app serves them itself — no dependency
// on the old static GitHub Pages site. Runs before dev/build (and on Vercel).
import {
  readFileSync,
  mkdirSync,
  copyFileSync,
  readdirSync,
  rmSync,
  existsSync,
} from "node:fs";
import { join } from "node:path";

const ROOT = join(process.cwd(), ".."); // bbb_work/ (the repo root; Python output lives here)
const OUT = join(process.cwd(), "public", "worksheets");
const SUBJECTS = ["uncertainty", "algebra", "algebra8", "geometry8"];

rmSync(OUT, { recursive: true, force: true });

let pages = 0;
for (const key of SUBJECTS) {
  const metaPath = join(ROOT, key, "meta.json");
  if (!existsSync(metaPath)) {
    console.warn(`sync-content: skipping ${key} (no meta.json)`);
    continue;
  }
  const meta = JSON.parse(readFileSync(metaPath, "utf8"));

  const srcPages = join(ROOT, key, "assets", "pages");
  if (!existsSync(srcPages)) {
    console.warn(`sync-content: skipping ${key} (no assets/pages — run the Python build)`);
    continue;
  }
  const dstPages = join(OUT, key, "pages");
  mkdirSync(dstPages, { recursive: true });
  for (const f of readdirSync(srcPages)) {
    if (f.endsWith(".png")) {
      copyFileSync(join(srcPages, f), join(dstPages, f));
      pages++;
    }
  }

  const pdf = join(ROOT, key, meta.pdf);
  if (existsSync(pdf)) copyFileSync(pdf, join(OUT, key, meta.pdf));
}

console.log(
  `sync-content: ${SUBJECTS.length} subjects, ${pages} page images → public/worksheets`,
);
