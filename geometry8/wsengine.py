# -*- coding: utf-8 -*-
"""Shared worksheet engine for the grade-8 algebra booklet.

Design goal: full separation of CONTENT from PRESENTATION.
  * Each topic lives in its own file under topics/  (easy, isolated edits).
  * This module owns the helpers, the (uniform) CSS, and render().
  * The table of contents + per-section colours are collected automatically
    from the SECTION() calls, so adding/removing a topic needs no other edit.

A topic file looks like:

    import wsengine as W, charts as C
    def build():
        W.SECTION("א", "פונקציה וקריאת גרף", "...", "#4f46e5")
        W.Q(1, "...")
        W.ENDSEC()
"""
import os

CARDS = []          # rendered question/section html, in order
SECTIONS = []       # (letter, title, color) collected for the TOC
_qn = [0]           # per-section auto counter


# ---------- inline helpers ----------
def L(x):
    return f'<span dir="ltr">{x}</span>'

def lines(n):
    return '<div class="lines">' + '<div class="ln"></div>' * n + '</div>'

def parts(items):
    out = ['<ol class="parts">']
    for it in items:
        lab, body = it[0], it[1]
        nl = it[2] if len(it) > 2 else 0
        out.append(f'<li><span class="plab">{lab}</span><div class="ptext">{body}{lines(nl) if nl else ""}</div></li>')
    out.append('</ol>')
    return "".join(out)

def mc(options):
    out = ['<div class="mc">']
    for lab, txt in options:
        out.append(f'<div class="opt"><span class="ol">{lab}</span><span class="ot">{txt}</span></div>')
    out.append('</div>')
    return "".join(out)

def table(headers, rows, cls="tbl"):
    out = [f'<table class="{cls}"><thead><tr>']
    out += [f'<th>{h}</th>' for h in headers]
    out.append('</tr></thead><tbody>')
    for r in rows:
        out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>')
    out.append('</tbody></table>')
    return "".join(out)

def fig(svg, cap="", w=None):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    style = f' style="max-width:{w}%;margin-inline:auto"' if w else ""
    return f'<div class="figure"{style}>{svg}{c}</div>'

def img(name, w=64, cap=""):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="figure"><img class="embed" src="assets/{name}.png" style="max-width:{w}%" alt="{name}">{c}</div>'

def note(html):
    CARDS.append(f'<div class="note">{html}</div>')


# ---------- structure ----------
_HEB = "א ב ג ד ה ו ז ח ט י יא יב יג יד טו טז יז יח יט כ כא כב".split()
def _letter(n):
    return _HEB[n - 1] if n <= len(_HEB) else str(n)

def SECTION(title, subtitle, color):
    """Letter is auto-assigned sequentially across the whole booklet."""
    _qn[0] = 0
    letter = _letter(len(SECTIONS) + 1)
    SECTIONS.append((letter, title, color))
    CARDS.append(f'<section class="topic" style="--c:{color}"><div class="sectionbar">'
                 f'<div class="secletter">{letter}</div><div><div class="sectitle">{title}</div>'
                 f'<div class="secsub">{subtitle}</div></div></div>')

def Q(num, body, src="", grade=""):
    if isinstance(num, int):
        _qn[0] += 1
        label = str(_qn[0])
    else:
        label = num
    pill = f'<span class="pill">{src}</span>' if src else ""
    gp = f'<span class="pill grade">{grade}</span>' if grade else ""
    CARDS.append(f'<div class="q"><div class="qhead"><span class="qnum">{label}</span>'
                 f'<div class="qtags">{src and pill}{gp}</div></div><div class="qbody">{body}</div></div>')

def ENDSEC():
    CARDS.append('</section>')


