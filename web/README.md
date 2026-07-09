# web — מתמטיקה לחטיבת הביניים (Next.js 16 + PostgreSQL)

שדרוג האתר לטכנולוגיות מודרניות, **לצד** האתר הסטטי הקיים (שממשיך לרוץ על GitHub Pages).
הקטלוג, הנושאים והפרקים נטענים חי ממסד נתונים **PostgreSQL** דרך **Drizzle ORM**.
**התוכן/המלל של דפי־העבודה אינו במסד** — המסד מחזיק מטא־דאטה בלבד (שמות, ספירות, פרקים).

## הסטאק

- **Next.js 16.2** (App Router, React 19, TypeScript)
- **PostgreSQL** דרך **Drizzle ORM**, עם נפילה-רכה חכמה:
  - ללא `DATABASE_URL` — האתר מגיש **סנאפשוט מחויב** (`app/_data/catalog.json`
    דרך `db/data.ts`) — אפס התקנה, אפס מסד.
  - שרת Postgres אמיתי כש־`DATABASE_URL`/`POSTGRES_URL` מוגדר (Docker / Vercel / Neon).
  - PGlite (Postgres ב־WASM) משמש **בטסטים בלבד** (`test/db.test.ts`).

## הרצה מקומית (אפס התקנה — סנאפשוט)

```bash
cd web
npm install
npm run dev         # http://localhost:3000 — מגיש את הסנאפשוט המחויב
```

### אופציה: שרת Postgres אמיתי (Docker)

```bash
docker compose up -d db          # מתיקיית השורש bbb_work
# ב־web/.env: בטל הערה מ־DATABASE_URL, ואז:
npm run db:migrate && npm run db:seed && npm run dev
```

## מבנה

```
web/
  app/
    page.tsx              דף הבית — קטלוג נטען מ־Postgres
    [subject]/page.tsx    עמוד נושא + ניווט פרקים מ־Postgres
    api/subjects/route.ts  API: JSON של נושאים+פרקים מהמסד
  db/
    schema.ts     סכימת Drizzle — טבלאות subjects, chapters
    index.ts      חיבור שרת Postgres (pool יחיד, lazy) — ללא שרת מוגש הסנאפשוט
    seed.ts       הזרעה: נושאים מ־meta.json, פרקים מ־viewer.html (קריאה בלבד)
docker-compose.yml  (בשורש) — Postgres 16 לשרת אמיתי
```

## תוכנית ההגירה (הדרגתית, בלי לשבור את הקיים)

1. ✅ **שלב 1:** שלד Next.js 16 + Postgres + דף בית מהמסד.
2. ✅ **שלב 1.5:** Postgres אמיתי ללא Docker/הרשאות (PGlite, dual-driver).
3. ✅ **שלב 2:** עמוד נושא מהמסד.
4. ✅ **שלב 3:** טבלת `chapters` + ניווט פרקים + API — הכל מהמסד.
5. ⏳ **שלב 4:** פריסה לשרת אמיתי (Vercel/Railway + Postgres מתארח) — החלטת אירוח.
