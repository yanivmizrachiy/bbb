import { NextResponse } from "next/server";
import { getSubjects, getAllChapters } from "@/db/data";

export const dynamic = "force-dynamic";

/** GET /api/subjects — the catalog + chapter list (Postgres when configured,
 *  else the bundled snapshot). */
export async function GET() {
  const [subjectRows, chapterRows] = await Promise.all([
    getSubjects(),
    getAllChapters(),
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
