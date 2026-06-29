# פריסה לאוויר — Vercel + Postgres מתארח

האפליקציה מוכנה לפריסה ב-100%. צריך רק שרת שמריץ Node + Postgres מתארח
(GitHub Pages לא מתאים — סטטי בלבד). מומלץ **Vercel** (אירוח Next.js) + **Neon**
(Postgres חינמי). הקוד כבר תומך: כש-`DATABASE_URL` מוגדר הוא משתמש בשרת אמיתי.

## שלב 1 — מסד נתונים (Neon)

1. היכנס ל-https://neon.tech → צור חשבון (חינם) → New Project.
2. העתק את ה-**Connection string** (נראה כך):
   `postgresql://USER:PASSWORD@HOST/DB?sslmode=require`

## שלב 2 — הזרעת המסד המתארח (פעם אחת, מקומית)

מתיקיית `web/`, עם מחרוזת ה-Neon:

```bash
# Windows PowerShell:
$env:DATABASE_URL="postgresql://...neon..."; npm run db:migrate; npm run db:seed
```

זה יוצר את הטבלאות (מיגרציות) ומזריע 4 נושאים + 39 פרקים מהמסד המתארח.

## שלב 3 — פריסה (Vercel)

1. https://vercel.com → צור חשבון → **Add New… → Project** → ייבא את
   `yanivmizrachiy/bbb`.
2. ב-**Root Directory** בחר `web`.
3. ב-**Environment Variables** הוסף:
   `DATABASE_URL = postgresql://...neon...`
4. **Deploy**. תוך ~דקה תקבל כתובת חיה (כמו `https://bbb-xxx.vercel.app`).

## זהו — ומכאן הכול אוטומטי 🔄

האתר חי, נטען מ-PostgreSQL אמיתי. **לאחר החיבור החד-פעמי הזה, כל `git push`
ל-`main` יפעיל פריסה אוטומטית ב-Vercel** — כלומר הסנכרון מקומי → GitHub → Vercel
הופך לאוטומטי לחלוטין. אין צורך לחזור על שלבי ההקמה.

> הערה: האפליקציה **עצמאית** — היא מגישה את תמונות-העמודים וה-PDF בעצמה
> (`public/worksheets`, נוצר ע"י `npm run content:sync` שרץ אוטומטית ב-build).
> המלל/התוכן לא משתנה — המסד מחזיק מטא-דאטה בלבד.
>
> **לאחר הפריסה:** אפשר למחוק את קבצי-ההגשה הסטטיים הישנים (root/subject
> `index.html`, `viewer.html`) שכבר מיותרים — לא נמחקו קודם כדי לא לשבור את
> אתר ה-GitHub-Pages לפני ש-Vercel חי.
