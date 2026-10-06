"""Catalog and vector generator for all 89 figures from Kiselev's Geometry (1931).

Generates clean, didactic, modern DrawSVG drawings with full fidelity to
the original textbook and saves them directly into SQLite (data/geometry/book_kb.db).
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

# Design tokens
BG_COLOR = "#f8fafc"
TEXT_COLOR = "#0f172a"
LINE_COLOR = "#1e293b"
BLUE_PRIMARY = "#2563eb"
GREEN_EQUAL = "#16a34a"
RED_AUX = "#dc2626"
PURPLE_AUX = "#9333ea"
GRAY_MUTED = "#64748b"


def create_canvas(w: int = 360, h: int = 220, bg: str = BG_COLOR) -> draw.Drawing:
    d = draw.Drawing(w, h)
    d.append(draw.Rectangle(0, 0, w, h, fill=bg, rx=8, stroke="#e2e8f0", stroke_width=1))
    return d


def draw_pt(
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


def draw_seg(
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


def draw_ray_line(
    d: draw.Drawing,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    ext_start: float = 0,
    ext_end: float = 0,
    color: str = LINE_COLOR,
    w: float = 2.0,
    dashed_ext: bool = False,
):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1e-4:
        return
    ux, uy = dx / L, dy / L
    sx, sy = x1 - ux * ext_start, y1 - uy * ext_start
    ex, ey = x2 + ux * ext_end, y2 + uy * ext_end
    if ext_start > 0:
        draw_seg(d, sx, sy, x1, y1, color=color, w=w, dashed=dashed_ext)
    draw_seg(d, x1, y1, x2, y2, color=color, w=w)
    if ext_end > 0:
        draw_seg(d, x2, y2, ex, ey, color=color, w=w, dashed=dashed_ext)


def draw_angle_arc(
    d: draw.Drawing,
    cx: float,
    cy: float,
    r: float,
    a1_deg: float,
    a2_deg: float,
    color: str = BLUE_PRIMARY,
    w: float = 1.8,
    fill: str = "none",
):
    # In SVG y is down, so invert angles
    d.append(draw.Arc(cx, cy, r, -a2_deg, -a1_deg, stroke=color, stroke_width=w, fill=fill))


def draw_right_sym(
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


def draw_tick(
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
# CATALOG GENERATORS (FIGURES 1 TO 89)
# ==============================================================================


def make_fig_1() -> draw.Drawing:
    d = create_canvas(340, 100)
    draw_ray_line(
        d, 60, 50, 280, 50, ext_start=35, ext_end=35, dashed_ext=True, color=BLUE_PRIMARY, w=2.5
    )
    draw_pt(d, 90, 50, "A", "top")
    draw_pt(d, 250, 50, "B", "top")
    d.append(draw.Text("a", 15, 310, 45, fill=GRAY_MUTED, font_style="italic"))
    return d


def make_fig_2() -> draw.Drawing:
    d = create_canvas(340, 100)
    draw_seg(d, 60, 50, 280, 50, color=BLUE_PRIMARY, w=3.0)
    draw_pt(d, 60, 50, "C", "top")
    draw_pt(d, 280, 50, "D", "top")
    return d


def make_fig_3() -> draw.Drawing:
    d = create_canvas(340, 100)
    draw_seg(d, 70, 50, 290, 50, color=BLUE_PRIMARY, w=2.5)
    draw_seg(d, 290, 50, 320, 50, color=BLUE_PRIMARY, w=2.0, dashed=True)
    draw_pt(d, 70, 50, "E", "top")
    draw_pt(d, 230, 50, "F", "top")
    return d


def make_fig_4() -> draw.Drawing:
    d = create_canvas(360, 130)
    draw_seg(d, 40, 45, 180, 45, color=BLUE_PRIMARY, w=2.5)
    draw_pt(d, 40, 45, "A", "top")
    draw_pt(d, 180, 45, "B", "top")
    draw_seg(d, 210, 45, 350, 45, color=GREEN_EQUAL, w=2.5)
    draw_pt(d, 210, 45, "C", "top")
    draw_pt(d, 350, 45, "D", "top")
    draw_tick(d, 40, 45, 180, 45, 1, GREEN_EQUAL)
    draw_tick(d, 210, 45, 350, 45, 1, GREEN_EQUAL)
    d.append(
        draw.Text("AB = CD (суміщення кінців)", 13, 180, 105, fill=TEXT_COLOR, text_anchor="middle")
    )
    return d


def make_fig_5() -> draw.Drawing:
    d = create_canvas(380, 140)
    draw_seg(d, 40, 40, 110, 40, color=GRAY_MUTED, w=2)
    d.append(draw.Text("AB", 12, 75, 30, text_anchor="middle", fill=GRAY_MUTED))
    draw_seg(d, 130, 40, 230, 40, color=GRAY_MUTED, w=2)
    d.append(draw.Text("CD", 12, 180, 30, text_anchor="middle", fill=GRAY_MUTED))
    draw_seg(d, 250, 40, 330, 40, color=GRAY_MUTED, w=2)
    d.append(draw.Text("EF", 12, 290, 30, text_anchor="middle", fill=GRAY_MUTED))
    y = 85
    draw_seg(d, 30, y, 350, y, color=BLUE_PRIMARY, w=3.0)
    draw_pt(d, 30, y, "M", "bottom")
    draw_pt(d, 100, y, "N", "bottom")
    draw_pt(d, 200, y, "P", "bottom")
    draw_pt(d, 280, y, "Q", "bottom")
    d.append(
        draw.Text(
            "MQ = MN + NP + PQ = AB + CD + EF", 13, 190, 128, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_6() -> draw.Drawing:
    d = create_canvas(360, 240)
    cx, cy, r = 180, 120, 85
    d.append(draw.Circle(cx, cy, r, fill="#f1f5f9", stroke=LINE_COLOR, stroke_width=2))
    draw_pt(d, cx, cy, "O", "bottom-left")
    ax, ay = cx + r * math.cos(math.radians(-30)), cy - r * math.sin(math.radians(-30))
    bx, by = cx + r * math.cos(math.radians(45)), cy - r * math.sin(math.radians(45))
    draw_seg(d, cx, cy, ax, ay, color=BLUE_PRIMARY, w=2)
    draw_seg(d, cx, cy, bx, by, color=BLUE_PRIMARY, w=2)
    draw_pt(d, ax, ay, "A", "right")
    draw_pt(d, bx, by, "B", "top-right")
    ex, ey = cx + r * math.cos(math.radians(150)), cy - r * math.sin(math.radians(150))
    fx, fy = cx + r * math.cos(math.radians(220)), cy - r * math.sin(math.radians(220))
    draw_seg(d, ex, ey, fx, fy, color=GREEN_EQUAL, w=2)
    draw_pt(d, ex, ey, "E", "top-left")
    draw_pt(d, fx, fy, "F", "bottom-left")
    draw_seg(d, cx - r, cy, cx + r, cy, color="#475569", w=1.5, dashed=True)
    d.append(draw.Text("радіус OA", 11, cx + 45, cy + 2, fill=BLUE_PRIMARY))
    d.append(draw.Text("хорда EF", 11, (ex + fx) / 2 - 40, (ey + fy) / 2, fill=GREEN_EQUAL))
    d.append(draw.Text("діаметр", 11, cx - 60, cy - 8, fill=GRAY_MUTED))
    return d


def make_fig_7() -> draw.Drawing:
    d = create_canvas(360, 220)
    cx, cy, r = 180, 115, 80
    d.append(draw.Circle(cx, cy, r, fill="none", stroke="#cbd5e1", stroke_width=1.5))
    draw_pt(d, cx, cy, "O", "bottom")
    d.append(draw.Arc(cx, cy, r, -160, -95, stroke=BLUE_PRIMARY, stroke_width=3.5, fill="none"))
    d.append(draw.Arc(cx, cy, r, -95, -30, stroke=GREEN_EQUAL, stroke_width=3.5, fill="none"))
    mx, my = cx + r * math.cos(math.radians(160)), cy - r * math.sin(math.radians(160))
    nx, ny = cx + r * math.cos(math.radians(95)), cy - r * math.sin(math.radians(95))
    px, py = cx + r * math.cos(math.radians(30)), cy - r * math.sin(math.radians(30))
    draw_pt(d, mx, my, "M", "left")
    draw_pt(d, nx, ny, "N", "top")
    draw_pt(d, px, py, "P", "right")
    d.append(
        draw.Text(
            "Дуга MP = Дуга MN + Дуга NP", 13, 180, 205, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_8() -> draw.Drawing:
    d = create_canvas(340, 200)
    ox, oy = 50, 160
    ax, ay = ox + 180 * math.cos(math.radians(55)), oy - 180 * math.sin(math.radians(55))
    bx, by = ox + 220, oy
    draw_seg(d, ox, oy, bx, by, color=LINE_COLOR, w=2.5)
    draw_seg(d, ox, oy, ax, ay, color=BLUE_PRIMARY, w=2.5)
    draw_pt(d, ox, oy, "O", "left")
    draw_pt(d, ax, ay, "A", "top-right")
    draw_pt(d, bx, by, "B", "bottom")
    draw_angle_arc(d, ox, oy, 40, 0, 55, color=BLUE_PRIMARY)
    d.append(
        draw.Text("внутрішня область", 12, ox + 90, oy - 45, fill=BLUE_PRIMARY, font_style="italic")
    )
    return d


def make_fig_9() -> draw.Drawing:
    d = create_canvas(360, 180)
    # Angle 1
    o1x, o1y = 40, 140
    a1x, a1y = o1x + 100 * math.cos(math.radians(50)), o1y - 100 * math.sin(math.radians(50))
    draw_seg(d, o1x, o1y, o1x + 110, o1y, color=LINE_COLOR, w=2)
    draw_seg(d, o1x, o1y, a1x, a1y, color=LINE_COLOR, w=2)
    draw_pt(d, o1x, o1y, "O", "bottom-left")
    draw_pt(d, a1x, a1y, "A", "top")
    draw_pt(d, o1x + 110, o1y, "B", "bottom")
    draw_angle_arc(d, o1x, o1y, 30, 0, 50, color=BLUE_PRIMARY)
    # Angle 2
    o2x, o2y = 210, 140
    a2x, a2y = o2x + 100 * math.cos(math.radians(50)), o2y - 100 * math.sin(math.radians(50))
    draw_seg(d, o2x, o2y, o2x + 110, o2y, color=GREEN_EQUAL, w=2)
    draw_seg(d, o2x, o2y, a2x, a2y, color=GREEN_EQUAL, w=2)
    draw_pt(d, o2x, o2y, "O₁", "bottom-left")
    draw_pt(d, a2x, a2y, "A₁", "top")
    draw_pt(d, o2x + 110, o2y, "B₁", "bottom")
    draw_angle_arc(d, o2x, o2y, 30, 0, 50, color=GREEN_EQUAL)
    d.append(
        draw.Text(
            "∠AOB = ∠A₁O₁B₁ (накладання)", 13, 180, 170, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_10() -> draw.Drawing:
    d = create_canvas(340, 200)
    ox, oy = 50, 160
    draw_seg(d, ox, oy, ox + 220, oy, color=LINE_COLOR, w=2.5)  # OB
    bx, by = ox + 220, oy
    c_deg = 35
    cx = ox + 180 * math.cos(math.radians(c_deg))
    cy = oy - 180 * math.sin(math.radians(c_deg))
    draw_seg(d, ox, oy, cx, cy, color=GREEN_EQUAL, w=2.5)  # OC
    a_deg = 70
    ax = ox + 180 * math.cos(math.radians(a_deg))
    ay = oy - 180 * math.sin(math.radians(a_deg))
    draw_seg(d, ox, oy, ax, ay, color=BLUE_PRIMARY, w=2.5)  # OA
    draw_pt(d, ox, oy, "O", "left")
    draw_pt(d, bx, by, "B", "bottom")
    draw_pt(d, cx, cy, "C", "right")
    draw_pt(d, ax, ay, "A", "top")
    draw_angle_arc(d, ox, oy, 35, 0, c_deg, color=GREEN_EQUAL)
    draw_angle_arc(d, ox, oy, 50, c_deg, a_deg, color=BLUE_PRIMARY)
    d.append(draw.Text("∠AOB = ∠AOC + ∠COB", 13, 170, 190, text_anchor="middle", fill=TEXT_COLOR))
    return d


def make_fig_11() -> draw.Drawing:
    d = create_canvas(340, 120)
    ox, oy = 170, 70
    draw_seg(d, 30, oy, 310, oy, color=LINE_COLOR, w=2.5)
    draw_pt(d, 50, oy, "A", "bottom")
    draw_pt(d, ox, oy, "O", "bottom")
    draw_pt(d, 290, oy, "B", "bottom")
    draw_angle_arc(d, ox, oy, 40, 0, 180, color=BLUE_PRIMARY, w=2.0)
    d.append(
        draw.Text(
            "Розгорнутий кут = 180° (2d)", 13, ox, 25, text_anchor="middle", fill=BLUE_PRIMARY
        )
    )
    return d


def make_fig_12() -> draw.Drawing:
    d = create_canvas(300, 200)
    ox, oy = 60, 160
    draw_seg(d, ox, oy, ox + 180, oy, color=LINE_COLOR, w=2.5)
    draw_seg(d, ox, oy, ox, oy - 130, color=LINE_COLOR, w=2.5)
    draw_pt(d, ox, oy, "O", "bottom-left")
    draw_pt(d, ox + 180, oy, "B", "bottom")
    draw_pt(d, ox, oy - 130, "A", "left")
    draw_right_sym(d, ox, oy, 0, 16, GREEN_EQUAL)
    d.append(draw.Text("Прямий кут = 90° (d)", 14, 180, 80, fill=GREEN_EQUAL, font_weight="bold"))
    return d


def make_fig_13() -> draw.Drawing:
    d = create_canvas(320, 180)
    ox, oy = 150, 90
    draw_seg(d, ox, oy, ox + 120, oy, color=BLUE_PRIMARY, w=2.5)
    draw_pt(d, ox, oy, "O", "left")
    draw_pt(d, ox + 120, oy, "A", "right")
    d.append(
        draw.Circle(
            ox, oy, 45, fill="none", stroke=BLUE_PRIMARY, stroke_width=2, stroke_dasharray="4,3"
        )
    )
    d.append(
        draw.Text("Повний кут = 360° (4d)", 13, ox, 160, text_anchor="middle", fill=TEXT_COLOR)
    )
    return d


def make_fig_14_15() -> draw.Drawing:
    d = create_canvas(360, 220)
    cx, cy, r = 180, 110, 75
    d.append(draw.Circle(cx, cy, r, fill="none", stroke="#cbd5e1", stroke_width=1.5))
    draw_pt(d, cx, cy, "O", "left")
    a1, a2 = -30, 40
    p1x, p1y = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    p2x, p2y = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    draw_seg(d, cx, cy, p1x, p1y, color=BLUE_PRIMARY, w=2)
    draw_seg(d, cx, cy, p2x, p2y, color=BLUE_PRIMARY, w=2)
    draw_pt(d, p1x, p1y, "A", "right")
    draw_pt(d, p2x, p2y, "B", "top-right")
    draw_angle_arc(d, cx, cy, 30, a1, a2, color=BLUE_PRIMARY)
    d.append(draw.Arc(cx, cy, r, -a2, -a1, stroke=GREEN_EQUAL, stroke_width=3.5, fill="none"))
    d.append(
        draw.Text("Центральний кут і дуга AB", 13, 180, 205, text_anchor="middle", fill=TEXT_COLOR)
    )
    return d


def make_fig_16_17() -> draw.Drawing:
    d = create_canvas(360, 220)
    ox, oy, r = 180, 160, 130
    d.append(draw.Arc(ox, oy, r, -180, 0, stroke=LINE_COLOR, stroke_width=2, fill="#f1f5f9"))
    draw_seg(d, ox - r - 10, oy, ox + r + 10, oy, color=LINE_COLOR, w=2)
    draw_pt(d, ox, oy, "O", "bottom")
    for ang in range(0, 181, 10):
        rad = math.radians(ang)
        x1 = ox + (r - (10 if ang % 30 == 0 else 5)) * math.cos(rad)
        y1 = oy - (r - (10 if ang % 30 == 0 else 5)) * math.sin(rad)
        x2 = ox + r * math.cos(rad)
        y2 = oy - r * math.sin(rad)
        draw_seg(d, x1, y1, x2, y2, color=GRAY_MUTED, w=1)
    d.append(
        draw.Text(
            "Транспортир (шкала 0° - 180°)", 13, ox, 195, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_18() -> draw.Drawing:
    d = create_canvas(380, 140)
    # Acute
    draw_seg(d, 20, 100, 100, 100, color=LINE_COLOR, w=2)
    draw_seg(d, 20, 100, 80, 45, color=BLUE_PRIMARY, w=2)
    draw_angle_arc(d, 20, 100, 25, 0, 45, color=BLUE_PRIMARY)
    d.append(draw.Text("Гострий (<90°)", 11, 55, 125, text_anchor="middle", fill=TEXT_COLOR))
    # Right
    draw_seg(d, 140, 100, 210, 100, color=LINE_COLOR, w=2)
    draw_seg(d, 140, 100, 140, 35, color=GREEN_EQUAL, w=2)
    draw_right_sym(d, 140, 100, 0, 12, GREEN_EQUAL)
    d.append(draw.Text("Прямий (=90°)", 11, 175, 125, text_anchor="middle", fill=TEXT_COLOR))
    # Obtuse
    draw_seg(d, 270, 100, 360, 100, color=LINE_COLOR, w=2)
    draw_seg(d, 270, 100, 220, 45, color=RED_AUX, w=2)
    draw_angle_arc(d, 270, 100, 25, 0, 135, color=RED_AUX)
    d.append(draw.Text("Тупий (>90°)", 11, 295, 125, text_anchor="middle", fill=TEXT_COLOR))
    return d


def make_fig_19_21() -> draw.Drawing:
    d = create_canvas(360, 180)
    ox, oy = 180, 130
    draw_seg(d, 40, oy, 320, oy, color=LINE_COLOR, w=2.5)
    rad = math.radians(60)
    bx, by = ox + 110 * math.cos(rad), oy - 110 * math.sin(rad)
    draw_seg(d, ox, oy, bx, by, color=BLUE_PRIMARY, w=2.5)
    draw_pt(d, ox, oy, "O", "bottom")
    draw_pt(d, 40, oy, "A", "bottom")
    draw_pt(d, 320, oy, "C", "bottom")
    draw_pt(d, bx, by, "B", "top-right")
    draw_angle_arc(d, ox, oy, 30, 0, 60, color=BLUE_PRIMARY)
    draw_angle_arc(d, ox, oy, 35, 60, 180, color=RED_AUX)
    d.append(draw.Text("α", 13, ox + 45, oy - 15, fill=BLUE_PRIMARY, font_weight="bold"))
    d.append(draw.Text("β = 180° - α", 13, ox - 75, oy - 20, fill=RED_AUX, font_weight="bold"))
    return d


def make_fig_22() -> draw.Drawing:
    d = create_canvas(340, 180)
    ox, oy = 170, 130
    draw_seg(d, 40, oy, 300, oy, color=LINE_COLOR, w=2.5)
    draw_seg(d, ox, oy, ox, 30, color=GREEN_EQUAL, w=2.5)
    draw_pt(d, ox, oy, "O", "bottom")
    draw_pt(d, ox, 30, "B", "top")
    draw_pt(d, 40, oy, "A", "bottom")
    draw_pt(d, 300, oy, "C", "bottom")
    draw_right_sym(d, ox, oy, 0, 14, GREEN_EQUAL)
    draw_right_sym(d, ox, oy, 90, 14, GREEN_EQUAL)
    d.append(
        draw.Text(
            "OB ⊥ AC (перпендикуляр)",
            13,
            170,
            165,
            text_anchor="middle",
            fill=GREEN_EQUAL,
            font_weight="bold",
        )
    )
    return d


def make_fig_23() -> draw.Drawing:
    d = create_canvas(360, 200)
    ox, oy = 180, 100
    L = 140
    a_deg = 40
    ux1, uy1 = math.cos(math.radians(a_deg)), math.sin(math.radians(a_deg))
    ux2, uy2 = math.cos(math.radians(-a_deg)), math.sin(math.radians(-a_deg))
    draw_seg(d, ox - L * ux1, oy + L * uy1, ox + L * ux1, oy - L * uy1, color=LINE_COLOR, w=2.5)
    draw_seg(d, ox - L * ux2, oy + L * uy2, ox + L * ux2, oy - L * uy2, color=LINE_COLOR, w=2.5)
    draw_pt(d, ox, oy, "O", "bottom")
    draw_angle_arc(d, ox, oy, 30, -a_deg, a_deg, color=BLUE_PRIMARY)
    draw_angle_arc(d, ox, oy, 30, 180 - a_deg, 180 + a_deg, color=BLUE_PRIMARY)
    draw_angle_arc(d, ox, oy, 35, a_deg, 180 - a_deg, color=GREEN_EQUAL)
    draw_angle_arc(d, ox, oy, 35, 180 + a_deg, 360 - a_deg, color=GREEN_EQUAL)
    d.append(draw.Text("∠1", 12, ox + 45, oy + 4, fill=BLUE_PRIMARY, font_weight="bold"))
    d.append(draw.Text("∠3", 12, ox - 55, oy + 4, fill=BLUE_PRIMARY, font_weight="bold"))
    d.append(
        draw.Text("∠2", 12, ox, oy - 45, fill=GREEN_EQUAL, font_weight="bold", text_anchor="middle")
    )
    d.append(
        draw.Text("∠4", 12, ox, oy + 55, fill=GREEN_EQUAL, font_weight="bold", text_anchor="middle")
    )
    d.append(
        draw.Text(
            "Вертикальні кути: ∠1 = ∠3, ∠2 = ∠4", 13, ox, 190, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_24_27() -> draw.Drawing:
    d = create_canvas(360, 200)
    ox, oy = 180, 130
    draw_seg(d, 40, oy, 320, oy, color=LINE_COLOR, w=2)
    # Two adjacent bisectors
    bx, by = ox + 100 * math.cos(math.radians(70)), oy - 100 * math.sin(math.radians(70))
    draw_seg(d, ox, oy, bx, by, color=LINE_COLOR, w=2)
    # Bisector 1 of 70deg -> 35deg
    b1x, b1y = ox + 110 * math.cos(math.radians(35)), oy - 110 * math.sin(math.radians(35))
    draw_seg(d, ox, oy, b1x, b1y, color=BLUE_PRIMARY, w=2, dashed=True)
    # Bisector 2 of 110deg -> 125deg
    b2x, b2y = ox + 110 * math.cos(math.radians(125)), oy - 110 * math.sin(math.radians(125))
    draw_seg(d, ox, oy, b2x, b2y, color=RED_AUX, w=2, dashed=True)
    draw_pt(d, ox, oy, "O", "bottom")
    draw_right_sym(d, ox, oy, 35, 14, GREEN_EQUAL)
    d.append(
        draw.Text(
            "Кут між бісектрисами суміжних кутів = 90°",
            13,
            ox,
            180,
            text_anchor="middle",
            fill=GREEN_EQUAL,
            font_weight="bold",
        )
    )
    return d


def make_fig_28_30() -> draw.Drawing:
    d = create_canvas(360, 200)
    # Polygon ABCDE
    pts = [(80, 150), (60, 80), (160, 40), (280, 70), (250, 160)]
    names = ["A", "B", "C", "D", "E"]
    poly_pts = [c for pt in pts for c in pt]
    d.append(draw.Lines(*poly_pts, close=True, fill="#f1f5f9", stroke=LINE_COLOR, stroke_width=2))
    # Diagonal AC
    draw_seg(d, pts[0][0], pts[0][1], pts[2][0], pts[2][1], color=BLUE_PRIMARY, w=1.5, dashed=True)
    draw_seg(d, pts[0][0], pts[0][1], pts[3][0], pts[3][1], color=BLUE_PRIMARY, w=1.5, dashed=True)
    for (x, y), name in zip(pts, names, strict=True):
        draw_pt(d, x, y, name, "top" if y < 100 else "bottom")
    d.append(
        draw.Text(
            "Опуклий многокутник і діагоналі", 13, 180, 190, text_anchor="middle", fill=TEXT_COLOR
        )
    )
    return d


def make_fig_31_35() -> draw.Drawing:
    d = create_canvas(380, 180)
    # Isosceles
    ix, iy = 90, 130
    draw_seg(d, ix - 50, iy, ix + 50, iy, color=LINE_COLOR, w=2)
    draw_seg(d, ix - 50, iy, ix, iy - 80, color=BLUE_PRIMARY, w=2)
    draw_seg(d, ix + 50, iy, ix, iy - 80, color=BLUE_PRIMARY, w=2)
    draw_tick(d, ix - 50, iy, ix, iy - 80, 1, BLUE_PRIMARY)
    draw_tick(d, ix + 50, iy, ix, iy - 80, 1, BLUE_PRIMARY)
    d.append(draw.Text("Рівнобедрений", 11, ix, iy + 25, text_anchor="middle", fill=TEXT_COLOR))
    # Equilateral
    eqx, eqy = 270, 130
    s = 70
    draw_seg(d, eqx - s / 2, eqy, eqx + s / 2, eqy, color=GREEN_EQUAL, w=2)
    draw_seg(d, eqx - s / 2, eqy, eqx, eqy - s * 0.866, color=GREEN_EQUAL, w=2)
    draw_seg(d, eqx + s / 2, eqy, eqx, eqy - s * 0.866, color=GREEN_EQUAL, w=2)
    draw_tick(d, eqx - s / 2, eqy, eqx + s / 2, eqy, 1, GREEN_EQUAL)
    draw_tick(d, eqx - s / 2, eqy, eqx, eqy - s * 0.866, 1, GREEN_EQUAL)
    draw_tick(d, eqx + s / 2, eqy, eqx, eqy - s * 0.866, 1, GREEN_EQUAL)
    d.append(draw.Text("Рівносторонній", 11, eqx, eqy + 25, text_anchor="middle", fill=TEXT_COLOR))
    return d


def make_fig_36() -> draw.Drawing:
    d = create_canvas(340, 200)
    ax, ay = 60, 150
    bx, by = 260, 150
    cx, cy = 60, 40
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#f0fdf4", stroke=LINE_COLOR, stroke_width=2
        )
    )
    draw_right_sym(d, ax, ay, 0, 14, GREEN_EQUAL)
    draw_pt(d, ax, ay, "A (90°)", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom-right")
    draw_pt(d, cx, cy, "C", "top-left")
    d.append(draw.Text("катет b", 12, ax - 15, (ay + cy) / 2, text_anchor="end", fill=TEXT_COLOR))
    d.append(
        draw.Text("катет a", 12, (ax + bx) / 2, ay + 18, text_anchor="middle", fill=TEXT_COLOR)
    )
    d.append(
        draw.Text(
            "гіпотенуза c",
            12,
            (bx + cx) / 2 + 10,
            (by + cy) / 2 - 10,
            fill=BLUE_PRIMARY,
            font_weight="bold",
        )
    )
    return d


def make_fig_37_38() -> draw.Drawing:
    d = create_canvas(360, 200)
    ax, ay = 60, 160
    bx, by = 300, 160
    cx, cy = 160, 40
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#f8fafc", stroke=LINE_COLOR, stroke_width=2
        )
    )
    # Altitude CH
    hx, hy = cx, ay
    draw_seg(d, cx, cy, hx, hy, color=RED_AUX, w=2)
    draw_right_sym(d, hx, hy, 0, 10, RED_AUX)
    # Median CM
    mx, my = (ax + bx) / 2, ay
    draw_seg(d, cx, cy, mx, my, color=BLUE_PRIMARY, w=2, dashed=True)
    # Bisector CL
    lx, ly = 175, ay
    draw_seg(d, cx, cy, lx, ly, color=GREEN_EQUAL, w=2)
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom-right")
    draw_pt(d, cx, cy, "C", "top")
    draw_pt(d, hx, hy, "H", "bottom", color=RED_AUX)
    draw_pt(d, mx, my, "M", "bottom", color=BLUE_PRIMARY)
    d.append(
        draw.Text(
            "CH — висота, CM — медіана, CL — бісектриса",
            12,
            180,
            195,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_39_41() -> draw.Drawing:
    d = create_canvas(340, 220)
    ax, ay = 60, 170
    cx, cy = 280, 170
    bx, by = 170, 40
    d.append(
        draw.Lines(
            ax, ay, cx, cy, bx, by, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    # Axis of symmetry BD
    dx, dy = (ax + cx) / 2, ay
    draw_seg(d, bx, by, dx, dy, color=RED_AUX, w=2, dashed=True)
    draw_right_sym(d, dx, dy, 0, 12, RED_AUX)
    draw_tick(d, ax, ay, bx, by, 1, BLUE_PRIMARY)
    draw_tick(d, cx, cy, bx, by, 1, BLUE_PRIMARY)
    draw_tick(d, ax, ay, dx, dy, 2, GREEN_EQUAL)
    draw_tick(d, cx, cy, dx, dy, 2, GREEN_EQUAL)
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, cx, cy, "C", "bottom-right")
    draw_pt(d, bx, by, "B", "top")
    draw_pt(d, dx, dy, "D", "bottom")
    draw_angle_arc(d, ax, ay, 25, 0, 50, color=GREEN_EQUAL)
    draw_angle_arc(d, cx, cy, 25, 130, 180, color=GREEN_EQUAL)
    d.append(
        draw.Text(
            "∠A = ∠C, BD — вісь симетрії",
            13,
            170,
            205,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_42_44() -> draw.Drawing:
    # 1st congruence (SAS)
    d = create_canvas(380, 190)
    # T1
    p1 = [(40, 140), (140, 140), (70, 50)]
    d.append(
        draw.Lines(
            p1[0][0],
            p1[0][1],
            p1[1][0],
            p1[1][1],
            p1[2][0],
            p1[2][1],
            close=True,
            fill="#eff6ff",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    draw_pt(d, p1[0][0], p1[0][1], "A", "bottom-left")
    draw_pt(d, p1[1][0], p1[1][1], "C", "bottom-right")
    draw_pt(d, p1[2][0], p1[2][1], "B", "top")
    draw_tick(d, p1[0][0], p1[0][1], p1[1][0], p1[1][1], 1, BLUE_PRIMARY)
    draw_tick(d, p1[0][0], p1[0][1], p1[2][0], p1[2][1], 2, GREEN_EQUAL)
    draw_angle_arc(d, p1[0][0], p1[0][1], 20, 0, 70, color=RED_AUX)
    # T2
    p2 = [(220, 140), (320, 140), (250, 50)]
    d.append(
        draw.Lines(
            p2[0][0],
            p2[0][1],
            p2[1][0],
            p2[1][1],
            p2[2][0],
            p2[2][1],
            close=True,
            fill="#eff6ff",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    draw_pt(d, p2[0][0], p2[0][1], "A₁", "bottom-left")
    draw_pt(d, p2[1][0], p2[1][1], "C₁", "bottom-right")
    draw_pt(d, p2[2][0], p2[2][1], "B₁", "top")
    draw_tick(d, p2[0][0], p2[0][1], p2[1][0], p2[1][1], 1, BLUE_PRIMARY)
    draw_tick(d, p2[0][0], p2[0][1], p2[2][0], p2[2][1], 2, GREEN_EQUAL)
    draw_angle_arc(d, p2[0][0], p2[0][1], 20, 0, 70, color=RED_AUX)
    d.append(
        draw.Text(
            "Перша ознака рівності (САК)",
            13,
            190,
            175,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_45_46() -> draw.Drawing:
    # 2nd congruence (ASA)
    d = create_canvas(380, 190)
    p1 = [(40, 140), (150, 140), (80, 50)]
    d.append(
        draw.Lines(
            p1[0][0],
            p1[0][1],
            p1[1][0],
            p1[1][1],
            p1[2][0],
            p1[2][1],
            close=True,
            fill="#f0fdf4",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    draw_pt(d, p1[0][0], p1[0][1], "A", "bottom-left")
    draw_pt(d, p1[1][0], p1[1][1], "C", "bottom-right")
    draw_pt(d, p1[2][0], p1[2][1], "B", "top")
    draw_tick(d, p1[0][0], p1[0][1], p1[1][0], p1[1][1], 1, BLUE_PRIMARY)
    draw_angle_arc(d, p1[0][0], p1[0][1], 22, 0, 65, color=GREEN_EQUAL)
    draw_angle_arc(d, p1[1][0], p1[1][1], 22, 130, 180, color=RED_AUX)
    p2 = [(220, 140), (330, 140), (260, 50)]
    d.append(
        draw.Lines(
            p2[0][0],
            p2[0][1],
            p2[1][0],
            p2[1][1],
            p2[2][0],
            p2[2][1],
            close=True,
            fill="#f0fdf4",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    draw_pt(d, p2[0][0], p2[0][1], "A₁", "bottom-left")
    draw_pt(d, p2[1][0], p2[1][1], "C₁", "bottom-right")
    draw_pt(d, p2[2][0], p2[2][1], "B₁", "top")
    draw_tick(d, p2[0][0], p2[0][1], p2[1][0], p2[1][1], 1, BLUE_PRIMARY)
    draw_angle_arc(d, p2[0][0], p2[0][1], 22, 0, 65, color=GREEN_EQUAL)
    draw_angle_arc(d, p2[1][0], p2[1][1], 22, 130, 180, color=RED_AUX)
    d.append(
        draw.Text(
            "Друга ознака рівності (АСА)",
            13,
            190,
            175,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_47_50() -> draw.Drawing:
    # 3rd congruence (SSS)
    d = create_canvas(380, 190)
    p1 = [(40, 140), (140, 140), (80, 50)]
    d.append(
        draw.Lines(
            p1[0][0],
            p1[0][1],
            p1[1][0],
            p1[1][1],
            p1[2][0],
            p1[2][1],
            close=True,
            fill="#fdf4ff",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    draw_pt(d, p1[0][0], p1[0][1], "A", "bottom-left")
    draw_pt(d, p1[1][0], p1[1][1], "C", "bottom-right")
    draw_pt(d, p1[2][0], p1[2][1], "B", "top")
    draw_tick(d, p1[0][0], p1[0][1], p1[1][0], p1[1][1], 1, BLUE_PRIMARY)
    draw_tick(d, p1[0][0], p1[0][1], p1[2][0], p1[2][1], 2, GREEN_EQUAL)
    draw_tick(d, p1[1][0], p1[1][1], p1[2][0], p1[2][1], 3, RED_AUX)
    p2 = [(220, 140), (320, 140), (260, 50)]
    d.append(
        draw.Lines(
            p2[0][0],
            p2[0][1],
            p2[1][0],
            p2[1][1],
            p2[2][0],
            p2[2][1],
            close=True,
            fill="#fdf4ff",
            stroke=LINE_COLOR,
            stroke_width=2,
        )
    )
    draw_pt(d, p2[0][0], p2[0][1], "A₁", "bottom-left")
    draw_pt(d, p2[1][0], p2[1][1], "C₁", "bottom-right")
    draw_pt(d, p2[2][0], p2[2][1], "B₁", "top")
    draw_tick(d, p2[0][0], p2[0][1], p2[1][0], p2[1][1], 1, BLUE_PRIMARY)
    draw_tick(d, p2[0][0], p2[0][1], p2[2][0], p2[2][1], 2, GREEN_EQUAL)
    draw_tick(d, p2[1][0], p2[1][1], p2[2][0], p2[2][1], 3, RED_AUX)
    d.append(
        draw.Text(
            "Третя ознака рівності (ССС)",
            13,
            190,
            175,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_51_53() -> draw.Drawing:
    # Larger side opposite larger angle
    d = create_canvas(340, 200)
    ax, ay = 50, 150
    bx, by = 290, 150
    cx, cy = 110, 40
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#fffbeb", stroke=LINE_COLOR, stroke_width=2
        )
    )
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom-right")
    draw_pt(d, cx, cy, "C", "top")
    draw_angle_arc(d, cx, cy, 25, -90, 20, color=RED_AUX)
    draw_angle_arc(d, bx, by, 30, 150, 180, color=BLUE_PRIMARY)
    d.append(
        draw.Text(
            "AB > AC  ⟺  ∠C > ∠B",
            13,
            170,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_54_57() -> draw.Drawing:
    # Triangle inequality a < b + c
    d = create_canvas(340, 180)
    ax, ay = 50, 130
    bx, by = 280, 130
    cx, cy = 140, 45
    draw_seg(d, ax, ay, bx, by, color=BLUE_PRIMARY, w=3.0)
    draw_seg(d, ax, ay, cx, cy, color=LINE_COLOR, w=2.0)
    draw_seg(d, cx, cy, bx, by, color=LINE_COLOR, w=2.0)
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom-right")
    draw_pt(d, cx, cy, "C", "top")
    d.append(
        draw.Text(
            "AB < AC + CB (Нерівність трикутника)",
            13,
            170,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_58_63() -> draw.Drawing:
    # Perpendicular & oblique lines
    d = create_canvas(360, 210)
    sy = 150
    draw_seg(d, 30, sy, 330, sy, color=LINE_COLOR, w=2)
    px, py = 180, 40
    draw_pt(d, px, py, "P", "top")
    # Perpendicular PH
    draw_seg(d, px, py, px, sy, color=RED_AUX, w=2.5)
    draw_pt(d, px, sy, "H", "bottom")
    draw_right_sym(d, px, sy, 0, 12, RED_AUX)
    # Oblique PA and PB
    draw_seg(d, px, py, 90, sy, color=BLUE_PRIMARY, w=2)
    draw_pt(d, 90, sy, "A", "bottom")
    draw_seg(d, px, py, 270, sy, color=BLUE_PRIMARY, w=2)
    draw_pt(d, 270, sy, "B", "bottom")
    draw_tick(d, 90, sy, px, sy, 1, GREEN_EQUAL)
    draw_tick(d, px, sy, 270, sy, 1, GREEN_EQUAL)
    d.append(
        draw.Text(
            "HA = HB  ⟹  PA = PB (перпендикуляр і похилі)",
            13,
            180,
            195,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_64_65() -> draw.Drawing:
    # Perpendicular bisector as locus
    d = create_canvas(360, 200)
    ax, ay = 60, 150
    bx, by = 300, 150
    mx, my = (ax + bx) / 2, ay
    draw_seg(d, ax, ay, bx, by, color=LINE_COLOR, w=2)
    draw_seg(d, mx, 20, mx, 170, color=RED_AUX, w=2.5)
    draw_right_sym(d, mx, my, 0, 12, RED_AUX)
    px, py = mx, 50
    draw_seg(d, px, py, ax, ay, color=BLUE_PRIMARY, w=1.8, dashed=True)
    draw_seg(d, px, py, bx, by, color=BLUE_PRIMARY, w=1.8, dashed=True)
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom-right")
    draw_pt(d, mx, my, "M", "bottom-right")
    draw_pt(d, px, py, "P", "top-right")
    draw_tick(d, ax, ay, mx, my, 1, GREEN_EQUAL)
    draw_tick(d, mx, my, bx, by, 1, GREEN_EQUAL)
    d.append(
        draw.Text(
            "Серединний перпендикуляр: PA = PB (ГМТ)",
            13,
            180,
            190,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_66_68() -> draw.Drawing:
    # Constructions: angle bisector using compass
    d = create_canvas(360, 200)
    ox, oy = 50, 160
    ax, ay = ox + 220 * math.cos(math.radians(50)), oy - 220 * math.sin(math.radians(50))
    bx, by = ox + 250, oy
    draw_seg(d, ox, oy, ax, ay, color=LINE_COLOR, w=2)
    draw_seg(d, ox, oy, bx, by, color=LINE_COLOR, w=2)
    draw_pt(d, ox, oy, "O", "left")
    # Compass arc from O
    r1 = 90
    p1x, p1y = ox + r1 * math.cos(math.radians(50)), oy - r1 * math.sin(math.radians(50))
    p2x, p2y = ox + r1, oy
    draw_pt(d, p1x, p1y, "D", "top-left", color=GREEN_EQUAL)
    draw_pt(d, p2x, p2y, "E", "bottom", color=GREEN_EQUAL)
    d.append(
        draw.Arc(
            ox,
            oy,
            r1,
            -55,
            5,
            stroke=GREEN_EQUAL,
            stroke_width=1.5,
            stroke_dasharray="4,3",
            fill="none",
        )
    )
    # Intersecting arcs
    cx, cy = ox + 180 * math.cos(math.radians(25)), oy - 180 * math.sin(math.radians(25))
    draw_seg(d, ox, oy, cx + 40, cy - 20, color=RED_AUX, w=2.5)
    draw_pt(d, cx, cy, "C", "top", color=RED_AUX)
    d.append(
        draw.Text(
            "Побудова бісектриси циркулем і лінійкою",
            13,
            180,
            190,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_69_70() -> draw.Drawing:
    # Perpendicular from point outside line
    d = create_canvas(360, 200)
    draw_seg(d, 30, 150, 330, 150, color=LINE_COLOR, w=2)
    cx, cy = 180, 45
    draw_pt(d, cx, cy, "C", "top")
    # Arc from C
    d.append(
        draw.Arc(
            cx,
            cy,
            120,
            -145,
            -35,
            stroke=GREEN_EQUAL,
            stroke_width=1.5,
            stroke_dasharray="4,3",
            fill="none",
        )
    )
    ax, ay = cx - 70, 150
    bx, by = cx + 70, 150
    draw_pt(d, ax, ay, "A", "bottom")
    draw_pt(d, bx, by, "B", "bottom")
    draw_seg(d, cx, cy, cx, 150, color=RED_AUX, w=2.5)
    draw_pt(d, cx, 150, "P", "bottom-right", color=RED_AUX)
    draw_right_sym(d, cx, 150, 0, 12, RED_AUX)
    d.append(
        draw.Text(
            "Перпендикуляр із точки C до прямої AB",
            13,
            180,
            190,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_73_74() -> draw.Drawing:
    # Two lines and transversal
    d = create_canvas(360, 220)
    # Line 1 (AB)
    y1 = 65
    draw_seg(d, 30, y1, 330, y1, color=BLUE_PRIMARY, w=2.5)
    d.append(draw.Text("a", 14, 340, y1 + 5, fill=BLUE_PRIMARY, font_style="italic"))
    # Line 2 (CD)
    y2 = 145
    draw_seg(d, 30, y2, 330, y2, color=BLUE_PRIMARY, w=2.5)
    d.append(draw.Text("b", 14, 340, y2 + 5, fill=BLUE_PRIMARY, font_style="italic"))
    # Transversal (c)
    draw_seg(d, 80, 25, 260, 185, color=RED_AUX, w=2.5)
    d.append(draw.Text("c (січна)", 13, 275, 190, fill=RED_AUX))
    # Labels for angles
    p1x, p1y = 125, y1
    p2x, p2y = 215, y2
    draw_pt(d, p1x, p1y, "P", "top-left")
    draw_pt(d, p2x, p2y, "Q", "bottom-right")
    # Alternate interior: ∠4 and ∠6
    d.append(draw.Text("1", 11, p1x - 12, p1y - 12, fill=TEXT_COLOR))
    d.append(draw.Text("2", 11, p1x + 12, p1y - 12, fill=TEXT_COLOR))
    d.append(draw.Text("3", 11, p1x - 14, p1y + 14, fill=TEXT_COLOR))
    d.append(draw.Text("4", 11, p1x + 10, p1y + 14, fill=GREEN_EQUAL, font_weight="bold"))
    d.append(draw.Text("5", 11, p2x - 14, p2y - 12, fill=GREEN_EQUAL, font_weight="bold"))
    d.append(draw.Text("6", 11, p2x + 12, p2y - 12, fill=TEXT_COLOR))
    d.append(draw.Text("7", 11, p2x - 12, p2y + 14, fill=TEXT_COLOR))
    d.append(draw.Text("8", 11, p2x + 12, p2y + 14, fill=TEXT_COLOR))
    d.append(
        draw.Text(
            "Внутрішні різносторонні кути (∠4 = ∠5)",
            13,
            180,
            210,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_75_78() -> draw.Drawing:
    # Parallel lines criteria
    d = create_canvas(360, 200)
    y1, y2 = 60, 140
    draw_seg(d, 40, y1, 320, y1, color=BLUE_PRIMARY, w=2.5)
    draw_seg(d, 40, y2, 320, y2, color=BLUE_PRIMARY, w=2.5)
    draw_seg(d, 90, 25, 250, 175, color=RED_AUX, w=2)
    p1x, p1y = 130, y1
    p2x, p2y = 210, y2
    draw_angle_arc(d, p1x, p1y, 22, -45, 0, color=GREEN_EQUAL)
    draw_angle_arc(d, p2x, p2y, 22, 135, 180, color=GREEN_EQUAL)
    d.append(draw.Text("α", 12, p1x + 28, p1y + 12, fill=GREEN_EQUAL, font_weight="bold"))
    d.append(draw.Text("α", 12, p2x - 28, p2y - 12, fill=GREEN_EQUAL, font_weight="bold"))
    d.append(
        draw.Text(
            "a ∥ b  ⟺  внутрішні різносторонні кути рівні",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_79_80() -> draw.Drawing:
    # Euclid's parallel postulate
    d = create_canvas(360, 180)
    draw_seg(d, 40, 130, 320, 130, color=BLUE_PRIMARY, w=2.5)
    d.append(draw.Text("a", 14, 330, 135, fill=BLUE_PRIMARY, font_style="italic"))
    px, py = 180, 50
    draw_pt(d, px, py, "M", "top")
    draw_seg(d, 40, py, 320, py, color=GREEN_EQUAL, w=2.5)
    d.append(draw.Text("b ∥ a", 14, 330, py + 5, fill=GREEN_EQUAL, font_style="italic"))
    d.append(
        draw.Text(
            "Через точку M можна провести тільки одну пряму b ∥ a",
            13,
            180,
            165,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_81_82() -> draw.Drawing:
    # Angles with parallel sides
    d = create_canvas(360, 200)
    # Angle 1
    o1x, o1y = 60, 140
    draw_seg(d, o1x, o1y, o1x + 100, o1y, color=BLUE_PRIMARY, w=2.5)
    draw_seg(d, o1x, o1y, o1x + 70, o1y - 90, color=BLUE_PRIMARY, w=2.5)
    draw_angle_arc(d, o1x, o1y, 28, 0, 52, color=BLUE_PRIMARY)
    draw_pt(d, o1x, o1y, "O", "bottom-left")
    # Angle 2 (parallel sides)
    o2x, o2y = 190, 110
    draw_seg(d, o2x, o2y, o2x + 100, o2y, color=GREEN_EQUAL, w=2.5)
    draw_seg(d, o2x, o2y, o2x + 70, o2y - 90, color=GREEN_EQUAL, w=2.5)
    draw_angle_arc(d, o2x, o2y, 28, 0, 52, color=GREEN_EQUAL)
    draw_pt(d, o2x, o2y, "O₁", "bottom-left")
    d.append(
        draw.Text(
            "Співнапрямлені сторони ⟹ ∠O = ∠O₁",
            13,
            180,
            180,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_83_84() -> draw.Drawing:
    # Angles with perpendicular sides
    d = create_canvas(360, 200)
    ox, oy = 80, 140
    draw_seg(d, ox, oy, ox + 110, oy, color=BLUE_PRIMARY, w=2)
    draw_seg(d, ox, oy, ox + 60, oy - 90, color=BLUE_PRIMARY, w=2)
    draw_angle_arc(d, ox, oy, 25, 0, 56, color=BLUE_PRIMARY)
    o2x, o2y = 220, 140
    draw_seg(d, o2x, o2y, o2x, oy - 100, color=RED_AUX, w=2)
    draw_seg(d, o2x, o2y, o2x + 80, oy - 45, color=RED_AUX, w=2)
    draw_angle_arc(d, o2x, o2y, 25, -34, 90, color=RED_AUX)
    d.append(
        draw.Text(
            "Взаємно перпендикулярні сторони: кути рівні",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


def make_fig_85() -> draw.Drawing:
    # Sum of angles in a triangle = 180
    d = create_canvas(360, 220)
    ax, ay = 60, 160
    bx, by = 300, 160
    cx, cy = 150, 55
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#eff6ff", stroke=LINE_COLOR, stroke_width=2
        )
    )
    # Parallel line through C
    draw_seg(d, 30, cy, 330, cy, color=RED_AUX, w=2, dashed=True)
    d.append(draw.Text("l ∥ AB", 12, 340, cy + 4, fill=RED_AUX, font_style="italic"))
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom-right")
    draw_pt(d, cx, cy, "C", "bottom")
    # Angles at A, B, C
    draw_angle_arc(d, ax, ay, 25, 0, 48, color=BLUE_PRIMARY)
    draw_angle_arc(d, bx, by, 25, 145, 180, color=GREEN_EQUAL)
    draw_angle_arc(d, cx, cy, 25, -132, -35, color=PURPLE_AUX)
    # Alternate angles at C
    draw_angle_arc(d, cx, cy, 22, -180, -132, color=BLUE_PRIMARY)
    draw_angle_arc(d, cx, cy, 22, -35, 0, color=GREEN_EQUAL)
    d.append(
        draw.Text(
            "∠A + ∠B + ∠C = 180°",
            14,
            180,
            205,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_86() -> draw.Drawing:
    # Exterior angle of a triangle
    d = create_canvas(360, 200)
    ax, ay = 50, 140
    bx, by = 240, 140
    cx, cy = 160, 45
    d.append(
        draw.Lines(
            ax, ay, bx, by, cx, cy, close=True, fill="#f0fdf4", stroke=LINE_COLOR, stroke_width=2
        )
    )
    # Extend AB to D
    draw_seg(d, bx, by, 320, by, color=LINE_COLOR, w=2, dashed=True)
    draw_pt(d, ax, ay, "A", "bottom-left")
    draw_pt(d, bx, by, "B", "bottom")
    draw_pt(d, cx, cy, "C", "top")
    draw_pt(d, 310, by, "D", "bottom")
    draw_angle_arc(d, ax, ay, 25, 0, 42, color=BLUE_PRIMARY)
    draw_angle_arc(d, cx, cy, 25, -138, -50, color=GREEN_EQUAL)
    draw_angle_arc(d, bx, by, 30, 50, 180, color=RED_AUX)
    d.append(
        draw.Text(
            "зовнішній ∠CBD = ∠A + ∠C",
            13,
            180,
            185,
            text_anchor="middle",
            fill=RED_AUX,
            font_weight="bold",
        )
    )
    return d


def make_fig_87_88() -> draw.Drawing:
    # Sum of polygon angles: (n - 2) * 180
    d = create_canvas(360, 200)
    pts = [(80, 150), (60, 80), (160, 40), (280, 60), (270, 150)]
    poly_pts = [c for pt in pts for c in pt]
    d.append(draw.Lines(*poly_pts, close=True, fill="#faf5ff", stroke=LINE_COLOR, stroke_width=2))
    # Triangulation from vertex 0
    p0 = pts[0]
    draw_seg(d, p0[0], p0[1], pts[2][0], pts[2][1], color=PURPLE_AUX, w=1.5, dashed=True)
    draw_seg(d, p0[0], p0[1], pts[3][0], pts[3][1], color=PURPLE_AUX, w=1.5, dashed=True)
    for i, (x, y) in enumerate(pts):
        draw_pt(d, x, y, f"A_{i + 1}", "top" if y < 100 else "bottom")
    d.append(
        draw.Text(
            "Сума кутів n-кутника = 180° · (n - 2)",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
            font_weight="bold",
        )
    )
    return d


def make_fig_89() -> draw.Drawing:
    # Lobachevsky geometry
    d = create_canvas(360, 200)
    draw_seg(d, 30, 150, 330, 150, color=LINE_COLOR, w=2.5)
    d.append(draw.Text("a", 14, 340, 155, fill=LINE_COLOR, font_style="italic"))
    px, py = 180, 50
    draw_pt(d, px, py, "C", "top")
    draw_seg(d, 40, py - 10, 320, py + 30, color=BLUE_PRIMARY, w=2)
    draw_seg(d, 40, py + 15, 320, py + 10, color=GREEN_EQUAL, w=2)
    draw_seg(d, 40, py + 35, 320, py - 5, color=PURPLE_AUX, w=2)
    d.append(
        draw.Text(
            "Аксіома Лобачевського: пучок неперетинних прямих",
            13,
            180,
            185,
            text_anchor="middle",
            fill=TEXT_COLOR,
        )
    )
    return d


# ==============================================================================
# FIGURE METADATA REGISTRY
# ==============================================================================

FIGURES_REGISTRY: list[dict] = [
    {
        "num": 1,
        "page": 9,
        "sec": "§ 3. Пряма лінія",
        "title": "Пряма лінія, проведена через дві точки",
        "caption": "Пряма AB, безмежна в обидва боки",
        "didactic": "Показано безмежність прямої пунктиром на кінцях. Точки A і B визначають пряму однозначно.",
        "gen": make_fig_1,
        "w": 340,
        "h": 100,
    },
    {
        "num": 2,
        "page": 9,
        "sec": "§ 4. Відрізок і промінь",
        "title": "Відрізок прямої CD",
        "caption": "Відрізок CD із двома кінцями",
        "didactic": "Відрізок обмежений двома точками C і D, має фіксовану вимірну довжину.",
        "gen": make_fig_2,
        "w": 340,
        "h": 100,
    },
    {
        "num": 3,
        "page": 9,
        "sec": "§ 4. Відрізок і промінь",
        "title": "Промінь EF (півпряма)",
        "caption": "Промінь з початком у точці E",
        "didactic": "Має початкову точку E, але нескінченно продовжується в один бік через точку F.",
        "gen": make_fig_3,
        "w": 340,
        "h": 100,
    },
    {
        "num": 4,
        "page": 10,
        "sec": "§ 5. Рівність відрізків",
        "title": "Рівність відрізків способом накладання",
        "caption": "AB = CD при суміщенні кінців",
        "didactic": "Два відрізки рівні, якщо при суміщенні точки A з C точка B збігається з D.",
        "gen": make_fig_4,
        "w": 360,
        "h": 130,
    },
    {
        "num": 5,
        "page": 10,
        "sec": "§ 6. Сума відрізків",
        "title": "Додавання відрізків на одній прямій",
        "caption": "MQ = MN + NP + PQ = AB + CD + EF",
        "didactic": "Сума відрізків утворюється послідовним відкладанням частин в одному напрямку.",
        "gen": make_fig_5,
        "w": 380,
        "h": 140,
    },
    {
        "num": 6,
        "page": 11,
        "sec": "§ 8. Коло і круг",
        "title": "Коло та його основні елементи",
        "caption": "Центр O, радіус OA, хорда EF, діаметр, сектор",
        "didactic": "Показано центр O, радіус, хорду та діаметр як найбільшу хорду.",
        "gen": make_fig_6,
        "w": 360,
        "h": 240,
    },
    {
        "num": 7,
        "page": 11,
        "sec": "§ 10. Сума дуг",
        "title": "Додавання дуг на колі",
        "caption": "Дуга MP = Дуга MN + Дуга NP",
        "didactic": "Додавання дуг одного кола аналогічне додаванню відрізків на прямій.",
        "gen": make_fig_7,
        "w": 360,
        "h": 220,
    },
    {
        "num": 8,
        "page": 13,
        "sec": "§ 13. Означення кута",
        "title": "Кут AOB та його сторони",
        "caption": "Вершина O, сторони OA і OB",
        "didactic": "Кут утворений двома променями, що виходять з однієї точки. Внутрішня область виділена.",
        "gen": make_fig_8,
        "w": 340,
        "h": 200,
    },
    {
        "num": 9,
        "page": 13,
        "sec": "§ 14. Рівність кутів",
        "title": "Рівність кутів способом накладання",
        "caption": "∠AOB = ∠A₁O₁B₁",
        "didactic": "При накладанні вершин і однієї сторони другі сторони повністю суміщаються.",
        "gen": make_fig_9,
        "w": 360,
        "h": 180,
    },
    {
        "num": 10,
        "page": 14,
        "sec": "§ 15. Додавання кутів",
        "title": "Додавання кутів зі спільною вершиною",
        "caption": "∠AOB = ∠AOC + ∠COB",
        "didactic": "Два кути мають спільну вершину і спільну сторону OC.",
        "gen": make_fig_10,
        "w": 340,
        "h": 200,
    },
    {
        "num": 11,
        "page": 14,
        "sec": "§ 16. Розгорнутий кут",
        "title": "Розгорнутий кут",
        "caption": "Сторони OA і OB утворюють одну пряму",
        "didactic": "Сторони є доповняльними променями. Величина розгорнутого кута становить 180°.",
        "gen": make_fig_11,
        "w": 340,
        "h": 120,
    },
    {
        "num": 12,
        "page": 14,
        "sec": "§ 16. Прямий кут",
        "title": "Прямий кут (половина розгорнутого)",
        "caption": "Прямий кут = 90° (d)",
        "didactic": "Половина розгорнутого кута. Позначається квадратним маркером.",
        "gen": make_fig_12,
        "w": 300,
        "h": 200,
    },
    {
        "num": 13,
        "page": 14,
        "sec": "§ 16. Повний кут",
        "title": "Повний кут (повний оберт променя)",
        "caption": "Повний кут = 360° (4d)",
        "didactic": "Промінь робить повний оберт навколо початкової точки O.",
        "gen": make_fig_13,
        "w": 320,
        "h": 180,
    },
    {
        "num": 14,
        "page": 15,
        "sec": "§ 17. Центральний кут",
        "title": "Центральний кут і відповідна дуга",
        "caption": "Центральний кут спирається на дугу AB",
        "didactic": "Вершина кута лежить у центрі кола. Сторони вирізають дугу на колі.",
        "gen": make_fig_14_15,
        "w": 360,
        "h": 220,
    },
    {
        "num": 16,
        "page": 16,
        "sec": "§ 18-20. Градуси і транспортир",
        "title": "Градусна шкала і вимірювання кутів транспортиром",
        "caption": "Транспортир з градусною шкалою",
        "didactic": "Коло поділене на 360 частин (градусів). Півколо транспортира містить 180°.",
        "gen": make_fig_16_17,
        "w": 360,
        "h": 220,
    },
    {
        "num": 18,
        "page": 16,
        "sec": "§ 21. Види кутів",
        "title": "Класифікація кутів: гострий, прямий, тупий",
        "caption": "Гострий < 90°, Прямий = 90°, Тупий > 90°",
        "didactic": "Порівняння кутів із прямим кутом (еталоном 90°).",
        "gen": make_fig_18,
        "w": 380,
        "h": 140,
    },
    {
        "num": 19,
        "page": 17,
        "sec": "§ 22. Суміжні кути",
        "title": "Суміжні кути та їхня властивість",
        "caption": "α + β = 180°",
        "didactic": "Мають одну спільну сторону, а дві інші утворюють пряму лінію. Сума завжди 180°.",
        "gen": make_fig_19_21,
        "w": 360,
        "h": 180,
    },
    {
        "num": 22,
        "page": 18,
        "sec": "§ 23. Перпендикуляр",
        "title": "Перпендикуляр до прямої та його основа",
        "caption": "OB ⊥ AC, O — основа перпендикуляра",
        "didactic": "Пряма, що утворює з даною прямою рівні суміжні кути (по 90° кожен).",
        "gen": make_fig_22,
        "w": 340,
        "h": 180,
    },
    {
        "num": 23,
        "page": 18,
        "sec": "§ 25. Вертикальні кути",
        "title": "Вертикальні кути при перетині прямих",
        "caption": "∠1 = ∠3, ∠2 = ∠4",
        "didactic": "Сторони одного кута є продовженням сторін другого. Вертикальні кути рівні.",
        "gen": make_fig_23,
        "w": 360,
        "h": 200,
    },
    {
        "num": 24,
        "page": 20,
        "sec": "§ 26. Бісектриси кутів",
        "title": "Кут між бісектрисами суміжних кутів",
        "caption": "Бісектриси утворюють прямий кут 90°",
        "didactic": "Половина від суми 180° дорівнює строго 90°.",
        "gen": make_fig_24_27,
        "w": 360,
        "h": 200,
    },
    {
        "num": 28,
        "page": 21,
        "sec": "§ 30-31. Многокутник",
        "title": "Опуклий многокутник і його діагоналі",
        "caption": "Многокутник ABCDE з діагоналями",
        "didactic": "Замкнена ламана лінія. Діагоналі сполучають несусідні вершини.",
        "gen": make_fig_28_30,
        "w": 360,
        "h": 200,
    },
    {
        "num": 31,
        "page": 22,
        "sec": "§ 32. Види трикутників",
        "title": "Рівнобедрений та рівносторонній трикутники",
        "caption": "Види трикутників за сторонами",
        "didactic": "У рівнобедреному дві сторони рівні, у рівносторонньому — всі три рівні.",
        "gen": make_fig_31_35,
        "w": 380,
        "h": 180,
    },
    {
        "num": 36,
        "page": 23,
        "sec": "§ 32. Прямокутний трикутник",
        "title": "Елементи прямокутного трикутника",
        "caption": "Катети a, b та гіпотенуза c",
        "didactic": "Катети утворюють прямий кут, гіпотенуза лежить навпроти прямого кута.",
        "gen": make_fig_36,
        "w": 340,
        "h": 200,
    },
    {
        "num": 37,
        "page": 23,
        "sec": "§ 33. Лінії в трикутнику",
        "title": "Висота, медіана та бісектриса трикутника",
        "caption": "CH — висота, CM — медіана, CL — бісектриса",
        "didactic": "Висота перпендикулярна до сторони, медіана ділить сторону навпіл, бісектриса ділить кут навпіл.",
        "gen": make_fig_37_38,
        "w": 360,
        "h": 200,
    },
    {
        "num": 39,
        "page": 24,
        "sec": "§ 34. Властивості рівнобедреного трикутника",
        "title": "Рівність кутів при основі та вісь симетрії",
        "caption": "∠A = ∠C, BD — бісектриса, висота і медіана",
        "didactic": "У рівнобедреному трикутнику бісектриса кута при вершині є медіаною, висотою і віссю симетрії.",
        "gen": make_fig_39_41,
        "w": 340,
        "h": 220,
    },
    {
        "num": 42,
        "page": 25,
        "sec": "§ 38. Перша ознака рівності трикутників",
        "title": "Перша ознака рівності трикутників (САК)",
        "caption": "За двома сторонами і кутом між ними",
        "didactic": "Якщо AB=A₁B₁, AC=A₁C₁ та ∠A=∠A₁, трикутники рівні за першою ознакою.",
        "gen": make_fig_42_44,
        "w": 380,
        "h": 190,
    },
    {
        "num": 45,
        "page": 27,
        "sec": "§ 38. Друга ознака рівності трикутників",
        "title": "Друга ознака рівності трикутників (АСА)",
        "caption": "За стороною і двома прилеглими кутами",
        "didactic": "Якщо AC=A₁C₁, ∠A=∠A₁ та ∠C=∠C₁, трикутники рівні за другою ознакою.",
        "gen": make_fig_45_46,
        "w": 380,
        "h": 190,
    },
    {
        "num": 47,
        "page": 28,
        "sec": "§ 38. Третя ознака рівності трикутників",
        "title": "Третя ознака рівності трикутників (ССС)",
        "caption": "За трьома сторонами",
        "didactic": "Якщо всі три пари сторін відповідно рівні, трикутники рівні.",
        "gen": make_fig_47_50,
        "w": 380,
        "h": 190,
    },
    {
        "num": 51,
        "page": 29,
        "sec": "§ 42. Співвідношення сторін і кутів",
        "title": "Співвідношення між сторонами і кутами трикутника",
        "caption": "Проти більшої сторони лежить більший кут",
        "didactic": "У будь-якому трикутнику проти більшої сторони лежить більший кут, і навпаки.",
        "gen": make_fig_51_53,
        "w": 340,
        "h": 200,
    },
    {
        "num": 54,
        "page": 31,
        "sec": "§ 45. Нерівність трикутника",
        "title": "Нерівність трикутника",
        "caption": "AB < AC + CB",
        "didactic": "Кожна сторона трикутника завжди менша за суму двох інших сторін.",
        "gen": make_fig_54_57,
        "w": 340,
        "h": 180,
    },
    {
        "num": 58,
        "page": 33,
        "sec": "§ 48. Перпендикуляр і похилі",
        "title": "Перпендикуляр і похилі, проведені з однієї точки",
        "caption": "Рівним проекціям відповідають рівні похилі",
        "didactic": "Перпендикуляр завжди коротший за будь-яку похилу. Рівні похилі мають рівні проекції.",
        "gen": make_fig_58_63,
        "w": 360,
        "h": 210,
    },
    {
        "num": 64,
        "page": 36,
        "sec": "§ 56. Геометричні місця точок",
        "title": "Серединний перпендикуляр відрізка як ГМТ",
        "caption": "Кожна точка перпендикуляра рівновіддалена від A і B",
        "didactic": "Геометричне місце точок, рівновіддалених від кінців відрізка — серединний перпендикуляр.",
        "gen": make_fig_64_65,
        "w": 360,
        "h": 200,
    },
    {
        "num": 66,
        "page": 37,
        "sec": "§ 58-60. Побудова циркулем і лінійкою",
        "title": "Побудова бісектриси кута за допомогою циркуля",
        "caption": "Засічки циркуля однакового радіуса",
        "didactic": "Проводимо дугу з вершини O, потім дві дуги однакового радіуса з точок D і E.",
        "gen": make_fig_66_68,
        "w": 360,
        "h": 200,
    },
    {
        "num": 69,
        "page": 38,
        "sec": "§ 61. Побудова перпендикуляра",
        "title": "Побудова перпендикуляра до прямої з точки поза нею",
        "caption": "Побудова перпендикуляра CP ⊥ AB циркулем",
        "didactic": "Коло з центром C перетинає пряму в A і B; засічки з A і B дають напрям перпендикуляра.",
        "gen": make_fig_69_70,
        "w": 360,
        "h": 200,
    },
    {
        "num": 73,
        "page": 42,
        "sec": "§ 69. Паралельні прямі і січна",
        "title": "Кути, утворені двома прямими і січною",
        "caption": "Внутрішні різносторонні, відповідні, односторонні",
        "didactic": "Вісім кутів: внутрішні різносторонні (3 і 6, 4 і 5), відповідні (1 і 5), односторонні (4 і 6).",
        "gen": make_fig_73_74,
        "w": 360,
        "h": 220,
    },
    {
        "num": 75,
        "page": 43,
        "sec": "§ 69. Ознаки паралельності",
        "title": "Ознаки паралельності двох прямих",
        "caption": "a ∥ b якщо внутрішні різносторонні кути рівні",
        "didactic": "Якщо при перетині двох прямих січною внутрішні різносторонні кути рівні, прямі паралельні.",
        "gen": make_fig_75_78,
        "w": 360,
        "h": 200,
    },
    {
        "num": 79,
        "page": 44,
        "sec": "§ 71. Аксіома паралельних прямих",
        "title": "Аксіома паралельних прямих Евкліда",
        "caption": "Через точку поза прямою проходить лише одна паралельна",
        "didactic": "Фундаментальна аксіома евклідової геометрії, основа теорії паралельності.",
        "gen": make_fig_79_80,
        "w": 360,
        "h": 180,
    },
    {
        "num": 81,
        "page": 45,
        "sec": "§ 76. Кути з паралельними сторонами",
        "title": "Кути з відповідно паралельними сторонами",
        "caption": "Співнапрямлені сторони утворюють рівні кути",
        "didactic": "Якщо сторони двох кутів паралельні і напрямлені в один бік, ці кути рівні.",
        "gen": make_fig_81_82,
        "w": 360,
        "h": 200,
    },
    {
        "num": 83,
        "page": 46,
        "sec": "§ 77. Кути з перпендикулярними сторонами",
        "title": "Кути з взаємно перпендикулярними сторонами",
        "caption": "Гострі кути з перпендикулярними сторонами рівні",
        "didactic": "Два гострі кути, сторони яких взаємно перпендикулярні, рівні між собою.",
        "gen": make_fig_83_84,
        "w": 360,
        "h": 200,
    },
    {
        "num": 85,
        "page": 47,
        "sec": "§ 78. Сума кутів трикутника",
        "title": "Теорема про суму кутів трикутника (180°)",
        "caption": "∠A + ∠B + ∠C = 180° (проведення l ∥ AB)",
        "didactic": "Доведення: через вершину C проводимо пряму, паралельну основі AB. Утворюється розгорнутий кут.",
        "gen": make_fig_85,
        "w": 360,
        "h": 220,
    },
    {
        "num": 86,
        "page": 47,
        "sec": "§ 79. Зовнішній кут трикутника",
        "title": "Властивість зовнішнього кута трикутника",
        "caption": "Зовнішній кут дорівнює сумі двох внутрішніх не суміжних",
        "didactic": "Зовнішній кут ∠CBD = 180° - ∠B = ∠A + ∠C.",
        "gen": make_fig_86,
        "w": 360,
        "h": 200,
    },
    {
        "num": 87,
        "page": 47,
        "sec": "§ 80. Сума кутів многокутника",
        "title": "Сума кутів опуклого многокутника",
        "caption": "180° · (n - 2) при тріангуляції",
        "didactic": "Многокутник із однієї вершини розбивається на (n - 2) трикутники, сума кутів кожного 180°.",
        "gen": make_fig_87_88,
        "w": 360,
        "h": 200,
    },
    {
        "num": 89,
        "page": 49,
        "sec": "§ 84-85. Геометрія Лобачевського",
        "title": "Неєвклідова геометрія Лобачевського",
        "caption": "Пучок прямих через точку C, що не перетинають пряму a",
        "didactic": "Альтернативна аксіома: через точку поза прямою проходить більше ніж одна паралельна пряма.",
        "gen": make_fig_89,
        "w": 360,
        "h": 200,
    },
]


def populate_figures():
    db = BookDatabase()
    print("==================================================")
    print("🎨 Generating & Storing Kiselev Vector Figures in DB")
    print(f"Total catalog entries: {len(FIGURES_REGISTRY)}")
    print("==================================================")

    saved_count = 0
    for item in FIGURES_REGISTRY:
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
        saved_count += 1
        print(
            f"  ✓ Saved {fig_id} (Рис. {fig_num}): '{item['title'][:40]}...' (Стор. {item['page']})"
        )

    total_in_db = db.count_figures(BOOK_ID)
    print("==================================================")
    print(f"🎉 Successfully generated & stored {saved_count} figures in book_kb.db!")
    print(f"📊 Total figures in SQLite table 'book_figures': {total_in_db}")
    print("==================================================")


if __name__ == "__main__":
    populate_figures()
