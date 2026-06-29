import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { buildCatalog } from "../db/source";
import type { Subject, Chapter } from "../db/schema";

// Generate a static catalog snapshot (subjects + chapters) from the source
// files, bundled into the app. Used as the data source when no Postgres server
// is configured — so the deployed site works with zero database setup, while
// still using Postgres when DATABASE_URL/POSTGRES_URL is present.
const root = join(process.cwd(), "..");
const { subjects, chapters } = buildCatalog(root);

const subjectsOut: Subject[] = subjects.map((s, i) => ({
  id: i + 1,
  sort: s.sort ?? i,
  ...s,
})) as Subject[];

let cid = 0;
const chaptersOut: Chapter[] = chapters.map((c) => ({
  id: ++cid,
  ...c,
  hotLeft: c.hotLeft ?? null,
  hotTop: c.hotTop ?? null,
  hotWidth: c.hotWidth ?? null,
  hotHeight: c.hotHeight ?? null,
})) as Chapter[];

const out = join(process.cwd(), "app", "_data", "catalog.json");
mkdirSync(dirname(out), { recursive: true });
writeFileSync(
  out,
  JSON.stringify({ subjects: subjectsOut, chapters: chaptersOut }, null, 2) + "\n",
);
console.log(
  `catalog snapshot → app/_data/catalog.json (${subjectsOut.length} subjects, ${chaptersOut.length} chapters)`,
);
