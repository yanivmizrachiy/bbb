import type { NewChapter } from "./schema";

// Matches one chapter chip in a generated viewer.html chapter strip:
// <a class="tc" href="#p2" style="--cc:#4f46e5"><i>א</i>המעגל וחלקיו</a>
const CHIP =
  /<a class="tc" href="#p(\d+)" style="--cc:([^"]+)"><i>([^<]+)<\/i>([^<]+)<\/a>/g;

/** Extract a subject's chapters from its viewer.html chapter strip (read-only). */
export function parseChapterStrip(
  html: string,
  subjectKey: string,
): NewChapter[] {
  const re = new RegExp(CHIP.source, "g");
  const out: NewChapter[] = [];
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = re.exec(html))) {
    out.push({
      subjectKey,
      idx: i++,
      page: Number(m[1]),
      color: m[2],
      letter: m[3],
      title: m[4],
    });
  }
  return out;
}
