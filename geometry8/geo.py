# -*- coding: utf-8 -*-
"""Minimal vector-geometry SVG helpers — clean, uniform diagrams for the
geometry booklet (triangles, medians, rectangles, congruence/similarity marks)."""

INK = "#1f2a44"
ACC = "#4f46e5"
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


def label(p, text, dx=0, dy=0, size=14, col=INK, anchor="middle"):
    return (f'<text x="{p[0]+dx:.1f}" y="{p[1]+dy:.1f}" text-anchor="{anchor}" '
            f'fill="{col}" font-size="{size}" font-weight="700" style="{FONT}">{text}</text>')


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
