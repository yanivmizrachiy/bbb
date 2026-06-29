import "dotenv/config";
import { join } from "node:path";
import { db, closeDb, migrateDb, usingServer, pgliteDir } from "./index";
import { subjects, chapters } from "./schema";
import { buildCatalog } from "./source";

async function main() {
  // Apply versioned Drizzle migrations (creates/updates the schema).
  await migrateDb();

  const root = join(process.cwd(), ".."); // bbb_work/ — the existing static project
  const { subjects: subjectRows, chapters: chapterRows } = buildCatalog(root);

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
