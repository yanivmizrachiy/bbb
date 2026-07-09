import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getSubject, getChapters } from "@/db/data";
import styles from "./subject.module.css";

export const dynamic = "force-dynamic";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ subject: string }>;
}): Promise<Metadata> {
  const { subject } = await params;
  const s = await getSubject(subject);
  if (!s) return { title: "נושא לא נמצא" };
  return {
    title: `${s.title} — מתמטיקה לחטיבת הביניים`,
    description: `${s.subtitle} · ${s.questions} שאלות · ${s.chapters} פרקים · ${s.pages} עמודים.`,
  };
}

// Worksheet assets are served by this app itself (synced into public/worksheets).
const ARTIFACTS = "/worksheets";

export default async function SubjectPage({
  params,
}: {
  params: Promise<{ subject: string }>;
}) {
  // Next.js 16: params is async and must be awaited.
  const { subject } = await params;

  const s = await getSubject(subject);
  if (!s) notFound();

  const chapterRows = await getChapters(subject);

  const pdf = `${ARTIFACTS}/${s.key}/${encodeURIComponent(s.pdf)}`;

  return (
    <div className={styles.wrap}>
      <Link href="/" className={styles.back}>
        ← חזרה לכל הנושאים
      </Link>

      <div className={styles.card}>
        <div className={styles.bar} style={{ background: s.orbDeep }} />
        <div className={styles.body}>
          <div className={styles.head}>
            <span
              className={styles.orb}
              style={{
                background: `linear-gradient(135deg, ${s.orbLight}, ${s.orbDeep})`,
              }}
            />
            <div>
              <div className={styles.title}>{s.title}</div>
              <div className={styles.sub}>{s.subtitle}</div>
            </div>
          </div>

          <div className={styles.stats}>
            <div className={styles.stat}>
              <b style={{ color: s.orbDeep }}>{s.questions}</b>
              <span>שאלות</span>
            </div>
            <div className={styles.stat}>
              <b style={{ color: s.orbDeep }}>{s.chapters}</b>
              <span>פרקים</span>
            </div>
            <div className={styles.stat}>
              <b style={{ color: s.orbDeep }}>{s.pages}</b>
              <span>עמודי A4</span>
            </div>
          </div>

          <div className={styles.actions}>
            <Link
              className={`${styles.btn} ${styles.primary}`}
              href={`/${s.key}/viewer`}
              style={{ background: s.orbDeep }}
            >
              צפייה בדפים
            </Link>
            <a
              className={`${styles.btn} ${styles.ghost}`}
              href={pdf}
              target="_blank"
              rel="noopener"
            >
              הורדת PDF
            </a>
          </div>

          <div className={styles.chhead}>הפרקים בנושא</div>
          <ol className={styles.chlist}>
            {chapterRows.map((c) => (
              <li key={c.id}>
                <Link
                  className={styles.chrow}
                  href={`/${s.key}/viewer#p${c.page}`}
                >
                  <span
                    className={styles.chletter}
                    style={{ background: c.color }}
                  >
                    {c.letter}
                  </span>
                  <span className={styles.chtitle}>{c.title}</span>
                  <span className={styles.chpage}>עמ&apos; {c.page}</span>
                </Link>
              </li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
}
