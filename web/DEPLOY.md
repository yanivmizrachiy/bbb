# פריסה אוטומטית לאוויר — Vercel (turnkey)

האפליקציה מוכנה ב-100% וה-**אוטומציה כבר מובנית בקוד**:
- הזרעת המסד רצה **אוטומטית בכל פריסה** (סקריפט `vercel-build` → migrate + seed).
- המסד מתחבר **ללא הגדרת-סביבה ידנית** — הקוד מזהה את משתני-הסביבה ש-Vercel Postgres
  מזריק לבד (`POSTGRES_URL`), וגם `DATABASE_URL` אם תעדיף Neon חיצוני.

לכן הכול אוטומטי **חוץ מהתחברות חד-פעמית לחשבון שלך** — את זה רק אתה יכול לעשות
(אסור לי ליצור חשבונות / להזין סיסמאות / לאשר OAuth בשמך). זה ~3 דקות, פעם אחת.

## ההתחברות החד-פעמית (רק אתה)

1. **https://vercel.com → Sign Up with GitHub** (התחבר עם חשבון ה-GitHub שלך ואשר).
2. **Add New… → Project → Import** את `yanivmizrachiy/bbb`.
3. ב-**Root Directory** בחר `web` → **Deploy** (הפריסה הראשונה תרוץ; זה תקין שהמסד עדיין ריק).
4. בפרויקט: **Storage → Create Database → Postgres** → חבר אותו לפרויקט.
   Vercel מזריק את `POSTGRES_URL` אוטומטית — **אין צורך להעתיק/להדביק כלום**.
5. **Deployments → Redeploy** (פריסה אחת אחרי חיבור המסד). זהו — האתר חי ומלא.

> רוצה Neon חיצוני במקום? במקום שלב 4: צור מסד ב-https://neon.tech, והוסף
> ב-**Settings → Environment Variables** את `DATABASE_URL = postgresql://…neon…`.

## מכאן — סנכרון אוטומטי מלא 🔄

לאחר הייבוא החד-פעמי, **כל `git push` ל-`main` נפרס אוטומטית ב-Vercel** (כולל
הזרעת-מסד מחדש דרך `vercel-build`). הסנכרון מקומי → GitHub → Vercel הופך מלא ואוטומטי.

> האפליקציה **עצמאית**: מגישה את תמונות-העמודים וה-PDF בעצמה
> (`public/worksheets`, נוצר ב-build), והמסד מחזיק מטא-דאטה בלבד — המלל לא משתנה.
>
> **חשוב — לא למחוק את תוצרי ה-Python:** `meta.json`, `viewer.html` ותמונות
> `assets/pages/` של כל נושא הם **קלט של הבנייה** בכל פריסה
> (`sync-content.mjs` + `gen-data.ts` + `db/seed.ts` קוראים אותם). מחיקתם
> תפיל את הפריסה הבאה. רק `index.html` הסטטיים (root/נושא) הם הגשה-ישנה בלבד.
