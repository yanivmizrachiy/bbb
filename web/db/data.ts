import { asc, eq } from "drizzle-orm";
import { db, usingServer } from "./index";
import {
  subjects as subjectsTable,
  chapters as chaptersTable,
  type Subject,
  type Chapter,
} from "./schema";
import snapshot from "../app/_data/catalog.json";

// Single data-access layer. When a real Postgres server is configured
// (DATABASE_URL / POSTGRES_URL) it reads live from the DB; otherwise it serves
// the build-time snapshot — so the deployed site works with zero database
// setup, and "upgrades" to live Postgres the moment one is attached.
const snap = snapshot as unknown as { subjects: Subject[]; chapters: Chapter[] };

export async function getSubjects(): Promise<Subject[]> {
  if (usingServer)
    return db.select().from(subjectsTable).orderBy(asc(subjectsTable.sort));
  return [...snap.subjects].sort((a, b) => a.sort - b.sort);
}

export async function getSubject(key: string): Promise<Subject | undefined> {
  if (usingServer) {
    const [s] = await db
      .select()
      .from(subjectsTable)
      .where(eq(subjectsTable.key, key));
    return s;
  }
  return snap.subjects.find((s) => s.key === key);
}

export async function getChapters(key: string): Promise<Chapter[]> {
  if (usingServer)
    return db
      .select()
      .from(chaptersTable)
      .where(eq(chaptersTable.subjectKey, key))
      .orderBy(asc(chaptersTable.idx));
  return snap.chapters
    .filter((c) => c.subjectKey === key)
    .sort((a, b) => a.idx - b.idx);
}

export async function getAllChapters(): Promise<Chapter[]> {
  if (usingServer)
    return db.select().from(chaptersTable).orderBy(asc(chaptersTable.idx));
  return [...snap.chapters].sort((a, b) => a.idx - b.idx);
}
