# -*- coding: utf-8 -*-
"""Minimal vector-geometry SVG helpers — clean, uniform diagrams for the
geometry booklet (triangles, medians, rectangles, congruence/similarity marks)."""

INK = "#1f2a44"
ACC = "#4f46e5"
SUB = "#5b6573"
FONT = "font-family:'Segoe UI',Arial,sans-serif;"


def _svg(w, h, body):
    return f'<svg class="chart" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def seg(a, b, col=INK, wd=2.0, dash=False):
    d = ' stroke-dasharray="6 4"' if dash else ""
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{wd}"{d}/>'


def poly(pts, col=INK, wd=2.0, fill="none"):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" stroke="{col}" stroke-width="{wd}"/>'


def dot(p, r=3.0, col=INK):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{col}"/>'


def label(p, text, dx=0, dy=0, size=14, col=INK, anchor="middle", halo=True):
    """Text label. By default a white knockout halo is painted behind the glyphs
    (paint-order:stroke) so the label stays crisp wherever it sits — over a
    gridline, an axis or a curve. Textbook-grade legibility, applied everywhere
    so future figures inherit it and can't regress. Pass halo=False to disable."""
    h = (f' paint-order="stroke" stroke="#ffffff" stroke-width="{max(2.5, size * 0.26):.1f}"'
         f' stroke-linejoin="round"') if halo else ""
    return (f'<text x="{p[0]+dx:.1f}" y="{p[1]+dy:.1f}" text-anchor="{anchor}" '
            f'fill="{col}" font-size="{size}" font-weight="700" style="{FONT}"{h}>{text}</text>')


def vertex(p, name, dx=0, dy=0, anchor="middle"):
    """Dot + vertex label."""
    return dot(p) + label(p, name, dx, dy, anchor=anchor)


def tick(a, b, n=1, col=INK):
    """n small tick marks at the midpoint of segment a-b (equal-length marks)."""
    import math
    mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
    dx, dy = b[0]-a[0], b[1]-a[1]
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx/ln, dy/ln          # along
    px, py = -uy, ux               # perpendicular
    out = []
    for i in range(n):
        off = (i - (n-1)/2) * 5
        cx, cy = mx + ux*off, my + uy*off
        out.append(f'<line x1="{cx-px*5:.1f}" y1="{cy-py*5:.1f}" x2="{cx+px*5:.1f}" y2="{cy+py*5:.1f}" stroke="{col}" stroke-width="1.8"/>')
    return "".join(out)


def right_angle(corner, a, b, size=12, col=INK):
    """Small square at `corner` between directions to a and b."""
    import math
    def u(p):
        dx, dy = p[0]-corner[0], p[1]-corner[1]
        ln = math.hypot(dx, dy) or 1
        return dx/ln, dy/ln
    ax, ay = u(a); bx, by = u(b)
    p1 = (corner[0]+ax*size, corner[1]+ay*size)
    p2 = (corner[0]+ax*size+bx*size, corner[1]+ay*size+by*size)
    p3 = (corner[0]+bx*size, corner[1]+by*size)
    return f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="{col}" stroke-width="1.5"/>'


def arc(center, a, b, r=20, col=INK, text="", tdx=0, tdy=0):
    """Angle arc at `center` from ray->a to ray->b, optional label."""
    import math
    def ang(p): return math.atan2(p[1]-center[1], p[0]-center[0])
    a0, a1 = ang(a), ang(b)
    d = (a1 - a0) % (2*math.pi)
    if d > math.pi:                      # always draw the interior (minor) arc
        a0, a1 = a1, a0
        d = 2*math.pi - d
    x0, y0 = center[0]+r*math.cos(a0), center[1]+r*math.sin(a0)
    x1, y1 = center[0]+r*math.cos(a1), center[1]+r*math.sin(a1)
    s = f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{col}" stroke-width="1.6"/>'
    if text:
        mid = (a0 + d/2)
        tx, ty = center[0]+(r+11)*math.cos(mid), center[1]+(r+11)*math.sin(mid)
        s += label((tx, ty), text, tdx, tdy, size=12, col=col)
    return s


# ---- topic-2 (median) reconstructed figures ----
def median_tri():
    A, B, C, D = (150, 18), (28, 130), (272, 130), (150, 130)
    b = poly([A, B, C]) + seg(A, D)
    b += tick(B, D) + tick(D, C)
    b += vertex(A, "A", 0, -7) + vertex(B, "B", -9, 4) + vertex(C, "C", 9, 4) + vertex(D, "D", 0, 16)
    return _svg(300, 150, b)


