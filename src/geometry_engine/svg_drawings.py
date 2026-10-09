"""Pure Python vector geometry drawings generator using drawsvg.

Fast (< 0.5ms), crisp, responsive SVG drawings without Cartesian coordinates noise.
Built specifically for 7th grade planimetry in Marimo.
"""

from __future__ import annotations

import math
from functools import lru_cache

import drawsvg as draw

from .db import BookDatabase, BookFigure


def draw_angle(alpha_deg: float, width: int = 340, height: int = 220) -> draw.Drawing:
    """Генерує кут AOB із рухомим променем OA та фіксованим OB."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=10))

    ox, oy = 50, height - 50
    ray_len = 180

    # Фіксований промінь OB (горизонтальний)
    d.append(draw.Line(ox, oy, ox + ray_len, oy, stroke="#334155", stroke_width=2.5))
    d.append(draw.Text("B", 14, ox + ray_len + 8, oy + 5, fill="#334155", font_weight="bold"))

    # Рухомий промінь OA
    rad = math.radians(alpha_deg)
    ax = ox + ray_len * math.cos(rad)
    ay = oy - ray_len * math.sin(rad)
    d.append(draw.Line(ox, oy, ax, ay, stroke="#2563eb", stroke_width=3))
    d.append(draw.Text("A", 14, ax + 5, ay - 5, fill="#2563eb", font_weight="bold"))

    # Вершина O
    d.append(draw.Circle(ox, oy, 4.5, fill="#0f172a"))
    d.append(draw.Text("O", 15, ox - 20, oy + 5, fill="#0f172a", font_weight="bold"))

    # Дуга кута
    arc_r = 45
    # drawsvg Arc: cx, cy, r, start_deg, end_deg
    d.append(draw.Arc(ox, oy, arc_r, -alpha_deg, 0, stroke="#2563eb", stroke_width=2, fill="none"))

    # Підпис кута
    label_rad = math.radians(alpha_deg / 2)
    lx = ox + (arc_r + 20) * math.cos(label_rad)
    ly = oy - (arc_r + 20) * math.sin(label_rad)
    d.append(draw.Text(f"{alpha_deg:.0f}°", 13, lx, ly, fill="#2563eb", font_weight="bold"))

    return d


def draw_adjacent_angles(alpha_deg: float, width: int = 360, height: int = 200) -> draw.Drawing:
    """Генерує суміжні кути α та β = 180° - α на спільній прямій."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=10))

    ox, oy = width // 2, height - 40
    ray_len = 130

    # Горизонтальна пряма (доповняльні промені OA і OB)
    d.append(draw.Line(ox - ray_len, oy, ox + ray_len, oy, stroke="#334155", stroke_width=2.5))
    d.append(draw.Text("A", 14, ox - ray_len - 18, oy + 5, fill="#334155", font_weight="bold"))
    d.append(draw.Text("B", 14, ox + ray_len + 8, oy + 5, fill="#334155", font_weight="bold"))

    # Спільний рухомий промінь OC
    rad = math.radians(alpha_deg)
    cx = ox + ray_len * math.cos(rad)
    cy = oy - ray_len * math.sin(rad)
    d.append(draw.Line(ox, oy, cx, cy, stroke="#2563eb", stroke_width=3))
    d.append(draw.Text("C", 14, cx + 5, cy - 5, fill="#2563eb", font_weight="bold"))

    # Вершина O
    d.append(draw.Circle(ox, oy, 4.5, fill="#0f172a"))
    d.append(draw.Text("O", 15, ox - 6, oy + 22, fill="#0f172a", font_weight="bold"))

    # Дуга α (кут COB)
    d.append(draw.Arc(ox, oy, 40, -alpha_deg, 0, stroke="#2563eb", stroke_width=2, fill="none"))
    d.append(
        draw.Text(f"α = {alpha_deg:.0f}°", 13, ox + 35, oy - 20, fill="#2563eb", font_weight="bold")
    )

    # Дуга β (кут AOC)
    beta_deg = 180 - alpha_deg
    d.append(draw.Arc(ox, oy, 48, -180, -alpha_deg, stroke="#dc2626", stroke_width=2, fill="none"))
    d.append(
        draw.Text(f"β = {beta_deg:.0f}°", 13, ox - 95, oy - 20, fill="#dc2626", font_weight="bold")
    )

    return d


