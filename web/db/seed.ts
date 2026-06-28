import "dotenv/config";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { sql } from "drizzle-orm";
import { db, closeDb, usingServer, pgliteDir } from "./index";
import { subjects, type NewSubject } from "./schema";

// Gradient-orb palette (matches the live site's home identity colors).
const ORB: Record<string, [string, string]> = {
  uncertainty: ["#f472b6", "#db2777"], // ורוד
  algebra: ["#fcd34d", "#b45309"], // זהב
  algebra8: ["#4ade80", "#15803d"], // ירוק
  geometry8: ["#38bdf8", "#0284c7"], // תכלת
};
const ORDER = ["uncertainty", "algebra", "algebra8", "geometry8"];

async function main() {
  // Idempotent schema — lets embedded PGlite run with no separate migration step
  // (a server Postgres can also use `npm run db:push`; IF NOT EXISTS is harmless).
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

  const root = join(process.cwd(), ".."); // bbb_work/ — the existing static project
  const rows: NewSubject[] = ORDER.map((key, i) => {
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

  await db.delete(subjects);
  await db.insert(subjects).values(rows);
  console.log(
    `seeded ${rows.length} subjects → ${
      usingServer ? "server Postgres" : "PGlite @ " + pgliteDir
    }`,
  );
  await closeDb();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