def rect_median():
    A, B, C, D, E = (35, 25), (215, 25), (215, 185), (35, 185), (215, 105)
    b = poly([A, B, C, D]) + seg(A, C) + seg(A, E)
    b += tick(B, E) + tick(E, C)
    b += vertex(A, "A", -9, -4) + vertex(B, "B", 9, -4) + vertex(C, "C", 10, 14) + vertex(D, "D", -9, 14) + vertex(E, "E", 12, 4)
    return _svg(250, 210, b)


def rect_bisector():
    A, B, C, D, E = (35, 25), (215, 25), (215, 185), (35, 185), (215, 92)
    b = poly([A, B, C, D]) + seg(A, C) + seg(A, E)
    b += arc(A, B, E, r=22, text="α") + arc(A, E, C, r=30, text="α")
    b += vertex(A, "A", -9, -4) + vertex(B, "B", 9, -4) + vertex(C, "C", 10, 14) + vertex(D, "D", -9, 14) + vertex(E, "E", 12, 4)
    return _svg(250, 210, b)


def inh_reuven():
    A, B, C = (160, 18), (300, 150), (20, 150)
    R, Q, P = (90, 150), (160, 150), (230, 150)
    b = poly([A, B, C]) + seg(A, P) + seg(A, Q) + seg(A, R)
    for s in [(C, R), (R, Q), (Q, P), (P, B)]:
        b += tick(*s)
    b += vertex(A, "A", 0, -7) + vertex(B, "B", 9, 4) + vertex(C, "C", -9, 4)
    b += vertex(P, "P", 0, 16) + vertex(Q, "Q", 0, 16) + vertex(R, "R", 0, 16)
    return _svg(320, 170, b)


def inh_shimon():
    A, B, C, T, S = (160, 18), (300, 150), (20, 150), (160, 150), (160, 84)
    b = poly([A, B, C]) + seg(A, T) + seg(S, B) + seg(S, C)
    b += tick(C, T) + tick(T, B) + tick(A, S) + tick(S, T)
    b += vertex(A, "A", 0, -7) + vertex(B, "B", 9, 4) + vertex(C, "C", -9, 4)
    b += vertex(T, "T", 0, 16) + vertex(S, "S", -10, 4)
    return _svg(320, 175, b)


def inh_levi():
    A, B, C, D = (160, 18), (300, 140), (20, 140), (160, 140)
    E, F = (90, 79), (230, 79)
    b = poly([A, B, C]) + seg(A, D) + seg(D, E) + seg(D, F)
    b += right_angle(D, A, C, size=10)
    b += vertex(A, "A", 0, -7) + vertex(B, "B", 9, 4) + vertex(C, "C", -9, 4)
    b += vertex(D, "D", 0, 16) + vertex(E, "E", -10, -2) + vertex(F, "F", 10, -2)
    return _svg(320, 160, b)


def inh_yehuda():
    A, B, C = (160, 18), (20, 140), (300, 140)
    F, E, D = (90, 79), (230, 79), (160, 140)
    b = poly([A, B, C]) + poly([D, E, F], col=ACC)
    for s in [(A, F), (F, B), (A, E), (E, C), (B, D), (D, C)]:
        b += tick(*s)
    b += vertex(A, "A", 0, -7) + vertex(B, "B", -9, 4) + vertex(C, "C", 9, 4)
    b += vertex(F, "F", -10, -2) + vertex(E, "E", 10, -2) + vertex(D, "D", 0, 16)
    return _svg(320, 160, b)


# ---- topic-3 (congruence) reconstructed figures ----
def _tri_pair(marks):
    """Two congruent triangles side by side. marks: dict with optional
    'sides':[(idx,n)], 'angles':[(vertex,n)] applied to BOTH triangles.
    Triangle vertices indexed 0=A(top),1=B(left),2=C(right)."""
    import math
    L = [(62, 22), (20, 128), (128, 128)]
    R = [(250, 22), (208, 128), (316, 128)]
    b = poly(L) + poly(R)
    side_pts = {0: (0, 1), 1: (0, 2), 2: (1, 2)}   # AB, AC, BC
    for idx, n in marks.get("sides", []):
        i, j = side_pts[idx]
        b += tick(L[i], L[j], n) + tick(R[i], R[j], n)
    arcr = {0: 16, 1: 22, 2: 28}
    for v, n in marks.get("angles", []):
        others = [k for k in (0, 1, 2) if k != v]
        for T in (L, R):
            b += arc(T[v], T[others[0]], T[others[1]], r=arcr.get(n, 18))
            if n == 2:
                b += arc(T[v], T[others[0]], T[others[1]], r=arcr[n]+5)
    names = ["A", "B", "C"]
    off = [(0, -7), (-9, 6), (9, 6)]
    for T in (L, R):
        for k in range(3):
            b += vertex(T[k], names[k] if T is L else names[k]+"'", off[k][0], off[k][1])
    return _svg(340, 150, b)