def draw_vertical_angles(alpha_deg: float, width: int = 360, height: int = 240) -> draw.Drawing:
    """Генерує вертикальні кути (модель ножиць з двома прямими)."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=10))

    ox, oy = width // 2, height // 2
    r_len = 130

    # Пряма 1 (горизонтальна під кутом 15°)
    b_rad = math.radians(15)
    p1_x, p1_y = ox - r_len * math.cos(b_rad), oy + r_len * math.sin(b_rad)
    p2_x, p2_y = ox + r_len * math.cos(b_rad), oy - r_len * math.sin(b_rad)
    d.append(draw.Line(p1_x, p1_y, p2_x, p2_y, stroke="#64748b", stroke_width=2.5))

    # Пряма 2 (перехрещена під кутом alpha + 15°)
    a_rad = math.radians(alpha_deg + 15)
    q1_x, q1_y = ox - r_len * math.cos(a_rad), oy + r_len * math.sin(a_rad)
    q2_x, q2_y = ox + r_len * math.cos(a_rad), oy - r_len * math.sin(a_rad)
    d.append(draw.Line(q1_x, q1_y, q2_x, q2_y, stroke="#2563eb", stroke_width=3))

    # Вершина
    d.append(draw.Circle(ox, oy, 4.5, fill="#0f172a"))
    d.append(draw.Text("O", 14, ox - 18, oy - 10, fill="#0f172a", font_weight="bold"))

    # Підписи кутів
    d.append(
        draw.Text(
            f"∠1 = {alpha_deg:.0f}°", 12, ox + 35, oy - 20, fill="#2563eb", font_weight="bold"
        )
    )
    d.append(
        draw.Text(
            f"∠3 = {alpha_deg:.0f}°", 12, ox - 90, oy + 25, fill="#2563eb", font_weight="bold"
        )
    )
    beta = 180 - alpha_deg
    d.append(
        draw.Text(f"∠2 = {beta:.0f}°", 12, ox - 30, oy - 45, fill="#dc2626", font_weight="bold")
    )
    d.append(
        draw.Text(f"∠4 = {beta:.0f}°", 12, ox - 30, oy + 55, fill="#dc2626", font_weight="bold")
    )

    return d


def draw_angle_bisector(alpha_deg: float, width: int = 340, height: int = 220) -> draw.Drawing:
    """Генерує кут із бісектрисою, яка ділить його на α/2."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=10))

    ox, oy = 50, height - 50
    ray_len = 170

    # Сторона 1 (горизонтальна)
    d.append(draw.Line(ox, oy, ox + ray_len, oy, stroke="#334155", stroke_width=2.5))
    d.append(draw.Text("B", 14, ox + ray_len + 8, oy + 5, fill="#334155", font_weight="bold"))

    # Сторона 2
    rad = math.radians(alpha_deg)
    ax, ay = ox + ray_len * math.cos(rad), oy - ray_len * math.sin(rad)
    d.append(draw.Line(ox, oy, ax, ay, stroke="#334155", stroke_width=2.5))
    d.append(draw.Text("A", 14, ax + 5, ay - 5, fill="#334155", font_weight="bold"))

    # Бісектриса (зелена лінія)
    half_rad = math.radians(alpha_deg / 2)
    bx, by = ox + ray_len * math.cos(half_rad), oy - ray_len * math.sin(half_rad)
    d.append(draw.Line(ox, oy, bx, by, stroke="#16a34a", stroke_width=3, stroke_dasharray="6,4"))
    d.append(draw.Text("L (бісектриса)", 13, bx + 5, by - 5, fill="#16a34a", font_weight="bold"))

    # Вершина
    d.append(draw.Circle(ox, oy, 4, fill="#0f172a"))
    d.append(draw.Text("O", 15, ox - 18, oy + 5, fill="#0f172a", font_weight="bold"))

    # Підписи рівних половинок
    d.append(
        draw.Text(f"{alpha_deg / 2:.1f}°", 11, ox + 55, oy - 12, fill="#16a34a", font_weight="bold")
    )
    d.append(
        draw.Text(f"{alpha_deg / 2:.1f}°", 11, ox + 45, oy - 35, fill="#16a34a", font_weight="bold")
    )

    return d


