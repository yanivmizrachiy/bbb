import { asc } from "drizzle-orm";
import Link from "next/link";
import { db } from "@/db";
import { subjects as subjectsTable } from "@/db/schema";
import styles from "./page.module.css";

// Always render from the live database (per-request), not at build time.
export const dynamic = "force-dynamic";

export default async function Home() {
  const subjects = await db
    .select()
    .from(subjectsTable)
    .orderBy(asc(subjectsTable.sort));

  const totalQ = subjects.reduce((s, x) => s + x.questions, 0);
  const totalP = subjects.reduce((s, x) => s + x.pages, 0);

  return (
    <div className={styles.wrap}>
      <header className={styles.header}>
        <div className={styles.kick}>אוסף שאלות להדפסה</div>
        <h1 className={styles.title}>מתמטיקה לחטיבת הביניים</h1>
        <div className={styles.rule} />
        <p className={styles.sub}>שאלות מקור · עיצוב אחיד · מוכן להדפסה ב־A4</p>
        <div className={styles.dbtag}>
          <span className={styles.dot} />
          נטען חי מ־PostgreSQL · Next.js 16
        </div>
      </header>

      <div className={styles.stats}>
        <div className={styles.stat}>
          <b>{totalQ}</b>
          <span>שאלות</span>
        </div>
        <div className={styles.stat}>
          <b>{subjects.length}</b>
          <span>נושאים</span>
        </div>
        <div className={styles.stat}>
          <b>{totalP}</b>
          <span>עמודי A4</span>
        </div>
      </div>

      <div className={styles.grid}>
        {subjects.map((s) => (
          <article key={s.key} className={styles.card}>
            <span
              className={styles.orb}
              style={{
                background: `linear-gradient(135deg, ${s.orbLight}, ${s.orbDeep})`,
              }}
            />
            <div className={styles.ctitle}>{s.title}</div>
            <div className={styles.csub}>{s.subtitle}</div>
            <div className={styles.cmeta} style={{ color: s.orbDeep }}>
              {s.questions} שאלות &nbsp;·&nbsp; {s.chapters} פרקים &nbsp;·&nbsp;{" "}
              {s.pages} עמ&#39;
            </div>
            <Link
              className={styles.open}
              href={`/${s.key}`}
              style={{ background: s.orbDeep }}
            >
              פתיחת הנושא
            </Link>
          </article>
        ))}
      </div>

      <div className={styles.foot}>מתמטיקה · חטיבת הביניים</div>
    </div>
  );
}
