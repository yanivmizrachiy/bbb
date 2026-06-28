# web — מתמטיקה לחטיבת הביניים (Next.js 16 + PostgreSQL)

שדרוג האתר לטכנולוגיות מודרניות, **לצד** האתר הסטטי הקיים (שממשיך לרוץ על GitHub Pages).
הקטלוג (נושאים + נתונים) נטען חי ממסד נתונים **PostgreSQL** דרך **Drizzle ORM**.

## הסטאק

- **Next.js 16.2** (App Router, React 19, TypeScript)
- **PostgreSQL 16** (רץ מקומית ב־Docker)
- **Drizzle ORM** + `node-postgres` כשכבת הגישה לנתונים

## הרצה מקומית

```bash
# 1) מסד הנתונים (מתיקיית השורש bbb_work)
docker compose up -d db

# 2) מתיקיית web/
cp .env.example .env          # DATABASE_URL מקומי
npm install
npm run db:push               # יוצר את הטבלאות מתוך הסכימה (drizzle-kit)
npm run db:seed               # מזריע את הנושאים מתוך ../<subject>/meta.json
npm run dev                   # http://localhost:3000
```

## מבנה

```
web/
  app/            דפי Next.js (App Router) — הבית נטען מ־Postgres
  db/
    schema.ts     סכימת Drizzle (טבלת subjects)
    index.ts      חיבור ה־DB (pool יחיד)
    seed.ts       הזרעה מ־meta.json הקיימים
  drizzle.config.ts
docker-compose.yml  (בשורש) — Postgres 16
```

## תוכנית ההגירה (הדרגתית, בלי לשבור את הקיים)

1. **שלב 1 (בוצע):** שלד Next.js 16 + Postgres + הזרעת הנושאים + דף בית מהמסד.
2. **שלב 2:** טבלת `chapters` + ניווט פרקים מהמסד.
3. **שלב 3:** הגשת תוצרי ה־PDF/viewer מתוך Next.js.
4. **שלב 4:** פריסה לשרת אמיתי (Vercel/Railway + Postgres מתארח) — החלטת אירוח.
