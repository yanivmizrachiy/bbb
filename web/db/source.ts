import { readFileSync } from "node:fs";
import { join } from "node:path";
import type { NewSubject, NewChapter } from "./schema";
import { parseChapterStrip } from "./parse";

// Gradient-orb palette (matches the live site's home identity colors).
const ORB: Record<string, [string, string]> = {
  uncertainty: ["#f472b6", "#db2777"], // ורוד
  algebra: ["#fcd34d", "#b45309"], // זהב
  algebra8: ["#4ade80", "#15803d"], // ירוק
  geometry8: ["#38bdf8", "#0284c7"], // תכלת
};
export const ORDER = ["uncertainty", "algebra", "algebra8", "geometry8"];

/** Build the full catalog (subjects + chapters) from the existing static
 *  project files. `root` is the bbb_work/ directory. Pure: reads files only,
 *  never touches worksheet content. Shared by the DB seed AND the build-time
 *  snapshot generator, so both always agree. */
export function buildCatalog(root: string): {
  subjects: NewSubject[];
  chapters: NewChapter[];
} {
  const subjects: NewSubject[] = ORDER.map((key, i) => {
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

  const chapters: NewChapter[] = ORDER.flatMap((key) =>
    parseChapterStrip(readFileSync(join(root, key, "viewer.html"), "utf8"), key),
  );

  return { subjects, chapters };
}
