import { eq, asc } from "drizzle-orm";
import { notFound } from "next/navigation";
import Link from "next/link";
import { db } from "@/db";
import {
  subjects as subjectsTable,
  chapters as chaptersTable,
} from "@/db/schema";
import styles from "./viewer.module.css";

export const dynamic = "force-dynamic";

// Worksheet assets are served by this app itself (synced into public/worksheets).
const ARTIFACTS = "/worksheets";

export default async function Viewer({
  params,
}: {
  params: Promise<{ subject: string }>;
}) {
  const { subject } = await params;

  const [s] = await db
    .select()
    .from(subjectsTable)
    .where(eq(subjectsTable.key, subject));

  if (!s) notFound();

  const chapterRows = await db
    .select()
    .from(chaptersTable)
    .where(eq(chaptersTable.subjectKey, subject))
    .orderBy(asc(chaptersTable.idx));

  const pdf = `${ARTIFACTS}/${s.key}/${encodeURIComponent(s.pdf)}`;
  const pages = Array.from({ length: s.pages }, (_, i) => i + 1);

  return (
    <div className={styles.viewer}>
      <div className={styles.head}>
        <div className={styles.bar}>
          <Link href={`/${s.key}`}>⌂ דף הנושא</Link>
          <span>
            📄 <b>{s.title}</b> · {s.pages} עמודים
          </span>
          <a href={pdf} target="_blank" rel="noopener">
            ⬇ הורדה
          </a>
        </div>
        <div className={styles.chapters}>
          {chapterRows.map((c) => (
            <a key={c.id} className={styles.tc} href={`#p${c.page}`}>
              <i style={{ background: c.color }}>{c.letter}</i>
              {c.title}
            </a>
          ))}
        </div>
      </div>

      <div className={styles.wrap}>
        {pages.map((i) => {
          const src = `${ARTIFACTS}/${s.key}/pages/p${String(i).padStart(
            3,
            "0",
          )}.png`;
          // eslint-disable-next-line @next/next/no-img-element
          const img = <img src={src} alt={`עמוד ${i}`} loading="lazy" />;
          // Page 1 is the cover — overlay the clickable table-of-contents hotspots.
          const hotspots = chapterRows.filter((c) => c.hotLeft != null);
          const body =
            i === 1 && hotspots.length > 0 ? (
              <div className={styles.imgwrap}>
                {img}
                {hotspots.map((c) => (
                  <a
                    key={c.id}
                    className={styles.hot}
                    href={`#p${c.page}`}
                    aria-label={`מעבר ל${c.title}`}
                    style={{
                      left: `${c.hotLeft}%`,
                      top: `${c.hotTop}%`,
                      width: `${c.hotWidth}%`,
                      height: `${c.hotHeight}%`,
                    }}
                  />
                ))}
              </div>
            ) : (
              img
            );
          return (
            <div key={i} id={`p${i}`} className={styles.sheet}>
              {body}
              <div className={styles.pgn}>
                עמוד {i} / {s.pages}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