def cong_sas():
    return _tri_pair({"sides": [(0, 1), (1, 2)], "angles": [(0, 1)]})   # AB,AC + ∠A


def cong_asa():
    return _tri_pair({"sides": [(2, 1)], "angles": [(1, 1), (2, 2)]})   # BC + ∠B,∠C


def cong_sss():
    return _tri_pair({"sides": [(0, 1), (1, 2), (2, 3)]})               # AB,AC,BC


def isosceles_ext():
    A, B, C, D = (120, 20), (40, 140), (200, 140), (280, 140)
    b = poly([A, B, C]) + seg(C, D) + seg(A, D)
    b += tick(A, B) + tick(A, C)
    b += vertex(A, "A", 0, -7) + vertex(B, "B", -9, 6) + vertex(C, "C", 0, 16) + vertex(D, "D", 9, 6)
    return _svg(320, 165, b)


def x_segments():
    A, C = (30, 28), (250, 150)
    B, D = (30, 150), (250, 28)
    M = (140, 89)
    b = seg(A, C) + seg(B, D) + seg(A, B) + seg(C, D)
    b += tick(A, M) + tick(M, C) + tick(B, M, 2) + tick(M, D, 2)
    b += vertex(A, "A", -9, 0) + vertex(B, "B", -9, 6) + vertex(C, "C", 9, 6) + vertex(D, "D", 9, 0) + vertex(M, "M", 0, -8)
    return _svg(290, 175, b)


def cong_plain():
    return _tri_pair({})


# ---- topic-4 (similarity) reconstructed figures ----
def palm_shadow():
    g = 150
    b = seg((10, g), (330, g))                       # ground
    # person (small right triangle)
    # both right triangles share the SAME acute angle (sun rays parallel):
    # height/shadow = 1.72/2.15 = 9.6/12 = 0.8 for both.
    P0, P1, Ptop = (40, g), (120, g), (120, g - 64)      # 80 x 64  (ratio 0.8)
    b += seg(P0, P1) + seg(P1, Ptop) + seg(P0, Ptop) + right_angle(P1, P0, Ptop, size=9)
    b += label(((P0[0]+P1[0])/2, g+14), "2.15 מ'", size=11)
    b += label((P1[0]+24, (g+Ptop[1])/2), "1.72 מ'", size=11)
    # palm (large right triangle, same base angle): 155 x 124 (ratio 0.8)
    Q0, Q1, Qtop = (165, g), (320, g), (320, g - 124)
    b += seg(Q0, Q1) + seg(Q1, Qtop) + seg(Q0, Qtop) + right_angle(Q1, Q0, Qtop, size=9)
    b += label(((Q0[0]+Q1[0])/2, g+14), "12 מ'", size=11)
    b += label((Q1[0]-22, (g+Qtop[1])/2), "x = ?", size=11, col=ACC)
    return _svg(340, 172, b)


def square_in_tri():
    # isosceles right triangle: apex A = 90deg, base angles 45deg at C,B.
    # true inscribed square, side s = base*height/(base+height) = 200*100/300.
    A, C, B = (120, 70), (20, 170), (220, 170)
    s2 = (200*100/300) / 2          # half the square side ≈ 33.3
    S = (120 - s2, 170); R = (120 + s2, 170)
    Q = (120 + s2, 170 - 2*s2); P = (120 - s2, 170 - 2*s2)
    b = poly([A, C, B]) + poly([P, Q, R, S], col=ACC)
    b += right_angle(A, C, B, size=10)
    b += arc(C, B, A, r=24, text="45°", tdx=2) + arc(B, A, C, r=24, text="45°", tdx=-2)
    b += vertex(A, "A", 0, -7) + vertex(C, "C", -9, 6) + vertex(B, "B", 9, 6)
    b += vertex(P, "P", -9, -2) + vertex(Q, "Q", 9, -2) + vertex(R, "R", 9, 14) + vertex(S, "S", -9, 14)
    return _svg(240, 190, b)


