# -*- coding: utf-8 -*-
"""SVG chart helpers for the worksheet generator. Clean, print-quality, RTL-aware."""

PAL = ["#4f46e5", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"]
GRID = "#e6e8ee"
AXIS = "#1f2a44"
INK = "#1f2a44"
SUB = "#334155"
FONT = "font-family:'Segoe UI',Arial,sans-serif;"


def _ticks(ymax, ystep):
    t, v = [], 0.0
    while v <= ymax + 1e-9:
        t.append(round(v, 4))
        v += ystep
    return t


def _num(v):
    # No thousands separator: commas inside SVG <text> get mangled under RTL bidi.
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def vbar(cats, vals, ymax, ystep, ytitle="", xtitle="", colors=None,
         W=620, H=360, value_labels=True, barw_ratio=0.5, sticks=False):
    """Vertical bar / stick chart. cats & vals given left->right. vals may contain None (blank)."""
    ml, mr, mt, mb = 64, 22, 26, 58
    pw, ph = W - ml - mr, H - mt - mb
    n = len(cats)
    slot = pw / n
    bw = slot * (0.10 if sticks else barw_ratio)

    def xc(i):
        return ml + slot * (i + 0.5)

    def y(v):
        return mt + ph - (v / ymax) * ph

    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for t in _ticks(ymax, ystep):
        yy = round(y(t), 2)
        s.append(f'<line x1="{ml}" y1="{yy}" x2="{ml+pw}" y2="{yy}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{ml-9}" y="{yy+4}" text-anchor="end" fill="{SUB}" font-size="13" style="{FONT}">{_num(t)}</text>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    # tick marks on both axes, textbook style
    for t in _ticks(ymax, ystep):
        yy = round(y(t), 2)
        s.append(f'<line x1="{ml-5}" y1="{yy}" x2="{ml}" y2="{yy}" stroke="{AXIS}" stroke-width="1.6"/>')
    for i in range(n):
        s.append(f'<line x1="{xc(i):.1f}" y1="{mt+ph}" x2="{xc(i):.1f}" y2="{mt+ph+5}" stroke="{AXIS}" stroke-width="1.6"/>')
    for i, v in enumerate(vals):
        if v is None:
            continue
        col = (colors[i] if isinstance(colors, list) else colors) if colors else PAL[0]
        yy = y(v)
        if sticks:
            cx = xc(i)
            s.append(f'<line x1="{cx:.1f}" y1="{mt+ph}" x2="{cx:.1f}" y2="{yy:.1f}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
            s.append(f'<circle cx="{cx:.1f}" cy="{yy:.1f}" r="5" fill="{col}"/>')
        else:
            x0 = xc(i) - bw / 2
            s.append(f'<rect x="{x0:.1f}" y="{yy:.1f}" width="{bw:.1f}" height="{(mt+ph-yy):.1f}" rx="3" fill="{col}"/>')
        if value_labels:
            s.append(f'<text x="{xc(i):.1f}" y="{yy-7:.1f}" text-anchor="middle" fill="{INK}" font-size="13" font-weight="600" style="{FONT}">{_num(v)}</text>')
    for i, c in enumerate(cats):
        s.append(f'<text x="{xc(i):.1f}" y="{mt+ph+20}" text-anchor="middle" fill="{INK}" font-size="13.5" style="{FONT}">{c}</text>')
    if xtitle:
        s.append(f'<text x="{ml+pw/2:.1f}" y="{H-8}" text-anchor="middle" fill="{SUB}" font-size="13.5" font-weight="600" style="{FONT}">{xtitle}</text>')
    if ytitle:
        yc = mt + ph / 2
        s.append(f'<text x="16" y="{yc:.1f}" text-anchor="middle" fill="{SUB}" font-size="13.5" font-weight="600" transform="rotate(-90 16 {yc:.1f})" style="{FONT}">{ytitle}</text>')
    s.append("</svg>")
    return "".join(s)


def grouped_bar(cats, series, ymax, ystep, ytitle="", xtitle="", W=770, H=400):
    """series: list of dicts {name,color,vals(list aligned to cats, None to skip)}"""
    ml, mr, mt, mb = 66, 180, 30, 60
    pw, ph = W - ml - mr, H - mt - mb
    n = len(cats)
    slot = pw / n
    k = len(series)
    gap = slot * 0.18
    bw = (slot - gap) / k

    def y(v):
        return mt + ph - (v / ymax) * ph

    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for t in _ticks(ymax, ystep):
        yy = round(y(t), 2)
        s.append(f'<line x1="{ml}" y1="{yy}" x2="{ml+pw}" y2="{yy}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{ml-9}" y="{yy+4}" text-anchor="end" fill="{SUB}" font-size="12.5" style="{FONT}">{_num(t)}</text>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    for i in range(n):
        base = ml + slot * i + gap / 2
        for j, ser in enumerate(series):
            v = ser["vals"][i]
            if v is None:
                continue
            x0 = base + j * bw
            yy = y(v)
            stroke = ' stroke="#9aa3b2" stroke-width="0.8"' if ser["color"].lower() in ("#ffffff", "#fff", "white") else ""
            s.append(f'<rect x="{x0:.1f}" y="{yy:.1f}" width="{bw-1.5:.1f}" height="{(mt+ph-yy):.1f}" fill="{ser["color"]}"{stroke}/>')
        s.append(f'<text x="{ml+slot*(i+0.5):.1f}" y="{mt+ph+19}" text-anchor="middle" fill="{INK}" font-size="13" style="{FONT}">{cats[i]}</text>')
    # legend (RTL: swatch on the right, label flows left)
    sx = W - 30
    ly = mt + 6
    for ser in series:
        stroke = ' stroke="#9aa3b2" stroke-width="0.8"' if ser["color"].lower() in ("#ffffff", "#fff", "white") else ""
        s.append(f'<rect x="{sx}" y="{ly}" width="15" height="15" fill="{ser["color"]}"{stroke}/>')
        s.append(f'<text x="{sx-8}" y="{ly+12}" text-anchor="start" fill="{INK}" font-size="13" style="{FONT}">{ser["name"]}</text>')
        ly += 26
    if xtitle:
        s.append(f'<text x="{ml+pw/2:.1f}" y="{H-6}" text-anchor="middle" fill="{SUB}" font-size="13" font-weight="600" style="{FONT}">{xtitle}</text>')
    if ytitle:
        yc = mt + ph / 2
        s.append(f'<text x="16" y="{yc:.1f}" text-anchor="middle" fill="{SUB}" font-size="13" font-weight="600" transform="rotate(-90 16 {yc:.1f})" style="{FONT}">{ytitle}</text>')
    s.append("</svg>")
    return "".join(s)


import math


def pie(segments, W=480, H=330, r=108, title="", show_pct=True):
    """segments: list of (label, value, color). Clockwise from top. Shows % and legend."""
    has_labels = any(lab for lab, _, _ in segments)
    if not has_labels:
        cx, cy = W / 2, H / 2 + (8 if title else 0)
    else:
        cx, cy = 128, H / 2 + (8 if title else 0)
    total = sum(v for _, v, _ in segments)
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    if title:
        s.append(f'<text x="{W/2:.0f}" y="20" text-anchor="middle" fill="{INK}" font-size="14" font-weight="700" style="{FONT}">{title}</text>')
    ang = -90.0
    for label, v, col in segments:
        sweep = v / total * 360.0
        a0 = math.radians(ang)
        a1 = math.radians(ang + sweep)
        x0 = cx + r * math.cos(a0); y0 = cy + r * math.sin(a0)
        x1 = cx + r * math.cos(a1); y1 = cy + r * math.sin(a1)
        large = 1 if sweep > 180 else 0
        s.append(f'<path d="M{cx:.1f},{cy:.1f} L{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 1 {x1:.2f},{y1:.2f} Z" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
        if show_pct:
            mid = math.radians(ang + sweep / 2)
            lr = r * 0.62
            lx = cx + lr * math.cos(mid); ly = cy + lr * math.sin(mid)
            pct = v / total * 100
            pct_s = (f"{pct:.0f}%" if abs(pct - round(pct)) < 0.5 else f"{pct:.1f}%")
            s.append(f'<text x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle" fill="#ffffff" font-size="14" font-weight="700" style="{FONT}">{pct_s}</text>')
        ang += sweep
    # legend (RTL: swatch on the right, label flows left)
    if has_labels:
        sx = W - 34
        ly = cy - len(segments) * 13
        for label, v, col in segments:
            s.append(f'<rect x="{sx}" y="{ly}" width="15" height="15" rx="2" fill="{col}"/>')
            s.append(f'<text x="{sx-8}" y="{ly+12.5}" text-anchor="start" fill="{INK}" font-size="13" style="{FONT}">{label}</text>')
            ly += 26
    s.append("</svg>")
    return "".join(s)


def empty_pie(sectors=10, W=300, H=240, r=105):
    cx, cy = W / 2, H / 2
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fbfbfe" stroke="{INK}" stroke-width="2"/>')
    for i in range(sectors):
        a = math.radians(-90 + i * 360 / sectors)
        x1 = cx + r * math.cos(a); y1 = cy + r * math.sin(a)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="#7c86a0" stroke-width="1.4"/>')
    s.append("</svg>")
    return "".join(s)


def spinner(sectors=8, W=260, H=240, r=100):
    cx, cy = W / 2, H / 2
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fbfbfe" stroke="{INK}" stroke-width="6"/>')
    for i in range(sectors):
        a = math.radians(i * 360 / sectors)
        x1 = cx + (r - 12) * math.cos(a); y1 = cy + (r - 12) * math.sin(a)
        x2 = cx + r * math.cos(a); y2 = cy + r * math.sin(a)
        s.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="2"/>')
    # pointer
    a = math.radians(-32)
    px = cx + (r - 22) * math.cos(a); py = cy + (r - 22) * math.sin(a)
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<polygon points="{px:.1f},{py:.1f} {px-10:.1f},{py-4:.1f} {px-4:.1f},{py+9:.1f}" fill="{INK}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{INK}"/>')
    s.append("</svg>")
    return "".join(s)


def scatter(points, xtitle="", ytitle="", W=460, H=340):
    """points: list of (xfrac0to1, yfrac0to1, label)."""
    ml, mr, mt, mb = 40, 30, 24, 44
    pw, ph = W - ml - mr, H - mt - mb
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    ax = ml
    ay = mt + ph
    # axes with arrows
    s.append(f'<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{AXIS}"/></marker></defs>')
    s.append(f'<line x1="{ax}" y1="{ay}" x2="{ax+pw}" y2="{ay}" stroke="{AXIS}" stroke-width="2" marker-end="url(#arr)"/>')
    s.append(f'<line x1="{ax}" y1="{ay}" x2="{ax}" y2="{mt}" stroke="{AXIS}" stroke-width="2" marker-end="url(#arr)"/>')
    for xf, yf, lab in points:
        x = ax + 12 + xf * (pw - 30)
        y = ay - 12 - yf * (ph - 22)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{PAL[0]}"/>')
        s.append(f'<text x="{x+9:.1f}" y="{y-7:.1f}" fill="{INK}" font-size="14" font-weight="700" style="{FONT}">{lab}</text>')
    if xtitle:
        s.append(f'<text x="{ax+pw/2:.0f}" y="{H-8}" text-anchor="middle" fill="{SUB}" font-size="13" style="{FONT}">{xtitle}</text>')
    if ytitle:
        yc = mt + ph / 2
        s.append(f'<text x="14" y="{yc:.0f}" text-anchor="middle" fill="{SUB}" font-size="13" transform="rotate(-90 14 {yc:.0f})" style="{FONT}">{ytitle}</text>')
    s.append("</svg>")
    return "".join(s)


def line_chart(xlabels, yvals, ymin, ymax, ystep, ytitle="", xtitle="", color="#ef4444",
               W=640, H=360, threshold=None, threshold_label="", value_labels=True):
    ml, mr, mt, mb = 64, 22, 26, 56
    pw, ph = W - ml - mr, H - mt - mb
    n = len(xlabels)

    def xc(i):
        return ml + (pw) * (i / (n - 1)) if n > 1 else ml + pw / 2

    def y(v):
        return mt + ph - ((v - ymin) / (ymax - ymin)) * ph

    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for t in _ticks(ymax, ystep):
        if t < ymin - 1e-9:
            continue
        yy = round(y(t), 2)
        s.append(f'<line x1="{ml}" y1="{yy}" x2="{ml+pw}" y2="{yy}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{ml-9}" y="{yy+4}" text-anchor="end" fill="{SUB}" font-size="12.5" style="{FONT}">{_num(t)}</text>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    # tick marks on both axes, textbook style
    for t in _ticks(ymax, ystep):
        if t < ymin - 1e-9:
            continue
        yy = round(y(t), 2)
        s.append(f'<line x1="{ml-5}" y1="{yy}" x2="{ml}" y2="{yy}" stroke="{AXIS}" stroke-width="1.6"/>')
    for i in range(n):
        s.append(f'<line x1="{xc(i):.1f}" y1="{mt+ph}" x2="{xc(i):.1f}" y2="{mt+ph+5}" stroke="{AXIS}" stroke-width="1.6"/>')
    if threshold is not None:
        yy = y(threshold)
        s.append(f'<line x1="{ml}" y1="{yy:.1f}" x2="{ml+pw}" y2="{yy:.1f}" stroke="#ef4444" stroke-width="1.6" stroke-dasharray="6 4"/>')
        if threshold_label:
            s.append(f'<text x="{ml+pw-4}" y="{yy-6:.1f}" text-anchor="end" fill="#ef4444" font-size="12.5" style="{FONT}">{threshold_label}</text>')
    pts = " ".join(f"{xc(i):.1f},{y(v):.1f}" for i, v in enumerate(yvals))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="3"/>')
    for i, v in enumerate(yvals):
        s.append(f'<circle cx="{xc(i):.1f}" cy="{y(v):.1f}" r="5" fill="{color}"/>')
        if value_labels:
            s.append(f'<text x="{xc(i):.1f}" y="{y(v)-10:.1f}" text-anchor="middle" fill="{INK}" font-size="12.5" font-weight="600" style="{FONT}">{_num(v)}</text>')
    for i, lab in enumerate(xlabels):
        s.append(f'<text x="{xc(i):.1f}" y="{mt+ph+19}" text-anchor="middle" fill="{INK}" font-size="13" style="{FONT}">{lab}</text>')
    if xtitle:
        s.append(f'<text x="{ml+pw/2:.0f}" y="{H-6}" text-anchor="middle" fill="{SUB}" font-size="13" font-weight="600" style="{FONT}">{xtitle}</text>')
    if ytitle:
        yc = mt + ph / 2
        s.append(f'<text x="15" y="{yc:.0f}" text-anchor="middle" fill="{SUB}" font-size="13" font-weight="600" transform="rotate(-90 15 {yc:.0f})" style="{FONT}">{ytitle}</text>')
    s.append("</svg>")
    return "".join(s)


def hbar(cats, vals, vmax, vstep, color=None, W=600, H=300, xtitle=""):
    """Horizontal bars. cats top->bottom. Labels on the right, bars extend left."""
    ml, mr, mt, mb = 28, 120, 22, 48
    pw, ph = W - ml - mr, H - mt - mb
    n = len(cats)
    slot = ph / n
    bh = slot * 0.55
    rightx = ml + pw

    def x(v):
        return rightx - (v / vmax) * pw

    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for t in _ticks(vmax, vstep):
        xx = round(x(t), 1)
        s.append(f'<line x1="{xx}" y1="{mt}" x2="{xx}" y2="{mt+ph}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{xx}" y="{mt+ph+18}" text-anchor="middle" fill="{SUB}" font-size="12" style="{FONT}">{_num(t)}</text>')
    s.append(f'<line x1="{rightx}" y1="{mt}" x2="{rightx}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    for i, (c, v) in enumerate(zip(cats, vals)):
        cy = mt + slot * (i + 0.5)
        col = (color[i] if isinstance(color, list) else color) if color else PAL[0]
        s.append(f'<rect x="{x(v):.1f}" y="{cy-bh/2:.1f}" width="{(rightx-x(v)):.1f}" height="{bh:.1f}" rx="3" fill="{col}"/>')
        s.append(f'<text x="{rightx+10}" y="{cy+5:.1f}" fill="{INK}" font-size="13.5" style="{FONT}">{c}</text>')
        s.append(f'<text x="{x(v)-8:.1f}" y="{cy+5:.1f}" text-anchor="end" fill="{INK}" font-size="13" font-weight="600" style="{FONT}">{_num(v)}</text>')
    if xtitle:
        s.append(f'<text x="{ml+pw/2:.0f}" y="{H-6}" text-anchor="middle" fill="{SUB}" font-size="13" style="{FONT}">{xtitle}</text>')
    s.append("</svg>")
    return "".join(s)


def bar3d(cats, vals, ymin, ymax, ystep, colors, ytitle="", W=460, H=340, depth=16):
    """Misleading 3D-ish bars with a possibly truncated y-axis (ymin>0)."""
    ml, mr, mt, mb = 60, 24, 24, 50
    pw, ph = W - ml - mr, H - mt - mb
    n = len(cats)
    slot = pw / n
    bw = slot * 0.42

    def y(v):
        return mt + ph - ((v - ymin) / (ymax - ymin)) * ph

    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for t in _ticks(ymax, ystep):
        if t < ymin - 1e-9:
            continue
        yy = round(y(t), 1)
        s.append(f'<line x1="{ml}" y1="{yy}" x2="{ml+pw}" y2="{yy}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{ml-8}" y="{yy+4}" text-anchor="end" fill="{SUB}" font-size="12.5" style="{FONT}">{_num(t)}%</text>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="{AXIS}" stroke-width="2"/>')
    for i, (c, v) in enumerate(zip(cats, vals)):
        x0 = ml + slot * (i + 0.5) - bw / 2
        yy = y(v)
        col = colors[i]
        # darker side/top for 3d
        s.append(f'<polygon points="{x0:.1f},{yy:.1f} {x0+depth:.1f},{yy-depth:.1f} {x0+bw+depth:.1f},{yy-depth:.1f} {x0+bw:.1f},{yy:.1f}" fill="{col}" fill-opacity="0.75"/>')
        s.append(f'<polygon points="{x0+bw:.1f},{yy:.1f} {x0+bw+depth:.1f},{yy-depth:.1f} {x0+bw+depth:.1f},{mt+ph-depth:.1f} {x0+bw:.1f},{mt+ph:.1f}" fill="{col}" fill-opacity="0.55"/>')
        s.append(f'<rect x="{x0:.1f}" y="{yy:.1f}" width="{bw:.1f}" height="{(mt+ph-yy):.1f}" fill="{col}"/>')
        s.append(f'<text x="{x0+bw/2+depth/2:.1f}" y="{yy-depth-6:.1f}" text-anchor="middle" fill="{INK}" font-size="13" font-weight="700" style="{FONT}">{v}%</text>')
        s.append(f'<text x="{ml+slot*(i+0.5):.1f}" y="{mt+ph+19}" text-anchor="middle" fill="{INK}" font-size="13.5" style="{FONT}">{c}</text>')
    if ytitle:
        yc = mt + ph / 2
        s.append(f'<text x="15" y="{yc:.0f}" text-anchor="middle" fill="{SUB}" font-size="12.5" transform="rotate(-90 15 {yc:.0f})" style="{FONT}">{ytitle}</text>')
    s.append("</svg>")
    return "".join(s)


def _book(cx, cy, w, h, color):
    """A clean open-book glyph centred at (cx,cy)."""
    hw, hh = w / 2, h / 2
    top = cy - hh * 0.55
    bot = cy + hh * 0.50
    spine_b = cy + hh * 0.30
    left = f'M{cx:.1f},{top:.1f} L{cx-hw:.1f},{cy-hh*0.12:.1f} L{cx-hw:.1f},{bot:.1f} L{cx:.1f},{spine_b:.1f} Z'
    right = f'M{cx:.1f},{top:.1f} L{cx+hw:.1f},{cy-hh*0.12:.1f} L{cx+hw:.1f},{bot:.1f} L{cx:.1f},{spine_b:.1f} Z'
    return (f'<path d="{left}" fill="{color}" stroke="{color}" stroke-width="0.8" stroke-linejoin="round"/>'
            f'<path d="{right}" fill="{color}" fill-opacity="0.72" stroke="{color}" stroke-width="0.8" stroke-linejoin="round"/>'
            f'<line x1="{cx:.1f}" y1="{top:.1f}" x2="{cx:.1f}" y2="{spine_b:.1f}" stroke="#ffffff" stroke-width="1.1"/>'
            f'<line x1="{cx-hw*0.55:.1f}" y1="{cy-hh*0.02:.1f}" x2="{cx-hw*0.55:.1f}" y2="{bot-1:.1f}" stroke="#ffffff" stroke-width="0.6" opacity="0.7"/>'
            f'<line x1="{cx+hw*0.55:.1f}" y1="{cy-hh*0.02:.1f}" x2="{cx+hw*0.55:.1f}" y2="{bot-1:.1f}" stroke="#ffffff" stroke-width="0.6" opacity="0.7"/>')


def color_wheel(segments, W=370, H=232, r=82, pointer_deg=-45):
    """Spinner / color wheel with a tidy side legend. segments: (label, degrees, color), clockwise from top."""
    cx, cy = W - r - 24, H / 2
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    a = -90.0
    for label, deg, col in segments:
        a0 = math.radians(a); a1 = math.radians(a + deg)
        x0 = cx + r * math.cos(a0); y0 = cy + r * math.sin(a0)
        x1 = cx + r * math.cos(a1); y1 = cy + r * math.sin(a1)
        large = 1 if deg > 180 else 0
        s.append(f'<path d="M{cx:.1f},{cy:.1f} L{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 1 {x1:.2f},{y1:.2f} Z" '
                 f'fill="{col}" stroke="#ffffff" stroke-width="2"/>')
        a += deg
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    pa = math.radians(pointer_deg); pr = r * 0.78
    px = cx + pr * math.cos(pa); py = cy + pr * math.sin(pa)
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    bx, by = px - 13 * math.cos(pa - 0.4), py - 13 * math.sin(pa - 0.4)
    ex, ey = px - 13 * math.cos(pa + 0.4), py - 13 * math.sin(pa + 0.4)
    s.append(f'<polygon points="{px:.1f},{py:.1f} {bx:.1f},{by:.1f} {ex:.1f},{ey:.1f}" fill="{INK}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="{INK}"/>')
    # legend on the left (RTL: swatch on the right of each row, name flows left)
    sx = cx - r - 26
    y = cy - len(segments) * 12 + 6
    for label, deg, col in segments:
        s.append(f'<rect x="{sx}" y="{y-11:.0f}" width="15" height="15" rx="3" fill="{col}"/>')
        s.append(f'<text x="{sx-8}" y="{y+1:.0f}" text-anchor="start" fill="{INK}" font-size="13.5" style="{FONT}">{label}</text>')
        y += 24
    s.append("</svg>")
    return "".join(s)


def pictograph(cats, counts, color="#0d9488", W=640, H=330):
    """Clean vector pictograph: columns of book icons. cats & counts given left->right."""
    ml, mr, mt, mb = 24, 24, 44, 52
    pw, ph = W - ml - mr, H - mt - mb
    n = len(cats)
    slot = pw / n
    maxc = max(counts)
    cellh = ph / maxc
    iconh = min(cellh * 0.86, 32)
    iconw = min(slot * 0.62, iconh * 1.25)
    base = mt + ph
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    # legend (RTL: book on the right, label flows left)
    bx = W - 30
    s.append(_book(bx, 16, iconw * 0.8, iconh * 0.8, color))
    s.append(f'<text x="{bx-14}" y="21" text-anchor="start" fill="{SUB}" font-size="13" style="{FONT}">= תלמיד אחד</text>')
    for i, (c, cnt) in enumerate(zip(cats, counts)):
        cx = ml + slot * (i + 0.5)
        for k in range(cnt):
            cy = base - cellh * (k + 0.5)
            s.append(_book(cx, cy, iconw, iconh, color))
        s.append(f'<text x="{cx:.1f}" y="{base+20}" text-anchor="middle" fill="{INK}" font-size="13" style="{FONT}">{c}</text>')
    s.append(f'<line x1="{ml}" y1="{base}" x2="{ml+pw}" y2="{base}" stroke="{AXIS}" stroke-width="2"/>')
    s.append("</svg>")
    return "".join(s)
