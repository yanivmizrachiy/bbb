"use client";

import { useState } from "react";
import Link from "next/link";
import type { Subject } from "@/db/schema";
import styles from "./catalog.module.css";

const ARTIFACTS = "https://yanivmizrachiy.github.io/bbb";

function tint(hex: string, a: number): string {
  const h = hex.replace("#", "");
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${a})`;
}
const vars = (o: Record<string, string>) => o as React.CSSProperties;

export default function Catalog({ subjects }: { subjects: Subject[] }) {
  const [active, setActive] = useState(0);
  const s = subjects[active];
  const totalQ = subjects.reduce((n, x) => n + x.questions, 0);
  const totalP = subjects.reduce((n, x) => n + x.pages, 0);

  return (
    <div className={styles.app}>
      <aside className={styles.rail}>
        <div className={styles.brand}>
          <div className={styles.kick}>אוסף שאלות להדפסה</div>
          <h1>מתמטיקה לחטיבת הביניים</h1>
        </div>
        <div className={styles.rstats}>
          {totalQ} שאלות · {subjects.length} נושאים · {totalP} עמ&#39;
        </div>
        <nav className={styles.nav}>
          {subjects.map((x, i) => (
            <button
              key={x.key}
              className={`${styles.navitem} ${i === active ? styles.active : ""}`}
              onClick={() => setActive(i)}
              style={vars({ "--c": x.orbDeep, "--tint": tint(x.orbDeep, 0.1) })}
            >
              <span
                className={styles.ic}
                style={{
                  background: `linear-gradient(135deg, ${x.orbLight}, ${x.orbDeep})`,
                }}
              />
              <span className={styles.nt}>
                <span className={styles.nm}>{x.title}</span>
                <span className={styles.ct}>{x.questions} שאלות</span>
              </span>
            </button>
          ))}
        </nav>
        <a
          className={styles.ext}
          href="https://github.com/yanivmizrachiy/bbb"
          target="_blank"
          rel="noopener"
        >
          קוד המקור ב־GitHub
        </a>
      </aside>

      <main className={styles.panel} style={vars({ "--c": s.orbDeep })}>
        <div className={styles.pbody}>
          <div className={styles.phead}>
            <span
              className={styles.porb}
              style={{
                background: `linear-gradient(135deg, ${s.orbLight}, ${s.orbDeep})`,
              }}
            />
            <div className={styles.ptitle}>{s.title}</div>
          </div>
          <div className={styles.psub}>{s.subtitle}</div>

          <div className={styles.pmeta}>
            <div className={styles.chip}>
              <b>{s.questions}</b>
              <span>שאלות</span>
            </div>
            <div className={styles.chip}>
              <b>{s.chapters}</b>
              <span>פרקים</span>
            </div>
            <div className={styles.chip}>
              <b>{s.pages}</b>
              <span>עמודי A4</span>
            </div>
          </div>

          <div className={styles.preview}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={`${ARTIFACTS}/${s.key}/assets/pages/p001.png`}
              alt={s.title}
              loading="lazy"
            />
          </div>

          <div className={styles.pactions}>
            <Link
              className={`${styles.btn} ${styles.primary}`}
              href={`/${s.key}/viewer`}
            >
              צפייה בדפים
            </Link>
            <a
              className={`${styles.btn} ${styles.ghost}`}
              href={`${ARTIFACTS}/${s.key}/${encodeURIComponent(s.pdf)}`}
              target="_blank"
              rel="noopener"
            >
              הורדה
            </a>
            <Link className={`${styles.btn} ${styles.ghost}`} href={`/${s.key}`}>
              פתיחה
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