def rect_38():
    A, B, C, D = (24, 16), (184, 16), (184, 92), (24, 92)
    b = poly([A, B, C, D])
    b += label(((A[0]+B[0])/2, A[1]-6), "8 ס\"מ", size=12)
    b += label((A[0]-8, (A[1]+D[1])/2+4), "3 ס\"מ", size=12, anchor="end")
    b += vertex(A, "A", -8, -3) + vertex(B, "B", 8, -3) + vertex(C, "C", 8, 14) + vertex(D, "D", -8, 14)
    return _svg(210, 110, b)


def drone_cone():
    # proportions match the data: height:base = 20:16 = 1.25 (148 px : 118 px).
    K, M = (120, 14), (120, 162)
    L, R = (61, 162), (179, 162)
    b = poly([K, L, R]) + seg(K, M, dash=True) + right_angle(M, R, K, size=8)
    b += label((K[0]+38, (K[1]+M[1])/2), "20 מ'", size=11)
    b += label(((L[0]+R[0])/2, M[1]+15), "16 מ'", size=11)
    b += vertex(K, "K", 0, -7)
    return _svg(240, 182, b)


# ---- topic-1 (circle) reconstructed coordinate figure ----
def circle_diameter():
    """Coordinate circle with horizontal diameter AB: A(-3,0), B(7,0) → centre (2,0), r=5.
    Clean vector: faint grid, arrowed axes, labelled points."""
    ml, mt, u = 26, 16, 18                 # unit = 18 px/grid-square
    # 2-unit headroom beyond the circle (x∈[-3,7], y∈[-5,5]) so the axis arrows,
    # the x/y labels and the A/B labels never collide with the curve.
    xmin, xmax, ymin, ymax = -6, 10, -7, 7
    def X(x): return ml + (x - xmin) * u
    def Y(y): return mt + (ymax - y) * u
    W = ml + (xmax - xmin) * u + 22
    H = mt + (ymax - ymin) * u + 16
    GRID = "#e7eaf1"
    s = [f'<svg class="chart" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    # faint grid
    for gx in range(xmin, xmax + 1):
        s.append(f'<line x1="{X(gx):.0f}" y1="{Y(ymax):.0f}" x2="{X(gx):.0f}" y2="{Y(ymin):.0f}" stroke="{GRID}" stroke-width="1"/>')
    for gy in range(ymin, ymax + 1):
        s.append(f'<line x1="{X(xmin):.0f}" y1="{Y(gy):.0f}" x2="{X(xmax):.0f}" y2="{Y(gy):.0f}" stroke="{GRID}" stroke-width="1"/>')
    # axes + arrowheads
    y0, x0 = Y(0), X(0)
    s.append(f'<line x1="{X(xmin):.0f}" y1="{y0:.0f}" x2="{X(xmax):.0f}" y2="{y0:.0f}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<line x1="{x0:.0f}" y1="{Y(ymin):.0f}" x2="{x0:.0f}" y2="{Y(ymax):.0f}" stroke="{INK}" stroke-width="1.6"/>')
    s.append(f'<path d="M{X(xmax):.0f},{y0:.0f} l-8,-4 l0,8 z" fill="{INK}"/>')
    s.append(f'<path d="M{x0:.0f},{Y(ymax):.0f} l-4,8 l8,0 z" fill="{INK}"/>')
    s.append(label((x0 - 6, Y(0) + 13), "O", anchor="end", size=12, col=SUB))
    s.append(label((X(xmax) - 2, y0 - 7), "x", anchor="end", size=13, col=INK))
    s.append(label((x0 + 8, Y(ymax) + 11), "y", anchor="start", size=13, col=INK))
    # circle  (centre (2,0), r=5)
    s.append(f'<circle cx="{X(2):.0f}" cy="{Y(0):.0f}" r="{5*u}" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    # diameter AB + endpoints + centre
    s.append(seg((X(-3), Y(0)), (X(7), Y(0)), wd=2.2))
    s.append(dot((X(-3), Y(0))) + dot((X(7), Y(0))) + dot((X(2), Y(0)), r=2.6))
    s.append(label((X(-3), Y(0) + 18), "A(−3,0)", size=12.5))
    s.append(label((X(7), Y(0) + 18), "B(7,0)", size=12.5))
    s.append("</svg>")
    return "".join(s)


# ---- topic-1 (circle/area/solid) reconstructed figures ----
def hexagon_in_circle():
    import math
    cx, cy, R = 135, 120, 95
    pts = [(cx + R*math.cos(math.radians(a)), cy - R*math.sin(math.radians(a))) for a in range(0, 360, 60)]
    b = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += poly(pts, col=ACC, wd=2)
    b += seg((cx, cy), pts[0]) + seg((cx, cy), pts[1])   # two radii → one triangle
    b += dot((cx, cy), r=2.6) + label((cx-6, cy-7), "O", anchor="end", size=12, col=SUB)
    midr = ((cx+pts[0][0])/2, (cx and (cy+pts[0][1])/2))
    b += label(((cx+pts[0][0])/2, cy-8), "1", size=12, col=SUB)
    return _svg(280, 245, b)


def circle_in_square():
    A, B, C, D = (35, 25), (215, 25), (215, 205), (35, 205)
    cx, cy, r = 125, 115, 90
    b = poly([A, B, C, D]) + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACC}" stroke-width="2"/>'
    b += seg((cx, cy), (cx+r, cy), col=SUB, wd=1.6) + dot((cx, cy), r=2.4)
    b += label((cx+r/2, cy-6), "6", size=12, col=SUB)
    b += vertex(A, "A", -9, -4) + vertex(B, "B", 9, -4) + vertex(C, "C", 9, 14) + vertex(D, "D", -9, 14)
    return _svg(250, 232, b)


def stadium():
    # square (area 144 → side 12) with a semicircle on left and right
    x0, y0, s = 90, 40, 130
    r = s/2
    b = f'<rect x="{x0}" y="{y0}" width="{s}" height="{s}" fill="none" stroke="{INK}" stroke-width="2"/>'
    cyl = y0 + r
    b += f'<path d="M{x0},{y0} A{r},{r} 0 0 0 {x0},{y0+s}" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += f'<path d="M{x0+s},{y0} A{r},{r} 0 0 1 {x0+s},{y0+s}" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += label((x0+s/2, cyl+5), "144 מ\"ר", size=13, col=SUB)
    b += label((x0+s/2, y0-8), "12 מ'", size=11, col=SUB)
    return _svg(90+s+90, s+80, b)


def cone():
    # inverted cone (ice-cream): rim ellipse on top, apex at bottom; r=6, slant=10, h=?
    cx, topY, botY = 140, 50, 240
    rx, ry = 92, 24
    b = f'<ellipse cx="{cx}" cy="{topY}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += seg((cx-rx, topY), (cx, botY)) + seg((cx+rx, topY), (cx, botY))   # slant sides
    b += seg((cx, topY), (cx, botY), col=SUB, wd=1.4, dash=True)            # height
    b += seg((cx, topY), (cx+rx, topY), col=SUB, wd=1.4)                    # top radius
    b += right_angle((cx, topY), (cx+rx, topY), (cx, botY), size=10, col=SUB)
    b += label((cx+rx/2, topY-8), "r = 6", size=12, col=SUB)
    b += label((cx+52, (topY+botY)/2+20), "10 ס\"מ", size=12, col=SUB)
    b += label((cx-12, (topY+botY)/2), "h = ?", size=12, col=SUB, anchor="end")
    b += label((cx, topY-30), "קוטר = 12 ס\"מ", size=11, col=SUB)
    return _svg(290, 270, b)


def two_circles_rect():
    # rectangle ABCD with two tangent circles (r=5) inscribed side by side
    A, B, C, D = (20, 20), (260, 20), (260, 140), (20, 140)
    P, Q, r = (80, 80), (200, 80), 60
    b = poly([A, B, C, D])
    b += f'<circle cx="{P[0]}" cy="{P[1]}" r="{r}" fill="none" stroke="{ACC}" stroke-width="2"/>'
    b += f'<circle cx="{Q[0]}" cy="{Q[1]}" r="{r}" fill="none" stroke="{ACC}" stroke-width="2"/>'
    b += seg(P, (P[0]+r, P[1]), col=SUB, wd=1.5) + dot(P, 2.4) + dot(Q, 2.4)
    b += label((P[0]+r/2, P[1]-5), "5", size=12, col=SUB)
    b += label((P[0], P[1]+16), "P", size=12, col=SUB) + label((Q[0], Q[1]+16), "Q", size=12, col=SUB)
    b += vertex(A, "A", -9, -4) + vertex(B, "B", 9, -4) + vertex(C, "C", 9, 14) + vertex(D, "D", -9, 14)
    return _svg(290, 162, b)


def shapes_ab():
    # rect 20x12; ב' = rectangle with a semicircular notch; א' = rectangle with a bump (r=6)
    rw, rh, r = 110, 66, 33
    yt, yb = 34, 34+rh
    # shape ב' (left): notch cut into the left side
    bx = 30
    b = f'<path d="M{bx},{yt} H{bx+rw} V{yb} H{bx} A{r},{r} 0 0 0 {bx},{yt} Z" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += label((bx+rw/2, yt-7), "20 ס\"מ", size=10.5, col=SUB)
    b += label((bx+rw+7, (yt+yb)/2+4), "12", size=10.5, col=SUB, anchor="start")
    b += label((bx+rw/2, yb+22), "צורה ב'", size=12)
    # shape א' (right): semicircle bump added on the left side
    ax = 250
    b += f'<path d="M{ax},{yt} A{r},{r} 0 0 0 {ax},{yb} H{ax+rw} V{yt} Z" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += label((ax+rw/2, yt-7), "20 ס\"מ", size=10.5, col=SUB)
    b += label((ax+rw+7, (yt+yb)/2+4), "12", size=10.5, col=SUB, anchor="start")
    b += label((ax+rw/2, yb+22), "צורה א'", size=12)
    return _svg(250+rw+30, yb+34, b)


def _cyl(cx, rx, topY, botY, ry=15, col=INK):
    s = f'<ellipse cx="{cx}" cy="{topY}" rx="{rx}" ry="{ry}" fill="none" stroke="{col}" stroke-width="2"/>'
    s += seg((cx-rx, topY), (cx-rx, botY), col=col) + seg((cx+rx, topY), (cx+rx, botY), col=col)
    s += f'<path d="M{cx-rx},{botY} A{rx},{ry} 0 0 0 {cx+rx},{botY}" fill="none" stroke="{col}" stroke-width="2"/>'
    s += f'<path d="M{cx-rx},{botY} A{rx},{ry} 0 0 1 {cx+rx},{botY}" fill="none" stroke="{col}" stroke-width="1.1" stroke-dasharray="4 3"/>'
    return s


def cylinders_pair():
    b = ""
    # cylinder א : r = 3
    cxA, rxA = 78, 40
    b += _cyl(cxA, rxA, 36, 150)
    b += seg((cxA, 36), (cxA+rxA, 36), col=SUB, wd=1.3) + label((cxA+rxA/2, 30), "r=3", size=11, col=SUB)
    b += label((cxA, 172), "א'", size=13, col=SUB)
    # cylinder ב : r = 5, h = 8, axial rectangle ABCD (area 60)
    cxB, rxB, topB, botB = 250, 56, 36, 150
    b += _cyl(cxB, rxB, topB, botB)
    A, Bp, C, D = (cxB-rxB, topB), (cxB+rxB, topB), (cxB+rxB, botB), (cxB-rxB, botB)
    b += seg(A, D, col=ACC, wd=1.6) + seg(Bp, C, col=ACC, wd=1.6)
    b += label((A[0]-8, A[1]+2), "A", size=11) + label((Bp[0]+8, Bp[1]+2), "B", size=11)
    b += label((C[0]+8, C[1]+6), "C", size=11) + label((D[0]-8, D[1]+6), "D", size=11)
    b += label((cxB+rxB+12, (topB+botB)/2+4), "h=8", size=11, col=SUB, anchor="start")
    b += label((cxB, 172), "ב'", size=13, col=SUB)
    return _svg(340, 186, b)


# ---- topic-2 (angles) reconstructed line diagrams ----
RED, BLU, GRN = "#ef4444", "#2563eb", "#0d9488"


def _isect(a, b, c, d):
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))