def draw_triangle(
    a_side: float = 140,
    b_side: float = 120,
    angle_c_deg: float = 60,
    width: int = 360,
    height: int = 240,
    title: str = "Трикутник ABC",
) -> draw.Drawing:
    """Генерує трикутник ABC за двома сторонами та кутом між ними (ознака С-К-С)."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=10))

    cx, cy = 60, height - 50

    # Вершина C — в точці (cx, cy)
    # Сторона CB вздовж осі X довжиною a_side
    bx, by = cx + a_side, cy

    # Сторона CA під кутом angle_c_deg довжиною b_side
    rad = math.radians(angle_c_deg)
    ax, ay = cx + b_side * math.cos(rad), cy - b_side * math.sin(rad)

    # Заливка трикутника напівпрозорим кольором
    points = [cx, cy, bx, by, ax, ay]
    d.append(draw.Lines(*points, close=True, fill="#e0f2fe", stroke="#0284c7", stroke_width=2.5))

    # Вершини
    for px, py, name, pos in [
        (ax, ay, "A", (-5, -10)),
        (bx, by, "B", (8, 5)),
        (cx, cy, "C", (-18, 5)),
    ]:
        d.append(draw.Circle(px, py, 4, fill="#0f172a"))
        d.append(draw.Text(name, 14, px + pos[0], py + pos[1], fill="#0f172a", font_weight="bold"))

    # Дуга кута C
    d.append(draw.Arc(cx, cy, 32, -angle_c_deg, 0, stroke="#0284c7", stroke_width=2, fill="none"))
    d.append(
        draw.Text(
            f"∠C = {angle_c_deg:.0f}°", 12, cx + 38, cy - 15, fill="#0284c7", font_weight="bold"
        )
    )

    # Підписи сторін
    d.append(draw.Text(f"a = {a_side:.0f}", 12, (cx + bx) / 2 - 10, cy + 18, fill="#475569"))
    d.append(
        draw.Text(f"b = {b_side:.0f}", 12, (cx + ax) / 2 - 25, (cy + ay) / 2 - 5, fill="#475569")
    )

    if title:
        d.append(draw.Text(title, 13, 15, 25, fill="#0f172a", font_weight="bold"))

    return d


def draw_congruence_showcase(
    criterion: str = "SAS",
    width: int = 560,
    height: int = 240,
) -> draw.Drawing:
    """Генерує креслення пари рівних трикутників ABC та A₁B₁C₁ із позначенням ознаки (САК, АСА, ССС)."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=12))

    # Геометрія еталонного трикутника
    # C в (0, 0), B на осі X (a=120), A під кутом 55° (b=100)
    a = 120
    b = 100
    angle_c = 55.0
    rad_c = math.radians(angle_c)
    ax_rel, ay_rel = b * math.cos(rad_c), -b * math.sin(rad_c)

    # Дві позиції на полотні: лівий трикутник (ABC) і правий (A1B1C1)
    t1_c = (45, height - 45)
    t2_c = (305, height - 45)

    triangles = [
        {"base": t1_c, "prefix": "", "color": "#0284c7", "fill": "#e0f2fe"},
        {"base": t2_c, "prefix": "₁", "color": "#ea580c", "fill": "#ffedd5"},
    ]

    for t in triangles:
        cx, cy = t["base"]
        bx, by = cx + a, cy
        ax, ay = cx + ax_rel, cy + ay_rel
        col = t["color"]
        pref = t["prefix"]

        # Заливка
        d.append(
            draw.Lines(
                cx, cy, bx, by, ax, ay, close=True, fill=t["fill"], stroke=col, stroke_width=2.5
            )
        )

        # Вершини
        for px, py, name, pos in [
            (ax, ay, f"A{pref}", (-6, -10)),
            (bx, by, f"B{pref}", (8, 5)),
            (cx, cy, f"C{pref}", (-18, 5)),
        ]:
            d.append(draw.Circle(px, py, 4, fill="#0f172a"))
            d.append(
                draw.Text(name, 13, px + pos[0], py + pos[1], fill="#0f172a", font_weight="bold")
            )

        # Позначення за ознакою
        if criterion in ["SAS", "САК"]:
            # Сторона AC (1 засічка)
            mid_ac_x, mid_ac_y = (cx + ax) / 2, (cy + ay) / 2
            d.append(
                draw.Line(
                    mid_ac_x - 4,
                    mid_ac_y - 4,
                    mid_ac_x + 4,
                    mid_ac_y + 4,
                    stroke=col,
                    stroke_width=3,
                )
            )

            # Сторона BC (2 засічки)
            mid_bc_x, mid_bc_y = (cx + bx) / 2, cy
            d.append(
                draw.Line(
                    mid_bc_x - 3,
                    mid_bc_y - 6,
                    mid_bc_x - 3,
                    mid_bc_y + 6,
                    stroke=col,
                    stroke_width=2.5,
                )
            )
            d.append(
                draw.Line(
                    mid_bc_x + 3,
                    mid_bc_y - 6,
                    mid_bc_x + 3,
                    mid_bc_y + 6,
                    stroke=col,
                    stroke_width=2.5,
                )
            )

            # Кут C (дуга)
            d.append(
                draw.Arc(cx, cy, 26, -angle_c, 0, stroke="#dc2626", stroke_width=2.5, fill="none")
            )

        elif criterion in ["ASA", "АСА"]:
            # Сторона AC (1 засічка)
            mid_ac_x, mid_ac_y = (cx + ax) / 2, (cy + ay) / 2
            d.append(
                draw.Line(
                    mid_ac_x - 4,
                    mid_ac_y - 4,
                    mid_ac_x + 4,
                    mid_ac_y + 4,
                    stroke=col,
                    stroke_width=3,
                )
            )

            # Кут C (1 дуга)
            d.append(
                draw.Arc(cx, cy, 26, -angle_c, 0, stroke="#dc2626", stroke_width=2.5, fill="none")
            )

            # Кут A (2 дуги)
            d.append(
                draw.Circle(
                    ax, ay, 18, stroke="#16a34a", stroke_width=2, fill="none", clip_path=None
                )
            )

        elif criterion in ["SSS", "ССС"]:
            # Сторона AB (1 засічка)
            mid_ab_x, mid_ab_y = (ax + bx) / 2, (ay + by) / 2
            d.append(
                draw.Line(
                    mid_ab_x - 5, mid_ab_y, mid_ab_x + 5, mid_ab_y, stroke=col, stroke_width=3
                )
            )

            # Сторона BC (2 засічки)
            mid_bc_x, mid_bc_y = (cx + bx) / 2, cy
            d.append(
                draw.Line(
                    mid_bc_x - 3,
                    mid_bc_y - 6,
                    mid_bc_x - 3,
                    mid_bc_y + 6,
                    stroke=col,
                    stroke_width=2.5,
                )
            )
            d.append(
                draw.Line(
                    mid_bc_x + 3,
                    mid_bc_y - 6,
                    mid_bc_x + 3,
                    mid_bc_y + 6,
                    stroke=col,
                    stroke_width=2.5,
                )
            )

            # Сторона AC (3 засічки)
            mid_ac_x, mid_ac_y = (cx + ax) / 2, (cy + ay) / 2
            d.append(
                draw.Line(
                    mid_ac_x - 6,
                    mid_ac_y - 4,
                    mid_ac_x - 2,
                    mid_ac_y + 4,
                    stroke=col,
                    stroke_width=2,
                )
            )
            d.append(
                draw.Line(
                    mid_ac_x - 2,
                    mid_ac_y - 4,
                    mid_ac_x + 2,
                    mid_ac_y + 4,
                    stroke=col,
                    stroke_width=2,
                )
            )
            d.append(
                draw.Line(
                    mid_ac_x + 2,
                    mid_ac_y - 4,
                    mid_ac_x + 6,
                    mid_ac_y + 4,
                    stroke=col,
                    stroke_width=2,
                )
            )

    # Заголовок та підпис
    crit_titles = {
        "SAS": "Перша ознака (САК): AC = A₁C₁, BC = B₁C₁, ∠C = ∠C₁",
        "САК": "Перша ознака (САК): AC = A₁C₁, BC = B₁C₁, ∠C = ∠C₁",
        "ASA": "Друга ознака (АСА): AC = A₁C₁, ∠C = ∠C₁, ∠A = ∠A₁",
        "АСА": "Друга ознака (АСА): AC = A₁C₁, ∠C = ∠C₁, ∠A = ∠A₁",
        "SSS": "Третя ознака (ССС): AB = A₁B₁, BC = B₁C₁, AC = A₁C₁",
        "ССС": "Третя ознака (ССС): AB = A₁B₁, BC = B₁C₁, AC = A₁C₁",
    }
    banner = crit_titles.get(criterion, f"Ознака рівності: {criterion}")
    d.append(draw.Text(banner, 13, 20, 24, fill="#0f172a", font_weight="bold"))
    d.append(draw.Text("△ABC", 13, 85, height - 15, fill="#0284c7", font_weight="bold"))
    d.append(draw.Text("△A₁B₁C₁", 13, 345, height - 15, fill="#ea580c", font_weight="bold"))

    return d


