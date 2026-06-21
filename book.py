# -*- coding: utf-8 -*-
"""Master builder: rebuilds every subject, then generates the book home page
with fully dynamic statistics read from each subject's meta.json."""
import os, sys, json, subprocess, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
SUBJECTS = ["uncertainty", "algebra", "algebra8", "geometry8"]   # order on the home page (source-file order)
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

# 3) home page — sidebar app: nav rail + dynamic panel (cover preview + actions)
def _rgba(hexc, a):
    h = hexc.lstrip("#"); r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

subj = []
for m in metas:
    subj.append({"key": m["key"], "title": m["title"], "subtitle": m["subtitle"],
                 "color": m["color"], "icon": m["icon"], "questions": m["questions"],
                 "chapters": m["chapters"], "pages": m["pages"],
                 "pdf": m["key"] + "/" + urllib.parse.quote(m["pdf"]),
                 "viewer": m["key"] + "/viewer.html", "index": m["key"] + "/index.html",
                 "cover": m["key"] + "/assets/pages/p001.png"})

nav = ""
for i, s in enumerate(subj):
    nav += (f'<button class="navitem{" active" if i == 0 else ""}" style="--c:{s["color"]};--tint:{_rgba(s["color"],0.09)}" onclick="sel({i})">'
            f'<span class="ic">{s["icon"]}</span>'
            f'<span class="nt"><span class="nm">{s["title"]}</span><span class="ct">{s["questions"]} שאלות</span></span></button>')

s0 = subj[0]
DATA_JS = json.dumps(subj, ensure_ascii=False)

