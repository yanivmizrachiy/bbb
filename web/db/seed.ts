import "dotenv/config";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { sql } from "drizzle-orm";
import { db, closeDb, usingServer, pgliteDir } from "./index";
import {
  subjects,
  chapters,
  type NewSubject,
  type NewChapter,
} from "./schema";

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
const CHIP =
  /<a class="tc" href="#p(\d+)" style="--cc:([^"]+)"><i>([^<]+)<\/i>([^<]+)<\/a>/g;

function readChapters(key: string, root: string): NewChapter[] {
  const html = readFileSync(join(root, key, "viewer.html"), "utf8");
  const out: NewChapter[] = [];
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = CHIP.exec(html))) {
    out.push({
      subjectKey: key,
      idx: i++,
      page: Number(m[1]),
      color: m[2],
      letter: m[3],
      title: m[4],
    });
  }
  return out;
}

async function main() {
  // Idempotent schema (lets embedded PGlite run with no separate migration step).
  await db.execute(sql`
    CREATE TABLE IF NOT EXISTS subjects (
      id serial PRIMARY KEY,
      key text NOT NULL UNIQUE,
      title text NOT NULL,
      subtitle text NOT NULL,
      icon text NOT NULL,
      color text NOT NULL,
      orb_light text NOT NULL,
      orb_deep text NOT NULL,
      questions integer NOT NULL,
      chapters integer NOT NULL,
      pages integer NOT NULL,
      pdf text NOT NULL,
      sort integer NOT NULL DEFAULT 0
    );
  `);
  await db.execute(sql`
    CREATE TABLE IF NOT EXISTS chapters (
      id serial PRIMARY KEY,
      subject_key text NOT NULL,
      idx integer NOT NULL,
      letter text NOT NULL,
      title text NOT NULL,
      color text NOT NULL,
      page integer NOT NULL
    );
  `);

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