def draw_line_segment_ray(width: int = 640, height: int = 200) -> draw.Drawing:
    """Генерує векторні креслення прямої, відрізка та променя (Рис. 1, 2, 3 за Кисельовим)."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=12))

    # Рис. 1: Пряма лінія a (проходить через A і B, нескінченна в обидва боки)
    y1 = 45
    d.append(draw.Line(30, y1, 590, y1, stroke="#475569", stroke_width=2.5))
    d.append(draw.Circle(140, y1, 4.5, fill="#0f172a"))
    d.append(draw.Text("A", 14, 135, y1 - 12, fill="#0f172a", font_weight="bold"))
    d.append(draw.Circle(380, y1, 4.5, fill="#0f172a"))
    d.append(draw.Text("B", 14, 375, y1 - 12, fill="#0f172a", font_weight="bold"))
    d.append(
        draw.Text("a", 15, 600, y1 + 5, fill="#2563eb", font_style="italic", font_weight="bold")
    )
    d.append(
        draw.Text(
            "Рис. 1. Пряма лінія AB (або a)", 12, 30, y1 + 22, fill="#64748b", font_weight="600"
        )
    )

    # Рис. 2: Відрізок CD (обмежений двома кінцями C і D)
    y2 = 105
    d.append(draw.Line(120, y2, 440, y2, stroke="#2563eb", stroke_width=3.5))
    d.append(draw.Circle(120, y2, 5.5, fill="#2563eb"))
    d.append(draw.Text("C", 14, 115, y2 - 12, fill="#2563eb", font_weight="bold"))
    d.append(draw.Circle(440, y2, 5.5, fill="#2563eb"))
    d.append(draw.Text("D", 14, 435, y2 - 12, fill="#2563eb", font_weight="bold"))
    d.append(
        draw.Text(
            "Рис. 2. Відрізок CD (кінці C і D)", 12, 30, y2 + 22, fill="#64748b", font_weight="600"
        )
    )

    # Рис. 3: Промінь EF (початок E, проходить через F і продовжується нескінченно)
    y3 = 165
    d.append(draw.Line(120, y3, 590, y3, stroke="#16a34a", stroke_width=2.5))
    d.append(draw.Circle(120, y3, 5.5, fill="#16a34a"))
    d.append(draw.Text("E (початок)", 13, 85, y3 - 12, fill="#16a34a", font_weight="bold"))
    d.append(draw.Circle(320, y3, 4.5, fill="#0f172a"))
    d.append(draw.Text("F", 14, 315, y3 - 12, fill="#0f172a", font_weight="bold"))
    d.append(
        draw.Text(
            "Рис. 3. Промінь EF (початкова точка E)",
            12,
            30,
            y3 + 22,
            fill="#64748b",
            font_weight="600",
        )
    )

    return d


def draw_segment_addition(
    ab: float = 90,
    cd: float = 120,
    ef: float = 80,
    width: int = 640,
    height: int = 170,
) -> draw.Drawing:
    """Генерує додавання відрізків MQ = AB + CD + EF на прямій (Рис. 4 і 5 за Кисельовим)."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=12))

    y = 75
    start_x = 70
    x_m = start_x
    x_n = x_m + ab
    x_p = x_n + cd
    x_q = x_p + ef

    # Фонова пряма лінія
    d.append(draw.Line(30, y, width - 30, y, stroke="#cbd5e1", stroke_width=2))

    # Складові відрізки кольоровими лініями
    d.append(draw.Line(x_m, y, x_n, y, stroke="#2563eb", stroke_width=4))
    d.append(draw.Line(x_n, y, x_p, y, stroke="#16a34a", stroke_width=4))
    d.append(draw.Line(x_p, y, x_q, y, stroke="#d97706", stroke_width=4))

    # Точки поділу M, N, P, Q
    points = [(x_m, "M"), (x_n, "N"), (x_p, "P"), (x_q, "Q")]
    for px, label in points:
        d.append(draw.Circle(px, y, 5, fill="#0f172a"))
        d.append(draw.Text(label, 14, px - 6, y + 24, fill="#0f172a", font_weight="bold"))

    # Підписи над частинами
    d.append(
        draw.Text("MN = AB", 13, (x_m + x_n) / 2 - 28, y - 14, fill="#2563eb", font_weight="bold")
    )
    d.append(
        draw.Text("NP = CD", 13, (x_n + x_p) / 2 - 28, y - 14, fill="#16a34a", font_weight="bold")
    )
    d.append(
        draw.Text("PQ = EF", 13, (x_p + x_q) / 2 - 28, y - 14, fill="#d97706", font_weight="bold")
    )

    # Нижній загальний підпис
    total_len = ab + cd + ef
    d.append(
        draw.Text(
            f"Рис. 5. Сума відрізків: MQ = MN + NP + PQ = AB + CD + EF ({total_len:.0f} од.)",
            13,
            40,
            height - 20,
            fill="#0f172a",
            font_weight="bold",
        )
    )

    return d


