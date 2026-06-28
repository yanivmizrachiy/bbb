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

const ARTIFACTS = "https://yanivmizrachiy.github.io/bbb";

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
        {pages.map((i) => (
          <div key={i} id={`p${i}`} className={styles.sheet}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`${ARTIFACTS}/${s.key}/assets/pages/p${String(i).padStart(
                3,
                "0",
              )}.png`}
              alt={`עמוד ${i}`}
              loading="lazy"
            />
            <div className={styles.pgn}>
              עמוד {i} / {s.pages}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