def t2_fig_q2():           # △ABC, D on extension of BC, AB∥EC, ∠A=65°, ∠ECD=40°, α=∠BCA
    B, C, D, A = (48, 152), (168, 152), (288, 152), (110, 52)
    E = (168 + (110-48), 152 - (152-52))     # CE ∥ AB
    b = seg(A, B) + seg(B, D) + seg(A, C) + seg(C, E)
    b += arc(A, B, C, r=22, text="65°")
    b += arc(C, E, D, r=20, text="40°")
    b += arc(C, B, A, r=30, text="α")
    b += vertex(A, "A", 0, -7) + vertex(B, "B", -9, 6) + vertex(C, "C", 0, 16) + vertex(D, "D", 9, 6) + vertex(E, "E", 9, -2)
    return _svg(320, 180, b)


def t2_fig_q5():           # ∠A=50°(bisected 25°), ∠C=30° (∠BCE=150°), α=∠B=100°
    A, B, C, D, E = (45, 150), (110, 72), (245, 150), (156, 98), (290, 150)
    b = seg(A, B) + seg(B, C) + seg(C, A) + seg(A, D) + seg(C, E)
    b += arc(A, D, C, r=26, text="25°")
    b += arc(C, B, E, r=24, text="150°")
    b += arc(B, A, C, r=20, text="α")
    b += vertex(A, "A", -9, 6) + vertex(B, "B", 0, -7) + vertex(C, "C", 0, 16) + vertex(D, "D", 9, -2) + vertex(E, "E", 9, 6)
    return _svg(320, 178, b)