# ---------- presentation (identical to the other booklets) ----------
CSS = """
@page { size: A4; margin: 16mm 12mm 18mm 12mm; }
* { box-sizing: border-box; }
html,body { margin:0; padding:0; }
body { direction: rtl; font-family:'Segoe UI','Arial',sans-serif; color:#1f2a44; font-size:11pt; line-height:1.55; }
p { margin:6px 0; }
.cover { height: 262mm; display:flex; flex-direction:column; justify-content:center; align-items:stretch; page-break-after: always; }
.cover .band { text-align:center; padding:0 28px; }
.cover .kick { font-size:10.5pt; letter-spacing:6px; color:#9aa1b3; font-weight:400; margin:0 0 18px; }
.cover h1 { font-size:30pt; font-weight:600; color:#3730a3; letter-spacing:1px; margin:0; }
.cover .rule { width:88px; height:3px; margin:18px auto 0; background:linear-gradient(90deg,#4f46e5,#7c3aed 55%,#0d9488); border-radius:2px; }
.cover .sub { font-size:13pt; color:#5b6573; font-weight:400; margin-top:16px; }
.cover .meta { margin-top:14px; font-size:11pt; opacity:.9; }
.toc { margin:40px 6px 0; }
.toc h2 { color:#1f2a44; font-size:12pt; font-weight:600; letter-spacing:5px; padding-bottom:12px; border-bottom:1.5px solid #1f2a44; margin:0; }
.toc ol { list-style:none; padding:0; margin:0; }
.toc li { display:flex; align-items:center; gap:18px; padding:13px 2px; border-bottom:0.75px solid #ececf1; }
.toc li:last-child { border-bottom:none; }
.toc .idx { color:var(--cc,#4f46e5); font-size:11pt; font-weight:600; letter-spacing:1px; min-width:24px; text-align:center; }
.toc .nm { flex:1; font-size:12pt; color:#2a3142; letter-spacing:.2px; }
.toc .tick { width:24px; height:1.5px; background:var(--cc,#4f46e5); opacity:.5; }
.cover .foot { margin-top:auto; text-align:center; color:#b6bbc7; font-size:8pt; letter-spacing:3px; padding-top:18px;}
.sectionbar { display:flex; align-items:center; gap:16px; background:var(--c); color:#fff; border-radius:14px; padding:14px 20px; margin:4px 0 14px; page-break-before: always; page-break-after: avoid; box-shadow:0 4px 14px rgba(0,0,0,.10); }
.secletter { width:46px; height:46px; border-radius:12px; background:rgba(255,255,255,.22); display:flex; align-items:center; justify-content:center; font-size:22pt; font-weight:800; }
.sectitle { font-size:17pt; font-weight:800; }
.secsub { font-size:10.5pt; opacity:.92; }
.q { border:1px solid #e6e8ee; border-radius:12px; padding:12px 16px 14px; margin:11px 0; background:#fff; page-break-inside: avoid; }
.qhead { display:flex; align-items:center; gap:10px; margin-bottom:4px; }
.qnum { background:var(--c,#4f46e5); color:#fff; min-width:30px; height:30px; padding:0 9px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:12.5pt; flex:0 0 auto; }
.qtags { display:flex; gap:6px; }
.pill { background:#eef0fb; color:#4f46e5; border:1px solid #dfe3fb; border-radius:999px; padding:2px 10px; font-size:8.5pt; font-weight:700; }
.qbody { font-size:11pt; }
ol.parts { list-style:none; margin:8px 0 0; padding:0; }
ol.parts > li { display:flex; gap:8px; margin:7px 0; align-items:flex-start; }
.plab { font-weight:800; color:var(--c,#4f46e5); flex:0 0 auto; min-width:30px; }
.ptext { flex:1; }
.mc { margin:8px 0 2px; display:grid; grid-template-columns:1fr 1fr; gap:6px 18px; }
.opt { display:flex; gap:8px; align-items:baseline; }
.ol { width:22px; height:22px; border:1.6px solid #c7ccda; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:9pt; font-weight:700; color:#4b5468; flex:0 0 auto;}
.ot { flex:1; }
.lines { margin:8px 0 2px; }
.ln { border-bottom:1px dotted #c2c8d6; height:21px; }
.figure { margin:10px auto; text-align:center; page-break-inside:avoid; }
svg.chart { display:block; margin:4px auto; max-width:100%; height:auto; }
.cap { color:#5b6573; font-size:9.5pt; margin-top:2px; font-weight:600; }
img.embed { max-width:64%; height:auto; border:1px solid #e6e8ee; border-radius:8px; padding:6px; background:#fff; }
table.tbl { border-collapse:collapse; margin:9px auto; font-size:10.5pt; }
table.tbl th, table.tbl td { border:1px solid #c7ccda; padding:6px 12px; text-align:center; vertical-align:middle; }
table.tbl thead th { background:#f4f5fb; color:#3a4256; font-weight:700; }
.blank { display:inline-block; min-width:46px; border-bottom:1.6px solid #9aa3b8; height:14px; }
.note { background:#f7f8fc; border:1px solid #e6e8ee; border-right:5px solid var(--c,#4f46e5); border-radius:8px; padding:8px 14px; margin:12px 0; font-size:10pt; color:#3a4256; page-break-inside:avoid; }
@media screen { html { background:#e9ebf0; } body { max-width: 880px; margin: 22px auto 60px; padding: 32px 44px; background:#fff; box-shadow:0 4px 24px rgba(20,25,50,.14); border-radius:6px; } .cover { height:auto; min-height:auto; } }
"""

# palette cycled for the cover dots if a section omits a colour (kept uniform with siblings)


