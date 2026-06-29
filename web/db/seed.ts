import "dotenv/config";
import { join } from "node:path";
import { db, closeDb, migrateDb, usingServer } from "./index";
import { subjects, chapters } from "./schema";
import { buildCatalog } from "./source";

async function main() {
  // No real Postgres server → the site serves the committed snapshot (db/data.ts),
  // so there is nothing to seed. Keeps `vercel-build` a clean no-op until a DB is attached.
  if (!usingServer) {
    console.log(
      "No Postgres server configured — the site uses the committed snapshot; nothing to seed.",
    );
    return;
  }

  // Apply versioned Drizzle migrations (creates/updates the schema).
  await migrateDb();

  const root = join(process.cwd(), ".."); // bbb_work/ — the existing static project
  const { subjects: subjectRows, chapters: chapterRows } = buildCatalog(root);

  await db.delete(chapters);
  await db.delete(subjects);
  await db.insert(subjects).values(subjectRows);
  await db.insert(chapters).values(chapterRows);

  console.log(
    `seeded ${subjectRows.length} subjects + ${chapterRows.length} chapters → server Postgres`,
  );
  await closeDb();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
