import { describe, it, expect } from "vitest";
import { parseChapterStrip } from "../db/parse";

const SAMPLE =
  '<div class="chapters">' +
  '<a class="tc" href="#p2" style="--cc:#4f46e5"><i>א</i>המעגל וחלקיו</a>' +
  '<a class="tc" href="#p4" style="--cc:#0d9488"><i>ב</i>היקף מעגל ושטחו</a>' +
  '<a class="tc" href="#p10" style="--cc:#7c3aed"><i>ג</i>גליל וחרוט</a>' +
  "</div>";

describe("parseChapterStrip", () => {
  it("extracts ordered chapters with page / color / letter / title", () => {
    const ch = parseChapterStrip(SAMPLE, "geometry8");
    expect(ch).toHaveLength(3);
    expect(ch[0]).toMatchObject({
      subjectKey: "geometry8",
      idx: 0,
      page: 2,
      color: "#4f46e5",
      letter: "א",
      title: "המעגל וחלקיו",
    });
    expect(ch[2]).toMatchObject({ idx: 2, page: 10, letter: "ג", title: "גליל וחרוט" });
  });

  it("returns an empty list when there are no chips", () => {
    expect(parseChapterStrip("<div></div>", "x")).toEqual([]);
  });
});