def render(OUT, h1, subtitle, meta_line, pdf_name, meta):
    """Assemble cover + all CARDS, then emit worksheet.html, PDF, page images,
    viewer.html, index.html (app) and meta.json into OUT."""
    import time, urllib.parse, json
    toc = "".join(f'<li style="--cc:{c}"><span class="idx">{l}</span><span class="nm">{t}</span><span class="tick"></span></li>'
                  for l, t, c in SECTIONS)
    cover = f"""<div class="cover">
  <div class="band"><div class="kick">מתמטיקה · חטיבת הביניים</div><h1>{h1}</h1><div class="rule"></div><div class="sub">{subtitle}</div></div>
  <div class="toc"><h2>תוכן העניינים</h2><ol>{toc}</ol></div>
  <div class="foot">מתמטיקה · חטיבת הביניים</div>
</div>"""
    html = (f'<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
            f'<title>{h1}</title><style>{CSS}</style></head><body>' + cover + "".join(CARDS) + "</body></html>")
    open(os.path.join(OUT, "worksheet.html"), "w", encoding="utf-8").write(html)

    from playwright.sync_api import sync_playwright
    pdf_path = os.path.join(OUT, pdf_name)
    foot = ('<div style="font-family:Segoe UI,Arial; font-size:8px; color:#9aa3b8; width:100%; text-align:center;">'
            + h1 + ' &nbsp;·&nbsp; עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file:///" + os.path.join(OUT, "worksheet.html").replace("\\", "/"))
        pg.pdf(path=pdf_path, format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>", footer_template=foot,
               margin={"top": "16mm", "bottom": "18mm", "left": "12mm", "right": "12mm"})
        b.close()

    import fitz, glob
    pages_dir = os.path.join(OUT, "assets", "pages"); os.makedirs(pages_dir, exist_ok=True)
    for old in glob.glob(os.path.join(pages_dir, "*.png")):
        os.remove(old)
    doc = fitz.open(pdf_path); npages = doc.page_count
    for i in range(npages):
        doc[i].get_pixmap(dpi=120).save(os.path.join(pages_dir, f"p{i+1:03d}.png"))
    doc.close()

    ts = int(time.time()); pdf_href = urllib.parse.quote(pdf_name)
    nq = len([c for c in CARDS if c.startswith('<div class="q"')]); nchap = len(SECTIONS)
    sheets = "".join(f'<div class="sheet"><img src="assets/pages/p{i+1:03d}.png?v={ts}" loading="lazy" alt="עמוד {i+1}">'
                     f'<div class="pgn">עמוד {i+1} / {npages}</div></div>' for i in range(npages))
    viewer = f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h1} — תצוגת הדפים</title><style>
 html,body{{margin:0;background:#e9ebf0;font-family:'Segoe UI',Arial,sans-serif}}
 .bar{{position:sticky;top:0;z-index:5;background:#191c2e;color:#eef;padding:11px 16px;font-size:13.5px;display:flex;gap:16px;align-items:center;justify-content:center}}
 .bar b{{color:#fff}} .bar a{{color:#8ad7ff;text-decoration:none;font-weight:600}}
 .wrap{{padding:22px 10px 70px;display:flex;flex-direction:column;align-items:center;gap:22px}}
 .sheet{{width:min(820px,96vw);background:#fff;box-shadow:0 5px 20px rgba(20,25,50,.22);border-radius:3px;overflow:hidden}}
 .sheet img{{display:block;width:100%;height:auto}}
 .pgn{{text-align:center;color:#7a8194;font-size:11px;padding:6px;background:#fafbfd;border-top:1px solid #eef}}
</style></head><body>
<div class="bar"><a href="index.html">⌂ דף הנושא</a> <span>📄 <b>תצוגת הדפים A4</b> · {npages} עמודים</span> <a href="{pdf_href}?v={ts}" download>⬇ הורדה</a></div>
<div class="wrap">{sheets}</div></body></html>"""
    open(os.path.join(OUT, "viewer.html"), "w", encoding="utf-8").write(viewer)

    chips = "".join(f'<span class="chip" style="--cc:{c}"><i>{l}</i>{t}</span>' for l, t, c in SECTIONS)
    APP = """<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__H1__</title><style>
 *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
 body{font-family:'Segoe UI','Arial',sans-serif;color:#1f2a44;min-height:100vh;background:radial-gradient(1100px 560px at 85% -12%,#e7ecff 0,transparent 60%),radial-gradient(820px 460px at -5% 2%,#dff5ee 0,transparent 55%),#f4f6fb}
 .wrap{max-width:680px;margin:0 auto;padding:26px 16px 60px}
 .hero{text-align:center;padding:26px 16px 6px}
 .hero .kick{font-size:11px;letter-spacing:5px;color:#9aa1b3;margin-bottom:12px}
 .hero h1{font-size:clamp(24px,6vw,30px);font-weight:600;color:#3730a3;letter-spacing:.5px;margin:0}
 .hero .rule{width:84px;height:3px;margin:14px auto 0;background:linear-gradient(90deg,#4f46e5,#7c3aed 55%,#0d9488);border-radius:2px}
 .hero p{color:#5b6573;font-size:clamp(13px,3.6vw,15px);margin-top:14px}
 .stats{display:flex;gap:10px;justify-content:center;margin:18px auto 0;max-width:420px;position:relative}
 .stat{flex:1;background:#fff;border-radius:15px;padding:14px 6px;text-align:center;box-shadow:0 8px 20px rgba(20,25,50,.09)}
 .stat b{display:block;font-size:clamp(20px,6vw,25px);font-weight:800;background:linear-gradient(135deg,#4f46e5,#0d9488);-webkit-background-clip:text;background-clip:text;color:transparent}
 .stat span{font-size:11.5px;color:#5b6573}
 .actions{display:flex;flex-direction:column;gap:11px;margin:26px 0 6px}
 .act{display:flex;align-items:center;gap:13px;padding:14px 15px;background:#fff;border:1px solid #e7e9f2;border-radius:16px;text-decoration:none;color:#1f2a44;box-shadow:0 2px 8px rgba(20,25,50,.04);transition:transform .15s,box-shadow .2s,border-color .2s}
 .act:hover{transform:translateY(-2px);border-color:#d3d8ea;box-shadow:0 10px 22px rgba(20,25,50,.09)}
 .act .ic{width:46px;height:46px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:21px;color:#fff;flex-shrink:0}
 .act .tx{flex:1;min-width:0} .act .tx b{display:block;font-size:16px} .act .tx span{font-size:12.5px;color:#7a8194}
 .act .ar{color:#c4cad8;font-size:24px;font-weight:300}
 .ic-view{background:linear-gradient(135deg,#6366f1,#7c3aed)} .ic-dl{background:linear-gradient(135deg,#0d9488,#10b981)} .ic-print{background:linear-gradient(135deg,#f59e0b,#d97706)}
 .lbl{text-align:center;color:#6b7280;font-size:12.5px;font-weight:700;margin:24px 0 11px;letter-spacing:1px}
 .chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
 .chip{display:flex;align-items:center;gap:8px;background:#fff;border-radius:12px;padding:7px 12px;font-size:12.5px;color:#3a4256;box-shadow:0 3px 12px rgba(20,25,50,.06);border-right:4px solid var(--cc)}
 .chip i{display:flex;align-items:center;justify-content:center;width:21px;height:21px;border-radius:50%;background:var(--cc);color:#fff;font-style:normal;font-weight:800;font-size:11.5px}
 .foot{text-align:center;color:#9aa3b8;font-size:11px;margin-top:28px}
</style></head><body><div class="wrap">
 <div class="hero"><div class="kick">אוסף שאלות להדפסה</div><h1>__H1__</h1><div class="rule"></div><p>__SUB__</p></div>
 <div class="stats"><div class="stat"><b>__NQ__</b><span>שאלות</span></div><div class="stat"><b>__NCHAP__</b><span>פרקים</span></div><div class="stat"><b>__NPAGES__</b><span>עמודי A4</span></div></div>
 <div class="actions">
   <a class="act" href="viewer.html"><span class="ic ic-view">📖</span><span class="tx"><b>צפייה בדפים</b><span>תצוגת A4 איכותית · גלילה נוחה</span></span><span class="ar">‹</span></a>
   <a class="act" href="__PDF__" download><span class="ic ic-dl">⬇</span><span class="tx"><b>הורדת ה־PDF</b><span>כל הדפים למכשיר · מוכן להדפסה</span></span><span class="ar">‹</span></a>
   <a class="act" href="__PDF__" target="_blank" rel="noopener"><span class="ic ic-print">🖨️</span><span class="tx"><b>הדפסה מהירה</b><span>פתיחת ה־PDF להדפסה ישירה</span></span><span class="ar">‹</span></a>
   <a class="act" href="../index.html"><span class="ic" style="background:linear-gradient(135deg,#64748b,#334155)">⌂</span><span class="tx"><b>חזרה לדף הראשי</b><span>כל הספר — מתמטיקה לחטיבת הביניים</span></span><span class="ar">‹</span></a>
 </div>
 <div class="lbl">הפרקים בנושא</div><div class="chips">__CHIPS__</div>
 <div class="foot">גרפיקה וקטורית · __NPAGES__ עמודי A4</div>
</div></body></html>"""
    APP = (APP.replace("__H1__", h1).replace("__SUB__", subtitle).replace("__NQ__", str(nq))
              .replace("__NCHAP__", str(nchap)).replace("__NPAGES__", str(npages))
              .replace("__PDF__", pdf_href).replace("__CHIPS__", chips))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(APP)

    meta = dict(meta); meta.update({"questions": nq, "chapters": nchap, "pages": npages, "pdf": pdf_name})
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[{meta.get('key')}] rendered: questions={nq} chapters={nchap} pages={npages}")
    return meta
