import "dotenv/config";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { db, closeDb, migrateDb, usingServer, pgliteDir } from "./index";
import {
  subjects,
  chapters,
  type NewSubject,
  type NewChapter,
} from "./schema";
import { parseChapterStrip } from "./parse";

// Gradient-orb palette (matches the live site's home identity colors).
const ORB: Record<string, [string, string]> = {
  uncertainty: ["#f472b6", "#db2777"], // ורוד
  algebra: ["#fcd34d", "#b45309"], // זהב
  algebra8: ["#4ade80", "#15803d"], // ירוק
  geometry8: ["#38bdf8", "#0284c7"], // תכלת
};
const ORDER = ["uncertainty", "algebra", "algebra8", "geometry8"];

// Read chapters straight from each subject's existing viewer.html chapter strip
// (read-only — never touches worksheet content).
function readChapters(key: string, root: string): NewChapter[] {
  const html = readFileSync(join(root, key, "viewer.html"), "utf8");
  return parseChapterStrip(html, key);
}

async function main() {
  // Apply versioned Drizzle migrations (creates/updates the schema).
  await migrateDb();

  const root = join(process.cwd(), ".."); // bbb_work/ — the existing static project

  const subjectRows: NewSubject[] = ORDER.map((key, i) => {
    const m = JSON.parse(readFileSync(join(root, key, "meta.json"), "utf8"));
    const [orbLight, orbDeep] = ORB[key];
    return {
      key,
      title: m.title,
      subtitle: m.subtitle,
      icon: m.icon,
      color: m.color,
      orbLight,
      orbDeep,
      questions: m.questions,
      chapters: m.chapters,
      pages: m.pages,
      pdf: m.pdf,
      sort: i,
    };
  });

  const chapterRows: NewChapter[] = ORDER.flatMap((key) =>
    readChapters(key, root),
  );

  await db.delete(chapters);
  await db.delete(subjects);
  await db.insert(subjects).values(subjectRows);
  await db.insert(chapters).values(chapterRows);

  console.log(
    `seeded ${subjectRows.length} subjects + ${chapterRows.length} chapters → ${
      usingServer ? "server Postgres" : "PGlite @ " + pgliteDir
    }`,
  );
  await closeDb();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
