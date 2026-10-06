"""Generate and store the remaining 46 figures (making all 89 figures complete).

Full coverage of figures 1 to 89 in Kiselev's Geometry (1931) with NUSH didactic annotations.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import drawsvg as draw

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from geometry_engine.db import BookDatabase, BookFigure  # noqa: E402

BOOK_ID = "kiselev_geometry_1931"

BG_COLOR = "#f8fafc"
TEXT_COLOR = "#0f172a"
LINE_COLOR = "#1e293b"
BLUE_PRIMARY = "#2563eb"
GREEN_EQUAL = "#16a34a"
RED_AUX = "#dc2626"
PURPLE_AUX = "#9333ea"
GRAY_MUTED = "#64748b"


def canvas(w: int = 360, h: int = 200, bg: str = BG_COLOR) -> draw.Drawing:
    d = draw.Drawing(w, h)
    d.append(draw.Rectangle(0, 0, w, h, fill=bg, rx=8, stroke="#e2e8f0", stroke_width=1))
    return d


def pt(
    d: draw.Drawing,
    x: float,
    y: float,
    name: str = "",
    pos: str = "top",
    color: str = TEXT_COLOR,
    r: float = 3.5,
):
    d.append(draw.Circle(x, y, r, fill=color))
    if name:
        ox, oy = x, y
        if pos == "top":
            oy -= 8
            anchor = "middle"
        elif pos == "bottom":
            oy += 18
            anchor = "middle"
        elif pos == "left":
            ox -= 9
            oy += 5
            anchor = "end"
        elif pos == "right":
            ox += 9
            oy += 5
            anchor = "start"
        elif pos == "top-left":
            ox -= 8
            oy -= 7
            anchor = "end"
        elif pos == "top-right":
            ox += 8
            oy -= 7
            anchor = "start"
        elif pos == "bottom-left":
            ox -= 8
            oy += 16
            anchor = "end"
        elif pos == "bottom-right":
            ox += 8
            oy += 16
            anchor = "start"
        else:
            oy -= 8
            anchor = "middle"
        d.append(
            draw.Text(
                name,
                14,
                ox,
                oy,
                fill=color,
                font_weight="bold",
                text_anchor=anchor,
                font_style="italic",
            )
        )


def seg(
    d: draw.Drawing,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = LINE_COLOR,
    w: float = 2.0,
    dashed: bool = False,
):
    kw = {"stroke_dasharray": "5,4"} if dashed else {}
    d.append(draw.Line(x1, y1, x2, y2, stroke=color, stroke_width=w, **kw))


def arc_deg(
    d: draw.Drawing,
    cx: float,
    cy: float,
    r: float,
    a1_deg: float,
    a2_deg: float,
    color: str = BLUE_PRIMARY,
    w: float = 1.8,
    dashed: bool = False,
):
    kw = {"stroke_dasharray": "4,3"} if dashed else {}
    d.append(draw.Arc(cx, cy, r, -a2_deg, -a1_deg, stroke=color, stroke_width=w, fill="none", **kw))


def right_sym(
    d: draw.Drawing,
    ox: float,
    oy: float,
    ang_deg: float = 0,
    sz: float = 12,
    color: str = GREEN_EQUAL,
):
    r1 = math.radians(ang_deg)
    r2 = math.radians(ang_deg + 90)
    p1x, p1y = ox + sz * math.cos(r1), oy - sz * math.sin(r1)
    p2x, p2y = (
        ox + sz * (math.cos(r1) + math.cos(r2)),
        oy - sz * (math.sin(r1) + math.sin(r2)),
    )
    p3x, p3y = ox + sz * math.cos(r2), oy - sz * math.sin(r2)
    d.append(
        draw.Lines(ox, oy, p1x, p1y, p2x, p2y, p3x, p3y, ox, oy, fill="#dcfce7", stroke="none")
    )
    d.append(draw.Lines(p1x, p1y, p2x, p2y, p3x, p3y, fill="none", stroke=color, stroke_width=1.5))


def tick(
    d: draw.Drawing,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    count: int = 1,
    color: str = GREEN_EQUAL,
):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1e-4:
        return
    nx, ny = -dy / L, dx / L
    ux, uy = dx / L, dy / L
    tick_sz = 5
    offsets = [-3, 3] if count == 2 else ([-4, 0, 4] if count == 3 else [0])
    for off in offsets:
        px, py = mx + ux * off, my + uy * off
        d.append(
            draw.Line(
                px - nx * tick_sz,
                py - ny * tick_sz,
                px + nx * tick_sz,
                py + ny * tick_sz,
                stroke=color,
                stroke_width=1.5,
            )
        )


# ==============================================================================
# REMAINING 46 GENERATORS
# ==============================================================================


def make_fig_15() -> draw.Drawing:
    d = canvas(360, 220)
    cx, cy, r = 180, 110, 75
    d.append(draw.Circle(cx, cy, r, fill="none", stroke="#cbd5e1", stroke_width=1.5))
    pt(d, cx, cy, "O", "bottom")
    # Angle 1: 0 to 45 deg
    p1x, p1y = cx + r, cy
    p2x, p2y = cx + r * math.cos(math.radians(45)), cy - r * math.sin(math.radians(45))
    seg(d, cx, cy, p1x, p1y, color=BLUE_PRIMARY, w=2)
    seg(d, cx, cy, p2x, p2y, color=BLUE_PRIMARY, w=2)
    pt(d, p1x, p1y, "B", "right")
    pt(d, p2x, p2y, "A", "top-right")
    arc_deg(d, cx, cy, r, 0, 45, color=BLUE_PRIMARY, w=3.5)
    # Angle 2: 120 to 165 deg
    p3x, p3y = cx + r * math.cos(math.radians(120)), cy - r * math.sin(math.radians(120))
    p4x, p4y = cx + r * math.cos(math.radians(165)), cy - r * math.sin(math.radians(165))
    seg(d, cx, cy, p3x, p3y, color=GREEN_EQUAL, w=2)
    seg(d, cx, cy, p4x, p4y, color=GREEN_EQUAL, w=2)
    pt(d, p3x, p3y, "C", "top-left")
    pt(d, p4x, p4y, "D", "left")
    arc_deg(d, cx, cy, r, 120, 165, color=GREEN_EQUAL, w=3.5)
    d.append(
        draw.Text(
            "∠AOB = ∠COD  ⟺  Дуга AB = Дуга CD", 13, 180, 205, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_17() -> draw.Drawing:
    d = canvas(360, 220)
    ox, oy, r = 180, 160, 120
    d.append(draw.Arc(ox, oy, r, -180, 0, stroke=LINE_COLOR, stroke_width=2, fill="#f8fafc"))
    seg(d, ox - r - 10, oy, ox + r + 10, oy, color=LINE_COLOR, w=2)
    pt(d, ox, oy, "O", "bottom")
    # Measured angle: 55 degrees
    rad = math.radians(55)
    rx, ry = ox + r * math.cos(rad), oy - r * math.sin(rad)
    seg(d, ox, oy, rx, ry, color=RED_AUX, w=2.5)
    pt(d, rx, ry, "A (55°)", "top-right", color=RED_AUX)
    arc_deg(d, ox, oy, 40, 0, 55, color=RED_AUX, w=2)
    d.append(
        draw.Text(
            "Вимірювання кута 55° транспортиром", 13, ox, 200, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_20() -> draw.Drawing:
    d = canvas(360, 180)
    ox, oy = 180, 130
    seg(d, 40, oy, 320, oy, color=LINE_COLOR, w=2)
    bx, by = ox + 110 * math.cos(math.radians(50)), oy - 110 * math.sin(math.radians(50))
    seg(d, ox, oy, bx, by, color=BLUE_PRIMARY, w=2.5)
    # Perpendicular OE for proof
    seg(d, ox, oy, ox, oy - 100, color=RED_AUX, w=1.8, dashed=True)
    pt(d, ox, oy, "O", "bottom")
    pt(d, 40, oy, "A", "bottom")
    pt(d, 320, oy, "C", "bottom")
    pt(d, bx, by, "B", "top-right")
    pt(d, ox, oy - 100, "E (90°)", "top", color=RED_AUX)
    right_sym(d, ox, oy, 0, 12, RED_AUX)
    d.append(
        draw.Text(
            "Доведення: ∠AOB + ∠BOC = 2d = 180°", 13, ox, 165, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_21() -> draw.Drawing:
    d = canvas(360, 180)
    ox1, oy = 100, 130
    ox2 = 260
    # Two straight lines
    seg(d, 30, oy, 170, oy, color=LINE_COLOR, w=2)
    seg(d, 190, oy, 330, oy, color=LINE_COLOR, w=2)
    # Equal angles 60 deg
    rad = math.radians(60)
    seg(d, ox1, oy, ox1 + 70 * math.cos(rad), oy - 70 * math.sin(rad), color=BLUE_PRIMARY, w=2)
    seg(d, ox2, oy, ox2 + 70 * math.cos(rad), oy - 70 * math.sin(rad), color=BLUE_PRIMARY, w=2)
    arc_deg(d, ox1, oy, 25, 0, 60, color=BLUE_PRIMARY)
    arc_deg(d, ox2, oy, 25, 0, 60, color=BLUE_PRIMARY)
    arc_deg(d, ox1, oy, 30, 60, 180, color=GREEN_EQUAL)
    arc_deg(d, ox2, oy, 30, 60, 180, color=GREEN_EQUAL)
    d.append(
        draw.Text(
            "Якщо α₁ = α₂, то суміжні β₁ = β₂ = 180° - α",
            13,
            180,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_25() -> draw.Drawing:
    d = canvas(340, 180)
    ox, oy = 170, 130
    seg(d, 40, oy, 300, oy, color=LINE_COLOR, w=2)
    # One angle 3 times the other: 45° and 135°
    rad = math.radians(45)
    bx, by = ox + 110 * math.cos(rad), oy - 110 * math.sin(rad)
    seg(d, ox, oy, bx, by, color=BLUE_PRIMARY, w=2.5)
    pt(d, ox, oy, "O", "bottom")
    arc_deg(d, ox, oy, 30, 0, 45, color=BLUE_PRIMARY)
    arc_deg(d, ox, oy, 35, 45, 180, color=RED_AUX)
    d.append(draw.Text("x", 12, ox + 45, oy - 12, fill=BLUE_PRIMARY, font_weight="bold"))
    d.append(draw.Text("3x", 12, ox - 50, oy - 18, fill=RED_AUX, font_weight="bold"))
    d.append(
        draw.Text(
            "x + 3x = 180°  ⟹  x = 45°",
            13,
            ox,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_26() -> draw.Drawing:
    d = canvas(340, 180)
    ox, oy = 170, 100
    # Two intersecting lines forming vertical angles
    rad = math.radians(40)
    ux, uy = math.cos(rad), math.sin(rad)
    seg(d, ox - 120, oy, ox + 120, oy, color=LINE_COLOR, w=2)
    seg(d, ox - 120 * ux, oy + 120 * uy, ox + 120 * ux, oy - 120 * uy, color=BLUE_PRIMARY, w=2)
    pt(d, ox, oy, "O", "bottom")
    arc_deg(d, ox, oy, 30, 0, 40, color=GREEN_EQUAL)
    arc_deg(d, ox, oy, 30, 180, 220, color=GREEN_EQUAL)
    d.append(
        draw.Text(
            "Пряма, що проходить через вершину кута",
            13,
            ox,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_27() -> draw.Drawing:
    d = canvas(360, 200)
    ox, oy = 180, 100
    rad1, rad2 = math.radians(50), math.radians(-50)
    # Two lines
    seg(
        d,
        ox - 120 * math.cos(rad1),
        oy + 120 * math.sin(rad1),
        ox + 120 * math.cos(rad1),
        oy - 120 * math.sin(rad1),
        color=LINE_COLOR,
        w=2,
    )
    seg(
        d,
        ox - 120 * math.cos(rad2),
        oy + 120 * math.sin(rad2),
        ox + 120 * math.cos(rad2),
        oy - 120 * math.sin(rad2),
        color=LINE_COLOR,
        w=2,
    )
    # Bisector line (horizontal)
    seg(d, ox - 130, oy, ox + 130, oy, color=RED_AUX, w=2.5, dashed=True)
    pt(d, ox, oy, "O", "bottom")
    d.append(
        draw.Text(
            "Бісектриси вертикальних кутів — одна пряма",
            13,
            ox,
            185,
            text_anchor="middle",
            fill=RED_AUX,
            font_weight="bold",
        )
    )
    return d


def make_fig_29() -> draw.Drawing:
    d = canvas(360, 180)
    # Non-convex polygon
    pts = [(80, 140), (80, 60), (160, 100), (240, 50), (260, 140)]
    poly_pts = [c for p in pts for c in p]
    d.append(draw.Lines(*poly_pts, close=True, fill="#fff1f2", stroke=RED_AUX, stroke_width=2))
    # Dashed line showing reflex reflex side
    seg(d, pts[1][0], pts[1][1], pts[3][0], pts[3][1], color=GRAY_MUTED, w=1.5, dashed=True)
    for i, (x, y) in enumerate(pts):
        pt(d, x, y, f"A_{i + 1}", "top" if y < 90 else "bottom")
    d.append(
        draw.Text(
            "Неопуклий (увігнутий) многокутник", 13, 180, 168, text_anchor="middle", fill=RED_AUX
        )
    )
    return d


def make_fig_30() -> draw.Drawing:
    d = canvas(360, 160)
    # Perimeter unfolding
    seg(d, 30, 90, 330, 90, color=BLUE_PRIMARY, w=3)
    xs = [30, 90, 160, 240, 330]
    names = ["A", "B", "C", "D", "A"]
    for x, name in zip(xs, names, strict=True):
        pt(d, x, 90, name, "bottom")
    d.append(
        draw.Text(
            "Периметр P = AB + BC + CD + DA",
            13,
            180,
            45,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_32() -> draw.Drawing:
    d = canvas(320, 180)
    ax, ay = 60, 140
    bx, by = 260, 140
    cx, cy = 60, 40
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#f0fdf4", stroke=LINE_COLOR, stroke_width=2
        )
    )
    right_sym(d, ax, ay, 0, 12, GREEN_EQUAL)
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, bx, by, "B", "bottom-right")
    pt(d, cx, cy, "C", "top-left")
    d.append(
        draw.Text(
            "Прямокутний різносторонній трикутник",
            12,
            160,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_33() -> draw.Drawing:
    d = canvas(340, 180)
    ax, ay = 120, 130
    bx, by = 300, 130
    cx, cy = 40, 60
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#fef2f2", stroke=LINE_COLOR, stroke_width=2
        )
    )
    arc_deg(d, ax, ay, 25, 0, 140, color=RED_AUX)
    pt(d, ax, ay, "A (>90°)", "bottom")
    pt(d, bx, by, "B", "bottom-right")
    pt(d, cx, cy, "C", "top")
    d.append(draw.Text("Тупокутний трикутник", 13, 170, 165, text_anchor="middle", fill=RED_AUX))
    return d


def make_fig_34() -> draw.Drawing:
    d = canvas(340, 180)
    # Isosceles obtuse
    bx, by = 170, 60
    ax, ay = 60, 130
    cx, cy = 280, 130
    d.append(
        draw.Lines(
            ax, ay, cx, cy, bx, by, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    tick(d, ax, ay, bx, by, 1, BLUE_PRIMARY)
    tick(d, cx, cy, bx, by, 1, BLUE_PRIMARY)
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, cx, cy, "C", "bottom-right")
    pt(d, bx, by, "B", "top")
    d.append(
        draw.Text(
            "Рівнобедрений тупокутний трикутник (AB = BC)",
            12,
            170,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_35() -> draw.Drawing:
    d = canvas(320, 190)
    s = 90
    ox, oy = 160, 140
    p1 = (ox - s / 2, oy)
    p2 = (ox + s / 2, oy)
    p3 = (ox, oy - s * 0.866)
    d.append(
        draw.Lines(
            p1[0],
            p1[1],
            p2[0],
            p2[1],
            p3[0],
            p3[1],
            close=True,
            fill="#f0fdf4",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    tick(d, p1[0], p1[1], p2[0], p2[1], 1, GREEN_EQUAL)
    tick(d, p1[0], p1[1], p3[0], p3[1], 1, GREEN_EQUAL)
    tick(d, p2[0], p2[1], p3[0], p3[1], 1, GREEN_EQUAL)
    pt(d, p1[0], p1[1], "A", "bottom-left")
    pt(d, p2[0], p2[1], "B", "bottom-right")
    pt(d, p3[0], p3[1], "C", "top")
    d.append(
        draw.Text(
            "Рівносторонній трикутник (всі кути по 60°)",
            12,
            160,
            170,
            text_anchor="middle",
            fill=GREEN_EQUAL,
            font_weight="bold",
        )
    )
    return d


def make_fig_38() -> draw.Drawing:
    d = canvas(340, 180)
    ax, ay = 50, 140
    bx, by = 290, 140
    cx, cy = 130, 40
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#f8fafc", stroke=LINE_COLOR, stroke_width=2
        )
    )
    mx, my = (ax + bx) / 2, ay
    seg(d, cx, cy, mx, my, color=BLUE_PRIMARY, w=2.5)
    tick(d, ax, ay, mx, my, 1, GREEN_EQUAL)
    tick(d, mx, my, bx, by, 1, GREEN_EQUAL)
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, bx, by, "B", "bottom-right")
    pt(d, cx, cy, "C", "top")
    pt(d, mx, my, "M", "bottom", color=BLUE_PRIMARY)
    d.append(
        draw.Text(
            "CM — медіана (AM = MB)",
            13,
            170,
            165,
            text_anchor="middle",
            fill=BLUE_PRIMARY,
            font_weight="bold",
        )
    )
    return d


def make_fig_40() -> draw.Drawing:
    d = canvas(340, 200)
    ax, ay = 60, 150
    cx, cy = 280, 150
    bx, by = 170, 40
    d.append(
        draw.Lines(
            ax, ay, cx, cy, bx, by, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    dx, dy = (ax + cx) / 2, ay
    seg(d, bx, by, dx, dy, color=RED_AUX, w=2, dashed=True)
    arc_deg(d, ax, ay, 25, 0, 50, color=GREEN_EQUAL)
    arc_deg(d, cx, cy, 25, 130, 180, color=GREEN_EQUAL)
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, cx, cy, "C", "bottom-right")
    pt(d, bx, by, "B", "top")
    pt(d, dx, dy, "D", "bottom")
    d.append(
        draw.Text(
            "Доведення: накладання △ABD на △CBD ⟹ ∠A = ∠C",
            12,
            170,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_41() -> draw.Drawing:
    d = canvas(340, 200)
    ax, ay = 60, 150
    cx, cy = 280, 150
    bx, by = 170, 35
    d.append(
        draw.Lines(
            ax, ay, cx, cy, bx, by, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    dx, dy = 170, 150
    seg(d, bx, by - 15, dx, dy + 20, color=RED_AUX, w=2.5, dashed=True)
    pt(d, 110, 95, "M", "top-left", color=BLUE_PRIMARY)
    pt(d, 230, 95, "M'", "top-right", color=BLUE_PRIMARY)
    seg(d, 110, 95, 230, 95, color=BLUE_PRIMARY, w=1.5, dashed=True)
    d.append(
        draw.Text(
            "Дзеркальна симетрія відносно осі BD",
            13,
            170,
            188,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_43_44() -> draw.Drawing:
    d = canvas(360, 180)
    # Superposition step
    p1 = [(40, 130), (140, 130), (70, 45)]
    d.append(
        draw.Lines(
            p1[0][0],
            p1[0][1],
            p1[1][0],
            p1[1][0],
            p1[2][0],
            p1[2][1],
            close=True,
            fill="#f0fdf4",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    pt(d, p1[0][0], p1[0][1], "A=A₁", "bottom-left", color=RED_AUX)
    pt(d, p1[1][0], p1[1][1], "C=C₁", "bottom-right", color=RED_AUX)
    pt(d, p1[2][0], p1[2][1], "B=B₁", "top", color=RED_AUX)
    d.append(
        draw.Text(
            "Суміщення вершини A з A₁ та променя AC з A₁C₁",
            13,
            180,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_46() -> draw.Drawing:
    d = canvas(360, 180)
    p = [(50, 130), (200, 130), (110, 45)]
    d.append(
        draw.Lines(
            p[0][0],
            p[0][1],
            p[1][0],
            p[1][1],
            p[2][0],
            p[2][1],
            close=True,
            fill="#f0fdf4",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    pt(d, p[0][0], p[0][1], "A", "bottom-left")
    pt(d, p[1][0], p[1][1], "C", "bottom-right")
    pt(d, p[2][0], p[2][1], "B", "top")
    arc_deg(d, p[0][0], p[0][1], 25, 0, 60, color=GREEN_EQUAL)
    arc_deg(d, p[1][0], p[1][1], 25, 130, 180, color=RED_AUX)
    d.append(
        draw.Text(
            "Доведення АСА: промені перетинаються в одній точці B",
            12,
            180,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_48_50() -> draw.Drawing:
    d = canvas(360, 220)
    # SSS proof by reflection
    ax, ay = 60, 110
    cx, cy = 300, 110
    bx, by = 160, 30
    b1x, b1y = 160, 190
    d.append(
        draw.Lines(
            ax, ay, cx, cy, bx, by, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    d.append(
        draw.Lines(
            ax, ay, cx, cy, b1x, b1y, close=True, fill="#fdf4ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    seg(d, bx, by, b1x, b1y, color=RED_AUX, w=2, dashed=True)
    pt(d, ax, ay, "A", "left")
    pt(d, cx, cy, "C", "right")
    pt(d, bx, by, "B", "top")
    pt(d, b1x, b1y, "B₁", "bottom")
    d.append(
        draw.Text(
            "Доведення ССС: прикладання △A₁B₁C₁ до △ABC",
            13,
            180,
            210,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_52_53() -> draw.Drawing:
    d = canvas(340, 180)
    ax, ay = 50, 130
    bx, by = 280, 130
    cx, cy = 100, 40
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#fffbeb", stroke=LINE_COLOR, stroke_width=2
        )
    )
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, bx, by, "B", "bottom-right")
    pt(d, cx, cy, "C", "top")
    d.append(
        draw.Text(
            "Проти більшого кута ∠C лежить більша сторона AB",
            12,
            170,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_55_57() -> draw.Drawing:
    d = canvas(360, 180)
    ax, ay = 40, 130
    bx, by = 320, 130
    seg(d, ax, ay, bx, by, color=BLUE_PRIMARY, w=3)
    # Broken line
    p1 = (110, 50)
    p2 = (220, 40)
    d.append(
        draw.Lines(
            ax,
            ay,
            p1[0],
            p1[1],
            p2[0],
            p2[1],
            bx,
            by,
            fill="none",
            stroke=RED_AUX,
            stroke_width=2,
            stroke_dasharray="5,4",
        )
    )
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, bx, by, "B", "bottom-right")
    pt(d, p1[0], p1[1], "C", "top")
    pt(d, p2[0], p2[1], "D", "top")
    d.append(
        draw.Text(
            "Пряма AB < Ламана ACDB",
            13,
            180,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_59_61() -> draw.Drawing:
    d = canvas(360, 200)
    sy = 140
    seg(d, 30, sy, 330, sy, color=LINE_COLOR, w=2)
    px, py = 180, 35
    pt(d, px, py, "P", "top")
    # Perpendicular
    seg(d, px, py, px, sy, color=RED_AUX, w=2.5)
    pt(d, px, sy, "H", "bottom")
    # Oblique 1 and 2
    seg(d, px, py, 80, sy, color=BLUE_PRIMARY, w=2)
    seg(d, px, py, 280, sy, color=GREEN_EQUAL, w=2)
    pt(d, 80, sy, "A", "bottom")
    pt(d, 280, sy, "B", "bottom")
    d.append(
        draw.Text(
            "HA < HB  ⟺  PA < PB (похилі та проекції)",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_62_63() -> draw.Drawing:
    d = canvas(360, 180)
    # Parallel lines distance
    y1, y2 = 50, 130
    seg(d, 40, y1, 320, y1, color=BLUE_PRIMARY, w=2)
    seg(d, 40, y2, 320, y2, color=BLUE_PRIMARY, w=2)
    for x in [100, 180, 260]:
        seg(d, x, y1, x, y2, color=GREEN_EQUAL, w=2)
        right_sym(d, x, y2, 0, 10, GREEN_EQUAL)
    d.append(
        draw.Text(
            "Відстань між паралельними прямими стала",
            13,
            180,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_65() -> draw.Drawing:
    d = canvas(360, 190)
    ox, oy = 50, 150
    ax, ay = ox + 220 * math.cos(math.radians(50)), oy - 220 * math.sin(math.radians(50))
    bx, by = ox + 250, oy
    seg(d, ox, oy, ax, ay, color=LINE_COLOR, w=2)
    seg(d, ox, oy, bx, by, color=LINE_COLOR, w=2)
    # Bisector
    lx, ly = ox + 220 * math.cos(math.radians(25)), oy - 220 * math.sin(math.radians(25))
    seg(d, ox, oy, lx, ly, color=RED_AUX, w=2.5)
    # Point P on bisector
    px, py = ox + 140 * math.cos(math.radians(25)), oy - 140 * math.sin(math.radians(25))
    pt(d, px, py, "P", "top", color=RED_AUX)
    # Perpendiculars from P to sides
    seg(d, px, py, px, oy, color=GREEN_EQUAL, w=1.8, dashed=True)
    right_sym(d, px, oy, 0, 10, GREEN_EQUAL)
    pt(d, ox, oy, "O", "left")
    d.append(
        draw.Text(
            "Бісектриса як ГМТ: точки P рівновіддалені від сторін",
            12,
            180,
            180,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_67() -> draw.Drawing:
    d = canvas(360, 180)
    # Copying an angle
    ox, oy = 50, 140
    seg(d, ox, oy, ox + 110, oy, color=LINE_COLOR, w=2)
    seg(d, ox, oy, ox + 90, 50, color=LINE_COLOR, w=2)
    arc_deg(d, ox, oy, 40, 0, 50, color=GREEN_EQUAL, dashed=True)
    pt(d, ox, oy, "O", "bottom-left")
    o1x, o1y = 200, 140
    seg(d, o1x, o1y, o1x + 110, o1y, color=BLUE_PRIMARY, w=2)
    seg(d, o1x, o1y, o1x + 90, 50, color=BLUE_PRIMARY, w=2)
    arc_deg(d, o1x, o1y, 40, 0, 50, color=GREEN_EQUAL, dashed=True)
    pt(d, o1x, o1y, "O₁", "bottom-left")
    d.append(
        draw.Text(
            "Задача 2: побудова кута, рівного даному",
            13,
            180,
            168,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_68() -> draw.Drawing:
    d = canvas(360, 190)
    ox, oy = 60, 150
    ax, ay = ox + 180 * math.cos(math.radians(50)), oy - 180 * math.sin(math.radians(50))
    seg(d, ox, oy, ax, ay, color=LINE_COLOR, w=2)
    seg(d, ox, oy, ox + 200, oy, color=LINE_COLOR, w=2)
    # Bisector
    bx, by = ox + 190 * math.cos(math.radians(25)), oy - 190 * math.sin(math.radians(25))
    seg(d, ox, oy, bx, by, color=RED_AUX, w=2.5)
    arc_deg(d, ox, oy, 60, 0, 50, color=GREEN_EQUAL, dashed=True)
    pt(d, ox, oy, "O", "left")
    d.append(
        draw.Text(
            "Задача 3: поділ кута навпіл (бісектриса)",
            13,
            180,
            178,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_70() -> draw.Drawing:
    d = canvas(360, 200)
    ax, ay = 60, 100
    bx, by = 300, 100
    seg(d, ax, ay, bx, by, color=LINE_COLOR, w=2.5)
    pt(d, ax, ay, "A", "left")
    pt(d, bx, by, "B", "right")
    # Two intersecting arcs from A and B
    r = 140
    arc_deg(d, ax, ay, r, -40, 40, color=GREEN_EQUAL, dashed=True)
    arc_deg(d, bx, by, r, 140, 220, color=GREEN_EQUAL, dashed=True)
    mx = (ax + bx) / 2
    seg(d, mx, 20, mx, 180, color=RED_AUX, w=2.5)
    pt(d, mx, ay, "M", "bottom-right", color=RED_AUX)
    right_sym(d, mx, ay, 0, 12, RED_AUX)
    d.append(
        draw.Text(
            "Задача 5: поділ відрізка навпіл серединним перпендикуляром",
            12,
            180,
            195,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_71_72() -> draw.Drawing:
    d = canvas(360, 200)
    # Triangle construction analysis
    ax, ay = 60, 150
    bx, by = 280, 150
    cx, cy = 170, 50
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    pt(d, ax, ay, "A", "bottom-left")
    pt(d, bx, by, "B", "bottom-right")
    pt(d, cx, cy, "C", "top")
    d.append(
        draw.Text(
            "Аналіз задач на побудову трикутників",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_74() -> draw.Drawing:
    d = canvas(360, 200)
    y1, y2 = 60, 130
    seg(d, 40, y1, 320, y1, color=BLUE_PRIMARY, w=2)
    seg(d, 40, y2, 320, y2, color=BLUE_PRIMARY, w=2)
    seg(d, 90, 25, 250, 165, color=RED_AUX, w=2)
    d.append(
        draw.Text(
            "Властивості кутів при паралельних прямих і січній",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_76() -> draw.Drawing:
    d = canvas(360, 200)
    y1, y2 = 60, 130
    seg(d, 40, y1, 320, y1, color=BLUE_PRIMARY, w=2)
    seg(d, 40, y2, 320, y2, color=BLUE_PRIMARY, w=2)
    seg(d, 90, 25, 250, 165, color=RED_AUX, w=2)
    arc_deg(d, 125, y1, 20, 0, 45, color=GREEN_EQUAL)
    arc_deg(d, 195, y2, 20, 0, 45, color=GREEN_EQUAL)
    d.append(
        draw.Text(
            "Відповідні кути рівні ⟹ a ∥ b",
            13,
            180,
            185,
            text_anchor="middle",
            fill=GREEN_EQUAL,
            font_weight="bold",
        )
    )
    return d


def make_fig_77() -> draw.Drawing:
    d = canvas(360, 200)
    y1, y2 = 60, 130
    seg(d, 40, y1, 320, y1, color=BLUE_PRIMARY, w=2)
    seg(d, 40, y2, 320, y2, color=BLUE_PRIMARY, w=2)
    seg(d, 90, 25, 250, 165, color=RED_AUX, w=2)
    arc_deg(d, 125, y1, 22, -135, 0, color=RED_AUX)
    arc_deg(d, 195, y2, 22, 0, 45, color=BLUE_PRIMARY)
    d.append(
        draw.Text(
            "Сума внутрішніх односторонніх = 180° ⟹ a ∥ b",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_78() -> draw.Drawing:
    d = canvas(360, 180)
    # Indirect proof: intersecting at K
    kx, ky = 310, 90
    seg(d, 40, 50, kx, ky, color=BLUE_PRIMARY, w=2)
    seg(d, 40, 130, kx, ky, color=BLUE_PRIMARY, w=2)
    seg(d, 100, 20, 100, 160, color=RED_AUX, w=2)
    pt(d, kx, ky, "K (суперечність)", "right", color=RED_AUX)
    d.append(
        draw.Text(
            "Доведення від супротивного: прямі перетинаються в K",
            12,
            160,
            168,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_80() -> draw.Drawing:
    d = canvas(360, 180)
    # Transitivity: a || c and b || c => a || b
    for y, label, col in [(40, "a", BLUE_PRIMARY), (90, "c", GRAY_MUTED), (140, "b", BLUE_PRIMARY)]:
        seg(d, 40, y, 300, y, color=col, w=2.5)
        d.append(draw.Text(label, 14, 315, y + 5, fill=col, font_style="italic"))
    d.append(
        draw.Text(
            "a ∥ c  та  b ∥ c   ⟹   a ∥ b",
            14,
            170,
            172,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_82() -> draw.Drawing:
    d = canvas(360, 200)
    # Parallel opposite directions
    ox1, oy1 = 120, 120
    seg(d, ox1, oy1, ox1 + 100, oy1, color=BLUE_PRIMARY, w=2)
    seg(d, ox1, oy1, ox1 + 60, oy1 - 80, color=BLUE_PRIMARY, w=2)
    arc_deg(d, ox1, oy1, 25, 0, 53, color=BLUE_PRIMARY)
    ox2, oy2 = 240, 120
    seg(d, ox2, oy2, ox2 - 100, oy2, color=RED_AUX, w=2)
    seg(d, ox2, oy2, ox2 + 60, oy2 - 80, color=RED_AUX, w=2)
    arc_deg(d, ox2, oy2, 25, 53, 180, color=RED_AUX)
    d.append(
        draw.Text(
            "Протилежно напрямлені сторони: α + β = 180°",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_84() -> draw.Drawing:
    d = canvas(360, 200)
    ox1, oy1 = 100, 130
    seg(d, ox1, oy1, ox1 + 100, oy1, color=BLUE_PRIMARY, w=2)
    seg(d, ox1, oy1, ox1 + 60, oy1 - 80, color=BLUE_PRIMARY, w=2)
    arc_deg(d, ox1, oy1, 25, 0, 53, color=BLUE_PRIMARY)
    ox2, oy2 = 230, 130
    seg(d, ox2, oy2, ox2, oy2 - 90, color=RED_AUX, w=2)
    seg(d, ox2, oy2, ox2 + 80, oy2 - 40, color=RED_AUX, w=2)
    arc_deg(d, ox2, oy2, 25, -26, 90, color=RED_AUX)
    d.append(
        draw.Text(
            "Перпендикулярні сторони (гострий і тупий): α + β = 180°",
            12,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_88() -> draw.Drawing:
    d = canvas(360, 200)
    pts = [(90, 140), (80, 80), (160, 50), (250, 70), (240, 140)]
    poly_pts = [c for p in pts for c in p]
    d.append(draw.Lines(*poly_pts, close=True, fill="#faf5ff", stroke=LINE_COLOR, stroke_width=2))
    # Extensions for exterior angles
    seg(d, pts[0][0], pts[0][1], pts[0][0] - 40, pts[0][1], color=RED_AUX, w=1.5, dashed=True)
    seg(d, pts[1][0], pts[1][1], pts[1][0], pts[1][1] - 40, color=RED_AUX, w=1.5, dashed=True)
    seg(d, pts[2][0], pts[2][1], pts[2][0] + 40, pts[2][1] - 15, color=RED_AUX, w=1.5, dashed=True)
    seg(d, pts[3][0], pts[3][1], pts[3][0] + 35, pts[3][1] + 25, color=RED_AUX, w=1.5, dashed=True)
    seg(d, pts[4][0], pts[4][1], pts[4][0] - 20, pts[4][1] + 35, color=RED_AUX, w=1.5, dashed=True)
    d.append(
        draw.Text(
            "Сума зовнішніх кутів n-кутника = 360° (4d)",
            13,
            180,
            188,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


# ==============================================================================
# REMAINING ENTRIES REGISTRY
# ==============================================================================

REMAINING_REGISTRY: list[dict] = [
    {
        "num": 15,
        "page": 15,
        "sec": "§ 17",
        "title": "Рівність центральних кутів і дуг",
        "caption": "∠AOB = ∠COD ⟺ Дуга AB = Дуга CD",
        "didactic": "Рівні центральні кути вирізають рівні дуги.",
        "gen": make_fig_15,
        "w": 360,
        "h": 220,
    },
    {
        "num": 17,
        "page": 16,
        "sec": "§ 20",
        "title": "Вимірювання кута транспортиром",
        "caption": "Кут 55° на шкалі транспортира",
        "didactic": "Суміщення центра транспортира з вершиною кута.",
        "gen": make_fig_17,
        "w": 360,
        "h": 220,
    },
    {
        "num": 20,
        "page": 17,
        "sec": "§ 22",
        "title": "Доведення суми суміжних кутів",
        "caption": "∠AOB + ∠BOC = 2d = 180°",
        "didactic": "Порівняння суміжних кутів із прямим кутом.",
        "gen": make_fig_20,
        "w": 360,
        "h": 180,
    },
    {
        "num": 21,
        "page": 17,
        "sec": "§ 22",
        "title": "Властивість рівних суміжних кутів",
        "caption": "Якщо α₁ = α₂, то β₁ = β₂",
        "didactic": "Суміжні кути до рівних кутів рівні між собою.",
        "gen": make_fig_21,
        "w": 360,
        "h": 180,
    },
    {
        "num": 25,
        "page": 19,
        "sec": "§ 26",
        "title": "Побудова суміжних кутів (вправа 1)",
        "caption": "x + 3x = 180°",
        "didactic": "Знаходження міри кутів через алгебраїчне рівняння.",
        "gen": make_fig_25,
        "w": 340,
        "h": 180,
    },
    {
        "num": 26,
        "page": 19,
        "sec": "§ 26",
        "title": "Пряма через вершину кута (вправа 2)",
        "caption": "Пряма через вершину кута",
        "didactic": "Утворення пар суміжних і вертикальних кутів.",
        "gen": make_fig_26,
        "w": 340,
        "h": 180,
    },
    {
        "num": 27,
        "page": 19,
        "sec": "§ 26",
        "title": "Бісектриси вертикальних кутів",
        "caption": "Бісектриси лежать на одній прямій",
        "didactic": "Бісектриси двох вертикальних кутів є доповняльними променями.",
        "gen": make_fig_27,
        "w": 360,
        "h": 200,
    },
    {
        "num": 29,
        "page": 21,
        "sec": "§ 31",
        "title": "Неопуклий многокутник",
        "caption": "Неопуклий контур",
        "didactic": "Пряма, що містить сторону, перетинає многокутник навпіл.",
        "gen": make_fig_29,
        "w": 360,
        "h": 180,
    },
    {
        "num": 30,
        "page": 22,
        "sec": "§ 31",
        "title": "Периметр многокутника",
        "caption": "P = AB + BC + CD + DA",
        "didactic": "Сума довжин усіх сторін многокутника.",
        "gen": make_fig_30,
        "w": 360,
        "h": 160,
    },
    {
        "num": 32,
        "page": 22,
        "sec": "§ 32",
        "title": "Прямокутний різносторонній трикутник",
        "caption": "Трикутник з прямим кутом",
        "didactic": "Один кут 90°, сторони різної довжини.",
        "gen": make_fig_32,
        "w": 320,
        "h": 180,
    },
    {
        "num": 33,
        "page": 22,
        "sec": "§ 32",
        "title": "Тупокутний трикутник",
        "caption": "Один кут більше 90°",
        "didactic": "Сума двох інших кутів менша за 90°.",
        "gen": make_fig_33,
        "w": 340,
        "h": 180,
    },
    {
        "num": 34,
        "page": 22,
        "sec": "§ 32",
        "title": "Рівнобедрений тупокутний трикутник",
        "caption": "Тупий кут при вершині",
        "didactic": "Кути при основі завжди гострі.",
        "gen": make_fig_34,
        "w": 340,
        "h": 180,
    },
    {
        "num": 35,
        "page": 22,
        "sec": "§ 32",
        "title": "Рівносторонній трикутник",
        "caption": "Усі сторони рівні, кути по 60°",
        "didactic": "Правильний трикутник.",
        "gen": make_fig_35,
        "w": 320,
        "h": 190,
    },
    {
        "num": 38,
        "page": 23,
        "sec": "§ 33",
        "title": "Медіана трикутника",
        "caption": "CM — медіана (AM = MB)",
        "didactic": "Сполучає вершину із серединою протилежної сторони.",
        "gen": make_fig_38,
        "w": 340,
        "h": 180,
    },
    {
        "num": 40,
        "page": 24,
        "sec": "§ 34",
        "title": "Рівність кутів при основі",
        "caption": "Доведення накладанням: ∠A = ∠C",
        "didactic": "Перегинання вздовж бісектриси BD.",
        "gen": make_fig_40,
        "w": 340,
        "h": 200,
    },
    {
        "num": 41,
        "page": 25,
        "sec": "§ 34",
        "title": "Вісь симетрії трикутника",
        "caption": "Дзеркальна симетрія відносно BD",
        "didactic": "Кожній точці M відповідає точка M'.",
        "gen": make_fig_41,
        "w": 340,
        "h": 200,
    },
    {
        "num": 43,
        "page": 26,
        "sec": "§ 38",
        "title": "Доведення САК: крок 1",
        "caption": "Суміщення вершини A з A₁",
        "didactic": "Перший крок методу накладання.",
        "gen": make_fig_43_44,
        "w": 360,
        "h": 180,
    },
    {
        "num": 44,
        "page": 26,
        "sec": "§ 38",
        "title": "Доведення САК: крок 2",
        "caption": "Суміщення сторін AB і AC",
        "didactic": "Повний збіг фігур.",
        "gen": make_fig_43_44,
        "w": 360,
        "h": 180,
    },
    {
        "num": 46,
        "page": 27,
        "sec": "§ 38",
        "title": "Доведення АСА накладанням",
        "caption": "Суміщення сторони AC з A₁C₁",
        "didactic": "Збіг напрямків променів.",
        "gen": make_fig_46,
        "w": 360,
        "h": 180,
    },
    {
        "num": 48,
        "page": 28,
        "sec": "§ 38",
        "title": "Доведення ССС прикладанням",
        "caption": "Прикладання за спільною стороною",
        "didactic": "Утворення рівнобедрених трикутників.",
        "gen": make_fig_48_50,
        "w": 360,
        "h": 220,
    },
    {
        "num": 49,
        "page": 28,
        "sec": "§ 38",
        "title": "ССС: гострокутний випадок",
        "caption": "Відрізок BB₁ всередині",
        "didactic": "Кут B ділиться на два рівні кути.",
        "gen": make_fig_48_50,
        "w": 360,
        "h": 220,
    },
    {
        "num": 50,
        "page": 28,
        "sec": "§ 38",
        "title": "ССС: тупокутний випадок",
        "caption": "Відрізок BB₁ зовні",
        "didactic": "Віднімання кутів.",
        "gen": make_fig_48_50,
        "w": 360,
        "h": 220,
    },
    {
        "num": 52,
        "page": 30,
        "sec": "§ 42",
        "title": "Проти більшого кута більша сторона",
        "caption": "∠C > ∠B ⟹ AB > AC",
        "didactic": "Теорема, обернена до властивості сторін.",
        "gen": make_fig_52_53,
        "w": 340,
        "h": 180,
    },
    {
        "num": 53,
        "page": 30,
        "sec": "§ 43",
        "title": "Гіпотенуза більша за катет",
        "caption": "c > a та c > b",
        "didactic": "Прямий кут — найбільший у прямокутному трикутнику.",
        "gen": make_fig_52_53,
        "w": 340,
        "h": 180,
    },
    {
        "num": 55,
        "page": 32,
        "sec": "§ 45",
        "title": "Пряма коротша за ламану",
        "caption": "Пряма AB < Ламана ACDB",
        "didactic": "Прямий відрізок є найкоротшою відстанню.",
        "gen": make_fig_55_57,
        "w": 360,
        "h": 180,
    },
    {
        "num": 56,
        "page": 32,
        "sec": "§ 46",
        "title": "Опукла ламана",
        "caption": "Охоплена опукла ламана",
        "didactic": "Послідовне продовження сторін.",
        "gen": make_fig_55_57,
        "w": 360,
        "h": 180,
    },
    {
        "num": 57,
        "page": 33,
        "sec": "§ 46",
        "title": "Порівняння двох ламаних",
        "caption": "Внутрішня ламана коротша",
        "didactic": "Властивість опуклих контурів.",
        "gen": make_fig_55_57,
        "w": 360,
        "h": 180,
    },
    {
        "num": 59,
        "page": 34,
        "sec": "§ 48",
        "title": "Рівні похилі та проекції",
        "caption": "HA = HB ⟺ PA = PB",
        "didactic": "Властивість прямокутних трикутників.",
        "gen": make_fig_59_61,
        "w": 360,
        "h": 200,
    },
    {
        "num": 60,
        "page": 34,
        "sec": "§ 49",
        "title": "Більша похила має більшу проекцію",
        "caption": "PA > PB ⟺ HA > HB",
        "didactic": "Зв'язок похилої з проекцією.",
        "gen": make_fig_59_61,
        "w": 360,
        "h": 200,
    },
    {
        "num": 61,
        "page": 34,
        "sec": "§ 49",
        "title": "Зворотна теорема про похилі",
        "caption": "HA > HB ⟹ PA > PB",
        "didactic": "Обернене твердження.",
        "gen": make_fig_59_61,
        "w": 360,
        "h": 200,
    },
    {
        "num": 62,
        "page": 35,
        "sec": "§ 50",
        "title": "Найкоротша відстань",
        "caption": "Перпендикуляр — найкоротша лінія",
        "didactic": "Відстань від точки до прямої вимірюється перпендикуляром.",
        "gen": make_fig_59_61,
        "w": 360,
        "h": 200,
    },
    {
        "num": 63,
        "page": 35,
        "sec": "§ 51",
        "title": "Відстань між паралельними",
        "caption": "Перпендикуляри рівні",
        "didactic": "Сталість відстані між паралельними прямими.",
        "gen": make_fig_62_63,
        "w": 360,
        "h": 180,
    },
    {
        "num": 65,
        "page": 36,
        "sec": "§ 56",
        "title": "Бісектриса як ГМТ",
        "caption": "Точки P рівновіддалені від сторін",
        "didactic": "Геометричне місце точок, рівновіддалених від двох прямих.",
        "gen": make_fig_65,
        "w": 360,
        "h": 190,
    },
    {
        "num": 67,
        "page": 37,
        "sec": "§ 59",
        "title": "Задача 2: Кут, рівний даному",
        "caption": "Побудова циркулем",
        "didactic": "Перенесення кута на новий промінь.",
        "gen": make_fig_67,
        "w": 360,
        "h": 180,
    },
    {
        "num": 68,
        "page": 37,
        "sec": "§ 60",
        "title": "Задача 3: Бісектриса кута",
        "caption": "Поділ кута навпіл",
        "didactic": "Побудова променя бісектриси.",
        "gen": make_fig_68,
        "w": 360,
        "h": 190,
    },
    {
        "num": 70,
        "page": 38,
        "sec": "§ 62",
        "title": "Задача 5: Поділ відрізка навпіл",
        "caption": "Серединний перпендикуляр",
        "didactic": "Знаходження середини відрізка циркулем.",
        "gen": make_fig_70,
        "w": 360,
        "h": 200,
    },
    {
        "num": 71,
        "page": 39,
        "sec": "§ 65",
        "title": "Аналіз задачі на побудову",
        "caption": "Схематичний рисунок аналізу",
        "didactic": "Метод розв'язування від шуканої фігури до відомих елементів.",
        "gen": make_fig_71_72,
        "w": 360,
        "h": 200,
    },
    {
        "num": 72,
        "page": 41,
        "sec": "§ 67",
        "title": "Метод геометричних місць",
        "caption": "Перетин двох ГМТ",
        "didactic": "Шукана точка знаходиться на перетині двох ліній.",
        "gen": make_fig_71_72,
        "w": 360,
        "h": 200,
    },
    {
        "num": 74,
        "page": 42,
        "sec": "§ 69",
        "title": "Властивості кутів при січній",
        "caption": "8 кутів при паралельних",
        "didactic": "Рівність різносторонніх та відповідних кутів.",
        "gen": make_fig_74,
        "w": 360,
        "h": 200,
    },
    {
        "num": 76,
        "page": 43,
        "sec": "§ 70",
        "title": "Ознака за відповідними кутами",
        "caption": "∠1 = ∠5 ⟹ a ∥ b",
        "didactic": "Друга ознака паралельності прямих.",
        "gen": make_fig_76,
        "w": 360,
        "h": 200,
    },
    {
        "num": 77,
        "page": 43,
        "sec": "§ 70",
        "title": "Ознака за односторонніми кутами",
        "caption": "∠4 + ∠6 = 180° ⟹ a ∥ b",
        "didactic": "Третя ознака паралельності прямих.",
        "gen": make_fig_77,
        "w": 360,
        "h": 200,
    },
    {
        "num": 78,
        "page": 43,
        "sec": "§ 70",
        "title": "Доведення ознаки паралельності",
        "caption": "Доведення від супротивного",
        "didactic": "Якщо прямі перетинаються, виникає суперечність із сумою кутів.",
        "gen": make_fig_78,
        "w": 360,
        "h": 180,
    },
    {
        "num": 80,
        "page": 44,
        "sec": "§ 72",
        "title": "Транзитивність паралельності",
        "caption": "a ∥ c та b ∥ c ⟹ a ∥ b",
        "didactic": "Дві прямі, паралельні третій, паралельні між собою.",
        "gen": make_fig_80,
        "w": 360,
        "h": 180,
    },
    {
        "num": 82,
        "page": 45,
        "sec": "§ 76",
        "title": "Паралельні протилежні сторони",
        "caption": "α + β = 180°",
        "didactic": "Сума кутів із протилежно напрямленими паралельними сторонами.",
        "gen": make_fig_82,
        "w": 360,
        "h": 200,
    },
    {
        "num": 84,
        "page": 46,
        "sec": "§ 77",
        "title": "Перпендикулярні сторони (сума 180°)",
        "caption": "α + β = 180°",
        "didactic": "Один гострий, один тупий кут.",
        "gen": make_fig_84,
        "w": 360,
        "h": 200,
    },
    {
        "num": 88,
        "page": 48,
        "sec": "§ 81",
        "title": "Сума зовнішніх кутів многокутника",
        "caption": "360° (4d) для будь-якого n-кутника",
        "didactic": "Сума зовнішніх кутів опуклого багатокутника завжди дорівнює 360°.",
        "gen": make_fig_88,
        "w": 360,
        "h": 200,
    },
]


def run():
    db = BookDatabase()
    print("==================================================")
    print(f"🎨 Generating {len(REMAINING_REGISTRY)} remaining figures...")
    print("==================================================")
    saved = 0
    for item in REMAINING_REGISTRY:
        fig_num = item["num"]
        fig_id = f"fig_{fig_num:03d}"
        drawing = item["gen"]()
        svg_xml = drawing.as_svg()

        fig_obj = BookFigure(
            fig_id=fig_id,
            fig_num=fig_num,
            book_id=BOOK_ID,
            page_num=item["page"],
            title=item["title"],
            section_ref=item["sec"],
            caption_original=item["caption"],
            didactic_notes=item["didactic"],
            svg_content=svg_xml,
            width=item["w"],
            height=item["h"],
        )
        db.save_figure(fig_obj)
        saved += 1
        print(f"  ✓ Saved {fig_id} (Рис. {fig_num}): {item['title'][:35]}...")

    total = db.count_figures(BOOK_ID)
    print("==================================================")
    print(f"🎉 Saved {saved} figures. Total in DB: {total} / 89!")
    print("==================================================")


if __name__ == "__main__":
    run()
