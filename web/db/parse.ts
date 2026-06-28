import type { NewChapter } from "./schema";

// One chapter chip in a viewer.html chapter strip:
// <a class="tc" href="#p2" style="--cc:#4f46e5"><i>א</i>המעגל וחלקיו</a>
const CHIP =
  /<a class="tc" href="#p(\d+)" style="--cc:([^"]+)"><i>([^<]+)<\/i>([^<]+)<\/a>/g;

// One transparent cover-TOC hotspot (overlaid on the cover image):
// <a class="hot" href="#p2" style="left:6.470%;top:27.064%;width:87.060%;height:4.525%"
const HOT =
  /<a class="hot" href="#p(\d+)" style="left:([\d.]+)%;top:([\d.]+)%;width:([\d.]+)%;height:([\d.]+)%"/g;

/** Extract a subject's chapters (+ their clickable cover hotspot, if any) from
 *  its viewer.html — read-only, never touches worksheet content. */
export function parseChapterStrip(
  html: string,
  subjectKey: string,
): NewChapter[] {
  const hot = new Map<number, [number, number, number, number]>();
  const hre = new RegExp(HOT.source, "g");
  let hm: RegExpExecArray | null;
  while ((hm = hre.exec(html))) {
    hot.set(Number(hm[1]), [
      Number(hm[2]),
      Number(hm[3]),
      Number(hm[4]),
      Number(hm[5]),
    ]);
  }

  const re = new RegExp(CHIP.source, "g");
  const out: NewChapter[] = [];
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = re.exec(html))) {
    const page = Number(m[1]);
    const h = hot.get(page);
    out.push({
      subjectKey,
      idx: i++,
      page,
      color: m[2],
      letter: m[3],
      title: m[4],
      hotLeft: h ? h[0] : null,
      hotTop: h ? h[1] : null,
      hotWidth: h ? h[2] : null,
      hotHeight: h ? h[3] : null,
    });
  }
  return out;
}
