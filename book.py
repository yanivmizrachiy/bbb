# -*- coding: utf-8 -*-
"""Master builder: rebuilds every subject, then generates the book home page
with fully dynamic statistics read from each subject's meta.json."""
import os, sys, json, subprocess, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = ["uncertainty", "algebra", "algebra8"]   # order on the home page (source-file order)
GH_URL = "https://github.com/yanivmizrachiy/bbb"

# 1) build every subject (each writes its own index/viewer/PDF/pages/meta.json)
#    pass --home-only to regenerate just the home page from existing meta.json
if "--home-only" not in sys.argv:
    for sub in SUBJECTS:
        print(f"=== building {sub} ===")
        subprocess.run([sys.executable, "build.py"], cwd=os.path.join(ROOT, sub), check=True)

# 2) read live stats
metas = []
for sub in SUBJECTS:
    m = json.load(open(os.path.join(ROOT, sub, "meta.json"), encoding="utf-8"))
    m["key"] = sub
    metas.append(m)

tot_q = sum(m["questions"] for m in metas)
tot_p = sum(m["pages"] for m in metas)
tot_s = len(metas)

# 3) subject cards (dynamic)
cards = ""
for m in metas:
    pdf = m["key"] + "/" + urllib.parse.quote(m["pdf"])
    cards += f"""
   <div class="subject" style="--cc:{m['color']}">
     <div class="shead">
       <div class="sicon">{m['icon']}</div>
       <div class="sinfo">
         <div class="stitle">{m['title']}</div>
         <div class="ssub">{m['subtitle']}</div>
         <div class="smeta">{m['questions']} שאלות &nbsp;·&nbsp; {m['chapters']} פרקים &nbsp;·&nbsp; {m['pages']} עמ'</div>
       </div>
     </div>
     <div class="sbtns">
       <a class="sb" href="{m['key']}/viewer.html">צפייה בדפים</a>
       <a class="sb" href="{pdf}" download>הורדה</a>
       <a class="sb" href="{m['key']}/index.html">פתיחה</a>
     </div>
   </div>"""

