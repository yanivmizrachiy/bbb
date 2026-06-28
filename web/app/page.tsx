import { asc } from "drizzle-orm";
import { db } from "@/db";
import { subjects as subjectsTable } from "@/db/schema";
import Catalog from "./Catalog";

// Always render from the live database (per-request), not at build time.
export const dynamic = "force-dynamic";

export default async function Home() {
  const subjects = await db
    .select()
    .from(subjectsTable)
    .orderBy(asc(subjectsTable.sort));

  return <Catalog subjects={subjects} />;
}
