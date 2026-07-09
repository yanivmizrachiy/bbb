# -*- coding: utf-8 -*-
"""Uniformity guard for the whole project — enforces STYLE_GUIDE.md.

Checks (static, no deps):
  1. CSS core design tokens are byte-identical across every CSS source.
  2. Math-notation symbols inside content (L("...")) follow the standard.
Optional (needs Playwright):  --heights  → flags any .q card taller than 263 mm.

Run from repo root:  python tools/check_uniformity.py [--heights]
Exit code 0 = all uniform, 1 = issues found.
"""
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_SOURCES = ["algebra8/wsengine.py", "geometry8/wsengine.py",
               "uncertainty/build.py", "algebra/build.py"]
CONTENT = glob.glob(os.path.join(ROOT, "*", "topics", "*.py")) + \
          [os.path.join(ROOT, "uncertainty", "build.py"),
           os.path.join(ROOT, "algebra", "build.py")]

# tokens that must appear verbatim in every CSS source (the shared design DNA)
CSS_TOKENS = [
    "font-family:'Segoe UI','Arial',sans-serif",
    "@page { size: A4; margin: 16mm 12mm 18mm 12mm; }",
    "border-radius:12px; padding:12px 16px 14px; margin:11px 0",        # .q card
    "linear-gradient(90deg,#4f46e5,#7c3aed 55%,#0d9488)",              # title accent rule
    "color:#3730a3",                                                    # title ink (cover + hero)
]

# forbidden -> required, checked inside L("...") content fragments
BAD_IN_L = [
    ("||", "∥ (parallel)"),
    ("∢", "∠ (angle)"),
    ("=~", "≅ (congruent)"),
    ("<=", "≤"), (">=", "≥"),
]
HYPHEN_MINUS = re.compile(r"(?<![\w])-\d|\d-\d")   # ASCII hyphen used as a math minus
L_LITERAL = re.compile(r"""L\(\s*(["'])(.*?)\1""")


def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def main():
    issues = []

    # 1) CSS uniformity
    for src in CSS_SOURCES:
        p = os.path.join(ROOT, src)
        if not os.path.exists(p):
            issues.append(f"[CSS]  {src}: file missing — cannot verify design tokens")
            continue
        t = rd(p)
        for tok in CSS_TOKENS:
            if tok not in t:
                issues.append(f"[CSS]  {src}: missing canonical token  «{tok[:48]}…»")

    # geometry8/algebra8 engines must stay identical
    a, g = os.path.join(ROOT, "algebra8/wsengine.py"), os.path.join(ROOT, "geometry8/wsengine.py")
    if os.path.exists(a) and os.path.exists(g) and rd(a) != rd(g):
        issues.append("[CSS]  algebra8/wsengine.py and geometry8/wsengine.py have DIVERGED")

    # 2) notation inside content
    for p in CONTENT:
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        t = rd(p)
        if "∢" in t:
            issues.append(f"[SYM]  {rel}: uses ∢ — use ∠ instead")
        for m in L_LITERAL.finditer(t):
            frag = m.group(2)
            ln = t[:m.start()].count("\n") + 1
            for bad, want in BAD_IN_L:
                if bad in frag:
                    issues.append(f"[SYM]  {rel}:{ln}: L(\"…{bad}…\") — use {want}")
            if HYPHEN_MINUS.search(frag):
                issues.append(f"[SYM]  {rel}:{ln}: L(\"{frag[:30]}\") uses ASCII '-' as minus — use − (U+2212)")

    # 3) optional card-height check
    if "--heights" in sys.argv:
        try:
            from playwright.sync_api import sync_playwright
            import pathlib
            checked = []
            with sync_playwright() as pw:
                b = pw.chromium.launch()
                for s in ["uncertainty", "algebra", "algebra8", "geometry8"]:
                    f = os.path.join(ROOT, s, "worksheet.html")
                    if not os.path.exists(f):
                        # worksheet.html is a gitignored build intermediate — its
                        # absence means heights were NOT verified, so say so loudly
                        # instead of passing in silence.
                        print(f"(heights NOT checked for {s}: {s}/worksheet.html missing — run the build first)")
                        continue
                    checked.append(s)
                    pg = b.new_page(viewport={"width": 703, "height": 1000})
                    pg.emulate_media(media="print")
                    pg.goto(pathlib.Path(f).resolve().as_uri())
                    hs = pg.evaluate("()=>[...document.querySelectorAll('.q')].map(q=>q.getBoundingClientRect().height/3.779528)")
                    # A4 content height is 263mm, but a card also carries ~6mm of
                    # margin and needs slack so page-break-inside:avoid keeps it
                    # whole. Empirically a ~254mm card still split across pages, so
                    # flag anything above 250mm as a page-overflow risk.
                    over = [round(h) for h in hs if h > 250]
                    if over:
                        issues.append(f"[FIT]  {s}: {len(over)} card(s) > 250mm (page-split risk): {over}")
                    pg.close()
                b.close()
            if checked:
                print(f"(heights verified for: {', '.join(checked)})")
            else:
                issues.append("[FIT]  --heights verified nothing (no worksheet.html found — run the build first)")
        except Exception as e:
            issues.append(f"[FIT]  --heights could not run ({e}) — heights NOT verified")

    if issues:
        print("UNIFORMITY ISSUES (%d):" % len(issues))
        for i in issues:
            print("  " + i)
        return 1
    print("OK — fonts, CSS tokens and math notation are uniform across all subjects.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