def t2_fig_q3km():         # k∥m, A,D on k; B,C on m; x and 55° at A, y at B
    k0, k1 = (40, 48), (296, 48)
    m0, m1 = (40, 168), (296, 168)
    A, D, B, C = (150, 48), (258, 48), (108, 168), (212, 168)
    b = seg(k0, k1) + seg(m0, m1) + seg(A, B) + seg(A, C)
    b += arc(A, k0, B, r=20, text="x")
    b += arc(A, D, C, r=26, text="55°")
    b += arc(B, A, m0, r=20, text="y")
    b += label((30, 52), "k", size=13) + label((30, 172), "m", size=13)
    b += vertex(A, "A", 0, -7) + vertex(D, "D", 9, -4) + vertex(B, "B", -2, 16) + vertex(C, "C", 2, 16)
    return _svg(320, 195, b)


def t2_fig_2tri():         # B,E,C,F collinear; △ABC & △DEF; G=AC∩DE; ∠B=40°, ∠F=60°
    B, E, C, F = (45, 158), (118, 158), (215, 158), (292, 158)
    A, D = (135, 52), (228, 58)
    G = _isect(A, C, D, E)
    b = seg(A, B) + seg(A, C) + seg(D, E) + seg(D, F) + seg(B, F)
    b += arc(B, A, F, r=22, text="40°")
    b += arc(F, D, B, r=22, text="60°")
    b += dot(G, 2.6) + label((G[0]+2, G[1]-7), "G", size=12)
    b += vertex(A, "A", -2, -7) + vertex(B, "B", -2, 16) + vertex(E, "E", 0, 16)
    b += vertex(C, "C", 0, 16) + vertex(F, "F", 6, 16) + vertex(D, "D", 6, -5)
    return _svg(320, 178, b)


