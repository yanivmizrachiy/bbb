import type { MetadataRoute } from "next";
import { getSubjects } from "@/db/data";

// Render at request time like every other DB-backed route. Without this the
// sitemap is prerendered during `next build`, which queries Postgres *before*
// vercel-build's migrate+seed step has run — a fresh DB fails the whole build.
export const dynamic = "force-dynamic";

const BASE = "https://bbb-ten-plum.vercel.app";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const subjects = await getSubjects();
  const now = new Date();

  const urls: MetadataRoute.Sitemap = [
    { url: BASE, lastModified: now, changeFrequency: "weekly", priority: 1 },
  ];
  for (const s of subjects) {
    urls.push({
      url: `${BASE}/${s.key}`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.8,
    });
    urls.push({
      url: `${BASE}/${s.key}/viewer`,
      lastModified: now,
      changeFrequency: "monthly",
      priority: 0.6,
    });
  }
  return urls;
}