HOME = """<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>מתמטיקה לחטיבת הביניים</title><style>
 *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
 body{font-family:'Segoe UI','Arial',sans-serif;color:#1f2a44;min-height:100vh;background:radial-gradient(1100px 560px at 85% -12%,#e7ecff 0,transparent 60%),radial-gradient(820px 460px at -5% 2%,#dff5ee 0,transparent 55%),#f4f6fb}
 .wrap{max-width:720px;margin:0 auto;padding:28px 16px 64px}
 .hero{background:linear-gradient(135deg,#4f46e5 0,#7c3aed 52%,#0d9488 100%);border-radius:26px;padding:42px 26px;color:#fff;text-align:center;box-shadow:0 16px 44px rgba(79,70,229,.28)}
 .hero .kick{font-size:12px;letter-spacing:5px;opacity:.9;margin-bottom:10px}
 .hero h1{font-size:clamp(30px,8vw,42px);letter-spacing:.5px;margin-bottom:8px}
 .hero p{opacity:.94;font-size:clamp(13px,3.6vw,15px)}
 .stats{display:flex;gap:11px;justify-content:center;margin:-26px auto 0;max-width:440px;position:relative}
 .stat{flex:1;background:#fff;border-radius:16px;padding:15px 6px;text-align:center;box-shadow:0 8px 22px rgba(20,25,50,.10)}
 .stat b{display:block;font-size:clamp(22px,6vw,27px);font-weight:800;background:linear-gradient(135deg,#4f46e5,#0d9488);-webkit-background-clip:text;background-clip:text;color:transparent}
 .stat span{font-size:11.5px;color:#5b6573}
 .lbl{text-align:center;color:#9aa1b3;font-size:11px;font-weight:600;margin:30px 0 16px;letter-spacing:4px}
 .subject{background:#fff;border:0.75px solid #e8eaf1;border-radius:16px;margin:0 0 16px;overflow:hidden;box-shadow:0 6px 22px rgba(20,25,50,.05)}
 .subject::before{content:"";display:block;height:3px;background:var(--cc)}
 .shead{display:flex;align-items:center;gap:15px;padding:20px 22px 16px}
 .sicon{width:46px;height:46px;border-radius:12px;border:1.25px solid var(--cc);color:var(--cc);display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;flex-shrink:0}
 .sinfo{flex:1;min-width:0}
 .stitle{font-size:18px;font-weight:700;letter-spacing:.2px}
 .ssub{font-size:12.5px;color:#6b7280;margin-top:1px}
 .smeta{font-size:11.5px;color:var(--cc);font-weight:600;margin-top:7px;letter-spacing:.3px}
 .sbtns{display:flex;border-top:0.75px solid #eef0f4}
 .sb{flex:1;text-align:center;padding:13px 8px;font-size:13.5px;font-weight:600;color:#3a4256;text-decoration:none;border-inline-start:0.75px solid #eef0f4;transition:background .15s,color .15s}
 .sb:first-child{border-inline-start:none}
 .sb:hover{background:#fafbff;color:var(--cc)}
 .ext{display:flex;align-items:center;justify-content:center;gap:8px;margin:14px 0 0;padding:13px;border-radius:13px;background:transparent;border:0.75px solid #d7dae6;color:#6b7280;text-decoration:none;font-size:12.5px;font-weight:600;letter-spacing:.5px}
 .ext:hover{background:#fff;color:#4f46e5}
 .foot{text-align:center;color:#b6bbc7;font-size:9.5px;margin-top:28px;letter-spacing:3px}
</style></head><body>
<div class="wrap">
 <div class="hero">
   <div class="kick">אוסף שאלות להדפסה</div>
   <h1>מָתֵמָטִיקָה לַחֲטִיבַת הַבֵּינַיִים</h1>
   <p>שאלות מקור · עיצוב אחיד · מוכן להדפסה ב־A4</p>
 </div>
 <div class="stats">
   <div class="stat"><b>__TOTQ__</b><span>שאלות</span></div>
   <div class="stat"><b>__TOTS__</b><span>נושאים</span></div>
   <div class="stat"><b>__TOTP__</b><span>עמודי A4</span></div>
 </div>
 <div class="lbl">בחרו נושא</div>
__CARDS__
 <a class="ext" href="__GH__" target="_blank" rel="noopener">קוד המקור ב־GitHub</a>
 <div class="foot">מתמטיקה · חטיבת הביניים</div>
</div>
</body></html>"""
HOME = (HOME.replace("__TOTQ__", str(tot_q)).replace("__TOTS__", str(tot_s))
            .replace("__TOTP__", str(tot_p)).replace("__CARDS__", cards).replace("__GH__", GH_URL))
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(HOME)

# 4) dynamic README
rd = ["# מתמטיקה לחטיבת הביניים 📚", "",
      f"אוסף שאלות מעוצב להדפסה ב־A4, מחולק ל־**{tot_s} נושאים נפרדים** (ללא ערבוב ביניהם), "
      "עם עיצוב אחיד וגרפיקה וקטורית. כל הנתונים המספריים נגזרים אוטומטית מתוכן השאלות.", "",
      f"🌐 **אפליקציה חיה:** https://yanivmizrachiy.github.io/bbb/", "",
      f"> סה\"כ **{tot_q} שאלות** · **{tot_p} עמודי A4** · **{tot_s} נושאים**", "",
      "## הנושאים", "", "| נושא | שאלות | פרקים | עמודים | קישור |", "|---|---|---|---|---|"]
for m in metas:
    rd.append(f"| {m['title']} | {m['questions']} | {m['chapters']} | {m['pages']} | [`{m['key']}/`](./{m['key']}/) |")
rd += ["", "## מבנה", "```", "index.html        ← דף הבית של הספר (כפתורים לכל נושא)",
       "book.py           ← בונה את כל הנושאים + דף הבית (נתונים דינמיים)"]
for m in metas:
    rd.append(f"{m['key']}/           ← {m['title']}: build.py · charts.py · index.html · viewer.html · PDF · assets/")
rd += ["```", "", "## בנייה מחדש", "```bash", "pip install pymupdf playwright",
       "playwright install chromium", "python book.py", "```",
       "הפקודה בונה מחדש כל נושא, מעדכנת את `meta.json` שלו, ומרכיבה את דף הבית עם הסטטיסטיקות המעודכנות.",
       "", "*Python · PyMuPDF · Playwright/Chromium · SVG · RTL.*", ""]
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(rd))

print(f"BOOK built. subjects={tot_s} total_questions={tot_q} total_pages={tot_p}")