def _cross4(P, ll, lr, tu, td, labs, cols, r=20):
    """4 angle arcs around a crossing P. ll/lr = line left/right pts, tu/td = transversal up/down pts.
    labs/cols = [top, right, bottom, left] (between tu&lr, lr&td, td&ll, ll&tu)."""
    quads = [(tu, lr), (lr, td), (td, ll), (ll, tu)]
    s = ""
    for (a, c), lab, col in zip(quads, labs, cols):
        if lab:
            s += arc(P, a, c, r=r, text=lab, col=col)
    return s


def t2_fig_8angles():      # two parallels + 1 transversal, α/β at top, α1/β1 at bottom
    l1a, l1b = (45, 78), (302, 50)
    l2a, l2b = (45, 172), (302, 144)
    ta, tb = (108, 24), (236, 198)
    P1 = _isect(ta, tb, l1a, l1b)
    P2 = _isect(ta, tb, l2a, l2b)
    b = seg(l1a, l1b) + seg(l2a, l2b) + seg(ta, tb)
    b += arc(P1, l1b, ta, r=20, text="β", col=BLU)
    b += arc(P1, l1a, tb, r=20, text="α", col=RED)
    b += arc(P2, l2b, ta, r=20, text="α₁", col=RED)
    b += arc(P2, l2a, tb, r=20, text="β₁", col=BLU)
    return _svg(330, 210, b)


