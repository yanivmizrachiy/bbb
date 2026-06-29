import type { MetadataRoute } from "next";
import { getSubjects } from "@/db/data";

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