def draw_circle_elements(width: int = 560, height: int = 320) -> draw.Drawing:
    """Генерує коло, круг, радіус, хорду, діаметр, дугу та січну (Рис. 6 і 7 за Кисельовим)."""
    d = draw.Drawing(width, height)
    d.append(draw.Rectangle(0, 0, width, height, fill="#f8fafc", rx=12))

    ox, oy = 175, 160
    r = 110

    # Заливка круга
    d.append(draw.Circle(ox, oy, r, fill="#ffffff", stroke="#0284c7", stroke_width=2.5))

    # Сектор AOB (кути -40° до 20°)
    rad1, rad2 = math.radians(-40), math.radians(20)
    p_a_x, p_a_y = ox + r * math.cos(rad1), oy + r * math.sin(rad1)
    p_b_x, p_b_y = ox + r * math.cos(rad2), oy + r * math.sin(rad2)

    # Заливка сектора AOB
    sector_path = draw.Path(fill="#e0f2fe", stroke="none")
    sector_path.M(ox, oy).L(p_a_x, p_a_y).A(r, r, 0, 0, 1, p_b_x, p_b_y).Z()
    d.append(sector_path)

    # Радіус OA
    d.append(draw.Line(ox, oy, p_a_x, p_a_y, stroke="#2563eb", stroke_width=2.5))
    d.append(draw.Circle(p_a_x, p_a_y, 4, fill="#2563eb"))
    d.append(draw.Text("A", 13, p_a_x + 8, p_a_y - 2, fill="#2563eb", font_weight="bold"))

    # Радіус OB
    d.append(draw.Line(ox, oy, p_b_x, p_b_y, stroke="#2563eb", stroke_width=2.5))
    d.append(draw.Circle(p_b_x, p_b_y, 4, fill="#2563eb"))
    d.append(draw.Text("B", 13, p_b_x + 8, p_b_y + 10, fill="#2563eb", font_weight="bold"))

    # Діаметр CD (через центр горизонтально)
    c_x, c_y = ox - r, oy
    d_x, d_y = ox + r, oy
    d.append(
        draw.Line(c_x, c_y, d_x, d_y, stroke="#dc2626", stroke_width=2, stroke_dasharray="5,3")
    )
    d.append(draw.Circle(c_x, c_y, 4, fill="#dc2626"))
    d.append(draw.Text("C", 13, c_x - 18, c_y + 5, fill="#dc2626", font_weight="bold"))
    d.append(draw.Circle(d_x, d_y, 4, fill="#dc2626"))
    d.append(draw.Text("D", 13, d_x + 8, d_y + 5, fill="#dc2626", font_weight="bold"))

    # Хорда EF (у верхній лівій чверті)
    rad_e, rad_f = math.radians(-150), math.radians(-85)
    e_x, e_y = ox + r * math.cos(rad_e), oy + r * math.sin(rad_e)
    f_x, f_y = ox + r * math.cos(rad_f), oy + r * math.sin(rad_f)
    d.append(draw.Line(e_x, e_y, f_x, f_y, stroke="#16a34a", stroke_width=3))
    d.append(draw.Circle(e_x, e_y, 4, fill="#16a34a"))
    d.append(draw.Text("E", 13, e_x - 16, e_y - 4, fill="#16a34a", font_weight="bold"))
    d.append(draw.Circle(f_x, f_y, 4, fill="#16a34a"))
    d.append(draw.Text("F", 13, f_x + 2, f_y - 10, fill="#16a34a", font_weight="bold"))

    # Січна лінія s
    d.append(draw.Line(50, 275, 300, 295, stroke="#94a3b8", stroke_width=2))
    d.append(draw.Text("s (січна)", 12, 305, 300, fill="#64748b", font_style="italic"))

    # Центр O
    d.append(draw.Circle(ox, oy, 5, fill="#0f172a"))
    d.append(draw.Text("O (центр)", 13, ox - 35, oy - 10, fill="#0f172a", font_weight="bold"))

    # Панель-легенда праворуч
    lx = 330
    d.append(
        draw.Text("Рис. 6. Елементи кола та круга:", 14, lx, 45, fill="#0f172a", font_weight="bold")
    )
    legend_items = [
        ("● O — центр кола", "#0f172a"),
        ("— OA, OB — радіуси (r)", "#2563eb"),
        ("--- CD — діаметр (d = 2r)", "#dc2626"),
        ("— EF — хорда", "#16a34a"),
        ("— s — січна лінія", "#64748b"),
        ("■ Сектор AOB (частина круга)", "#0284c7"),
    ]
    for i, (txt, col) in enumerate(legend_items):
        d.append(draw.Text(txt, 13, lx, 78 + i * 26, fill=col, font_weight="600"))

    d.append(
        draw.Text(
            "Рис. 7: Коло — лінія; круг — площина.",
            12,
            lx,
            255,
            fill="#475569",
            font_style="italic",
        )
    )

    return d