def t2_fig_islands():      # two parallels + transversal, 4 corresponding angles each crossing
    l1a, l1b = (45, 70), (302, 46)
    l2a, l2b = (45, 168), (302, 144)
    ta, tb = (120, 22), (250, 196)
    P1 = _isect(ta, tb, l1a, l1b)
    P2 = _isect(ta, tb, l2a, l2b)
    b = seg(l1a, l1b) + seg(l2a, l2b) + seg(ta, tb)
    b += _cross4(P1, l1a, l1b, ta, tb, ["δ", "γ", "β", "α"], ["#1f2a44", BLU, RED, GRN])
    b += _cross4(P2, l2a, l2b, ta, tb, ["δ₁", "γ₁", "β₁", "α₁"], ["#1f2a44", BLU, RED, GRN])
    return _svg(330, 210, b)


def t2_fig_ext():          # right △ABC (right angle B), D on AC, 56° at D, 22° at C, α at B, β at A
    A, B, C = (70, 40), (70, 208), (290, 208)
    D = (215, 150)          # on AC
    b = seg(A, B) + seg(B, C) + seg(C, A) + seg(B, D)
    b += right_angle(B, A, C, size=11)
    b += arc(D, B, C, r=22, text="56°")
    b += arc(C, B, A, r=24, text="22°")
    b += arc(B, D, C, r=22, text="α")
    b += arc(A, B, C, r=22, text="β")
    b += vertex(A, "A", -2, -7) + vertex(B, "B", -9, 6) + vertex(C, "C", 9, 6) + vertex(D, "D", 10, 0)
    return _svg(330, 235, b)


# ---- topic-1 complex figures reconstructed ----
FILLB = "#cfe8f3"


def yin_shaded():
    # circle split into two equal areas by an S-curve of two half-radius semicircles
    cx, cy, R = 140, 132, 104
    h = R/2
    shaded = (f'<path d="M{cx},{cy-R} A{R},{R} 0 0 1 {cx},{cy+R} '
              f'A{h},{h} 0 0 1 {cx},{cy} A{h},{h} 0 0 0 {cx},{cy-R} Z" fill="{FILLB}" stroke="none"/>')
    out = shaded
    out += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{INK}" stroke-width="2"/>'
    out += (f'<path d="M{cx},{cy-R} A{h},{h} 0 0 1 {cx},{cy} A{h},{h} 0 0 0 {cx},{cy+R}" '
            f'fill="none" stroke="{INK}" stroke-width="2"/>')
    return _svg(280, 268, out)


def _arrow_arc(cx, cy, r, a0, a1, col=INK):
    import math
    x0, y0 = cx+r*math.cos(math.radians(a0)), cy+r*math.sin(math.radians(a0))
    x1, y1 = cx+r*math.cos(math.radians(a1)), cy+r*math.sin(math.radians(a1))
    large = 1 if abs(a1-a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    s = f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}" fill="none" stroke="{col}" stroke-width="3"/>'
    # arrowhead at (x1,y1)
    ang = math.radians(a1) + (math.pi/2 if sweep else -math.pi/2)
    s += (f'<path d="M{x1:.1f},{y1:.1f} l{7*math.cos(ang-2.6):.1f},{7*math.sin(ang-2.6):.1f} '
          f'l{7*math.cos(ang+2.6):.1f},{7*math.sin(ang+2.6):.1f} z" fill="{col}"/>')
    return s


def paper_roll():
    def sheet(x, y, w, h):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{FILLB}" fill-opacity="0.5" stroke="{INK}" stroke-width="1.8"/>'
    b = ""
    # (א) roll by width — arrows wrap the left & right vertical edges
    x1, y1, w, h = 40, 55, 90, 130
    b += sheet(x1, y1, w, h)
    b += _arrow_arc(x1, y1+h/2, 26, -60, 60)
    b += _arrow_arc(x1+w, y1+h/2, 26, 120, 240)
    b += label((x1+w/2, y1-12), "(א) לפי הרוחב", size=12)
    # (ב) roll by length — arrows wrap the top & bottom edges
    x2 = 230
    b += sheet(x2, y1, w, h)
    b += _arrow_arc(x2+w/2, y1, 24, 30, 150)
    b += _arrow_arc(x2+w/2, y1+h, 24, 210, 330)
    b += label((x2+w/2, y1-12), "(ב) לפי האורך", size=12)
    return _svg(360, 215, b)
