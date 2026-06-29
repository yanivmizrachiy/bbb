import { getSubjects } from "@/db/data";
import Catalog from "./Catalog";

// Always render per-request, not at build time.
export const dynamic = "force-dynamic";

export default async function Home() {
  const subjects = await getSubjects();
  return <Catalog subjects={subjects} />;
}