HOME = """<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>מתמטיקה לחטיבת הביניים</title><style>
 *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
 body{font-family:'Segoe UI','Arial',sans-serif;color:#1f2a44;min-height:100vh;background:radial-gradient(1100px 560px at 85% -12%,#e7ecff 0,transparent 60%),radial-gradient(820px 460px at -5% 2%,#dff5ee 0,transparent 55%),#f4f6fb}
 .app{max-width:1000px;margin:0 auto;padding:22px 16px 56px;display:flex;gap:18px;align-items:flex-start}
 .rail{width:262px;flex:0 0 262px;background:#fff;border:0.75px solid #e8eaf1;border-radius:18px;padding:18px 14px;box-shadow:0 6px 22px rgba(20,25,50,.05);position:sticky;top:22px}
 .brand{padding:4px 8px 0}
 .brand .kick{font-size:9.5px;letter-spacing:4px;color:#9aa1b3}
 .brand h1{font-size:18px;font-weight:800;margin-top:5px;line-height:1.25;background:linear-gradient(135deg,#4f46e5,#7c3aed 55%,#0d9488);-webkit-background-clip:text;background-clip:text;color:transparent}
 .rstats{font-size:11px;color:#8a90a0;padding:8px 8px 14px;border-bottom:0.75px solid #eef0f4;margin-bottom:10px}
 nav{display:flex;flex-direction:column;gap:4px}
 .navitem{display:flex;align-items:center;gap:11px;width:100%;padding:10px 11px;border:none;border-inline-start:3px solid transparent;border-radius:12px;background:transparent;cursor:pointer;text-align:right;font-family:inherit;transition:background .15s}
 .navitem:hover{background:#fafbff}
 .navitem.active{background:var(--tint);border-inline-start-color:var(--c)}
 .navitem .ic{width:38px;height:38px;border-radius:11px;border:1.25px solid var(--c);color:var(--c);display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;flex:0 0 auto}
 .navitem .nt{display:flex;flex-direction:column;min-width:0}
 .navitem .nm{font-size:13.5px;font-weight:700;color:#1f2a44}
 .navitem .ct{font-size:10.5px;color:#9aa1b3;margin-top:1px}
 .ext{display:flex;align-items:center;justify-content:center;gap:7px;margin-top:14px;padding:11px;border-radius:12px;border:0.75px solid #e1e4ee;color:#8a90a0;text-decoration:none;font-size:11.5px;font-weight:600;letter-spacing:.4px}
 .ext:hover{color:#4f46e5;border-color:#cdd2e6}
 .panel{flex:1;min-width:0;background:#fff;border:0.75px solid #e8eaf1;border-radius:18px;box-shadow:0 6px 22px rgba(20,25,50,.05);overflow:hidden}
 .panel::before{content:"";display:block;height:4px;background:var(--c)}
 .pbody{padding:28px 30px 26px}
 .ptitle{font-size:clamp(24px,5vw,32px);font-weight:800;letter-spacing:.3px}
 .psub{font-size:14px;color:#6b7280;margin-top:4px}
 .pmeta{display:flex;gap:10px;margin:18px 0 22px}
 .chip{flex:1;background:#f6f7fb;border-radius:13px;padding:13px 8px;text-align:center}
 .chip b{display:block;font-size:22px;font-weight:800;color:var(--c)}
 .chip span{font-size:11px;color:#8a90a0}
 .preview{display:flex;justify-content:center;margin:0 0 22px}
 .preview img{max-width:60%;max-height:350px;border:0.75px solid #e1e4ee;border-radius:10px;box-shadow:0 10px 30px rgba(20,25,50,.12)}
 .pactions{display:flex;gap:10px;flex-wrap:wrap}
 .btn{flex:1;min-width:120px;text-align:center;padding:13px;border-radius:13px;text-decoration:none;font-size:14px;font-weight:700;transition:.15s}
 .btn.primary{background:var(--c);color:#fff}
 .btn.primary:hover{filter:brightness(1.07)}
 .btn.ghost{border:0.75px solid #d7dae6;color:#3a4256}
 .btn.ghost:hover{background:#fafbff;color:var(--c);border-color:var(--c)}
 .foot{text-align:center;color:#b6bbc7;font-size:9.5px;margin-top:26px;letter-spacing:3px}
 @media(max-width:820px){
  .app{flex-direction:column;gap:14px}
  .rail{width:100%;flex:none;position:static}
  .pbody{padding:22px 18px}
  .preview img{max-width:88%}
 }
</style></head><body>
<div class="app">
 <aside class="rail">
   <div class="brand"><div class="kick">אוסף שאלות להדפסה</div><h1>מתמטיקה לחטיבת הביניים</h1></div>
   <div class="rstats">__TOTQ__ שאלות · __TOTS__ נושאים · __TOTP__ עמ'</div>
   <nav>__NAV__</nav>
   <a class="ext" href="__GH__" target="_blank" rel="noopener">קוד המקור ב־GitHub</a>
 </aside>
 <main class="panel" id="panel" style="--c:__C0__">
   <div class="pbody">
     <div class="ptitle" id="pt">__T0__</div>
     <div class="psub" id="ps">__SUB0__</div>
     <div class="pmeta">
       <div class="chip"><b id="pq">__Q0__</b><span>שאלות</span></div>
       <div class="chip"><b id="pc">__CH0__</b><span>פרקים</span></div>
       <div class="chip"><b id="pp">__P0__</b><span>עמודי A4</span></div>
     </div>
     <div class="preview"><img id="pi" src="__COVER0__" alt="__T0__" loading="lazy"></div>
     <div class="pactions">
       <a class="btn primary" id="pv" href="__VIEW0__">צפייה בדפים</a>
       <a class="btn ghost" id="pd" href="__PDF0__" download>הורדה</a>
       <a class="btn ghost" id="po" href="__IDX0__">פתיחה</a>
     </div>
   </div>
 </main>
</div>
<div class="foot">מתמטיקה · חטיבת הביניים</div>
<script>
var D=__DATA__;
function sel(i){var s=D[i];
 var items=document.querySelectorAll('.navitem');
 for(var j=0;j<items.length;j++){items[j].classList.toggle('active',j===i);}
 document.getElementById('panel').style.setProperty('--c',s.color);
 document.getElementById('pt').textContent=s.title;
 document.getElementById('ps').textContent=s.subtitle;
 document.getElementById('pq').textContent=s.questions;
 document.getElementById('pc').textContent=s.chapters;
 document.getElementById('pp').textContent=s.pages;
 document.getElementById('pv').href=s.viewer;
 document.getElementById('pd').href=s.pdf;
 document.getElementById('po').href=s.index;
 var img=document.getElementById('pi');img.src=s.cover;img.alt=s.title;}
</script>
</body></html>"""
HOME = (HOME.replace("__TOTQ__", str(tot_q)).replace("__TOTS__", str(tot_s)).replace("__TOTP__", str(tot_p))
            .replace("__NAV__", nav).replace("__DATA__", DATA_JS).replace("__GH__", GH_URL)
            .replace("__C0__", s0["color"]).replace("__T0__", s0["title"]).replace("__SUB0__", s0["subtitle"])
            .replace("__Q0__", str(s0["questions"])).replace("__CH0__", str(s0["chapters"])).replace("__P0__", str(s0["pages"]))
            .replace("__COVER0__", s0["cover"]).replace("__VIEW0__", s0["viewer"]).replace("__PDF0__", s0["pdf"]).replace("__IDX0__", s0["index"]))
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
       "", "## אחידות עיצוב",
       "כל העמודים מעוצבים לפי [`STYLE_GUIDE.md`](./STYLE_GUIDE.md) (גופנים, צבעים, רכיבים, סימון מתמטי). "
       "המנוע הקנוני המשותף הוא `wsengine.py`. לפני כל קומיט הריצו את שומר-האחידות:",
       "```bash", "python tools/check_uniformity.py --heights", "```",
       "", "*Python · PyMuPDF · Playwright/Chromium · SVG · RTL.*", ""]
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write("\n".join(rd))

print(f"BOOK built. subjects={tot_s} total_questions={tot_q} total_pages={tot_p}")
