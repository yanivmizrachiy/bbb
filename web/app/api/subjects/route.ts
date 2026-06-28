import { NextResponse } from "next/server";
import { asc } from "drizzle-orm";
import { db } from "@/db";
import { subjects, chapters } from "@/db/schema";

export const dynamic = "force-dynamic";

/** GET /api/subjects — the catalog + chapter list, straight from PostgreSQL. */
export async function GET() {
  const [subjectRows, chapterRows] = await Promise.all([
    db.select().from(subjects).orderBy(asc(subjects.sort)),
    db.select().from(chapters).orderBy(asc(chapters.idx)),
  ]);

  const byKey = new Map<string, typeof chapterRows>();
  for (const c of chapterRows) {
    const list = byKey.get(c.subjectKey) ?? [];
    list.push(c);
    byKey.set(c.subjectKey, list);
  }

  return NextResponse.json({
    count: subjectRows.length,
    subjects: subjectRows.map((s) => ({
      ...s,
      chapterList: byKey.get(s.key) ?? [],
    })),
  });
}
