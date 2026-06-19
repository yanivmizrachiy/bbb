# מתמטיקה לחטיבת הביניים 📚

אוסף שאלות מעוצב להדפסה ב־A4, מחולק ל־**3 נושאים נפרדים** (ללא ערבוב ביניהם), עם עיצוב אחיד וגרפיקה וקטורית. כל הנתונים המספריים נגזרים אוטומטית מתוכן השאלות.

🌐 **אפליקציה חיה:** https://yanivmizrachiy.github.io/bbb/

> סה"כ **207 שאלות** · **134 עמודי A4** · **3 נושאים**

## הנושאים

| נושא | שאלות | פרקים | עמודים | קישור |
|---|---|---|---|---|
| תחום אי־וודאות | 54 | 7 | 43 | [`uncertainty/`](./uncertainty/) |
| אלגברה לכיתה ז' | 61 | 6 | 27 | [`algebra/`](./algebra/) |
| אלגברה לכיתה ח' | 92 | 12 | 64 | [`algebra8/`](./algebra8/) |

## מבנה
```
index.html        ← דף הבית של הספר (כפתורים לכל נושא)
book.py           ← בונה את כל הנושאים + דף הבית (נתונים דינמיים)
uncertainty/           ← תחום אי־וודאות: build.py · charts.py · index.html · viewer.html · PDF · assets/
algebra/           ← אלגברה לכיתה ז': build.py · charts.py · index.html · viewer.html · PDF · assets/
algebra8/           ← אלגברה לכיתה ח': build.py · charts.py · index.html · viewer.html · PDF · assets/
```

## בנייה מחדש
```bash
pip install pymupdf playwright
playwright install chromium
python book.py
```
הפקודה בונה מחדש כל נושא, מעדכנת את `meta.json` שלו, ומרכיבה את דף הבית עם הסטטיסטיקות המעודכנות.

*Python · PyMuPDF · Playwright/Chromium · SVG · RTL.*