@lru_cache(maxsize=512)
def get_book_figure(fig_num: int, book_id: str = "kiselev_geometry_1931") -> BookFigure | None:
    """Отримує об'єкт BookFigure з бази даних за номером рисунка.

    Результат кешується в пам'яті (Zero Recomputation). Після зміни book_kb.db
    у тому самому процесі викличте ``get_book_figure.cache_clear()``.
    """
    db = BookDatabase()
    return db.get_figure_by_num(book_id, fig_num)


def get_book_figure_svg(fig_num: int, book_id: str = "kiselev_geometry_1931") -> str | None:
    """Отримує готовий векторний SVG рисунка з бази даних за його номером (Рис. N)."""
    fig = get_book_figure(fig_num, book_id)
    return fig.svg_content if fig else None


def render_figure_card(
    fig_num: int, book_id: str = "kiselev_geometry_1931", show_caption: bool = True
) -> str:
    """Повертає оформлений HTML-блок картки з SVG-рисунком, назвою та методичним підписом."""
    fig = get_book_figure(fig_num, book_id)
    if not fig:
        return f'<div class="figure-missing">Рис. {fig_num} не знайдено в базі даних.</div>'

    caption_text = fig.caption_original or fig.didactic_notes
    caption_html = (
        f'<div class="figure-caption" style="font-size: 13px; color: #64748b; margin-top: 8px; font-style: italic;">{caption_text}</div>'
        if show_caption and caption_text
        else ""
    )

    svg_inline = fig.svg_content.strip()
    if svg_inline.startswith("<?xml"):
        start_idx = svg_inline.find("<svg")
        if start_idx != -1:
            svg_inline = svg_inline[start_idx:]

    return f"""<div class="figure-card" style="text-align: center; margin: 16px 0; padding: 14px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);"><div style="font-weight: 600; font-size: 14px; color: #1e293b; margin-bottom: 8px;">{fig.title}</div><div style="display: flex; justify-content: center; overflow-x: auto;">{svg_inline}</div>{caption_html}</div>"""
