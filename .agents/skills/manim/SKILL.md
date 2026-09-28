---
name: manim
description: Comprehensive implementation engine and best practices for Manim Community Edition (CE v0.18+). Use whenever creating, coding, refactoring, debugging, or rendering mathematical and scientific animations in Python with Manim. Covers Mobjects, MathTex, coordinate systems, ValueTracker, updaters, camera motion, pedagogical visual design, and CLI rendering workflows.
---

# 🎬 Manim Community Edition (CE) Animation Engine

Цей скіл є технічним виконавчим рушієм для створення анімацій у **Manim Community Edition** (v0.18+). Якщо скіл `feynman-manim-composer` створює педагогічний сценарій і розкадровку (`scenes.md`), то цей скіл перетворює ідеї на чистий, оптимізований, стабільний Python-код та рендерить відео.

---

## ⚡ Швидкий старт та CLI-команди (через `uv`)

Усі команди запускаються через ізольоване оточення проекту за допомогою `uv run`:

```bash
# Швидкий прев'ю-рендер низької якості (480p, 15fps) з автоматичним відкриттям відеоплеєра:
uv run manim -pql scene.py MyScene

# Середня якість для тестування анімацій (720p, 30fps):
uv run manim -pqm scene.py MyScene

# Фінальна висока якість (1080p, 60fps):
uv run manim -pqh scene.py MyScene

# 4K якість (2160p, 60fps):
uv run manim -pqk scene.py MyScene

# Рендер окремого кадру як PNG зображення:
uv run manim -s -pqm scene.py MyScene

# Рендер з прозорим фоном (для вставки в оверлеї чи веб):
uv run manim -pqm -t scene.py MyScene

# Експорт у форматі GIF:
uv run manim -pqm --format=gif scene.py MyScene
```

---

## 🎨 Дизайн-код та візуальні стандарти для 7 класу (12-13 років)

1. **Колірна палітра високого контрасту (3Blue1Brown Dark Theme):**
   - Фон: Темний графітовий `config.background_color = "#14161B"` (м'якший за чисто чорний, не втомлює очі дитини).
   - Акцентні кольори для фізичних величин:
     - Відстань / Положення ($x, s$): `BLUE_C` (`#58C4DD`)
     - Швидкість ($v$): `YELLOW_C` (`#F4D03F`)
     - Прискорення / Сила ($a, F$): `RED_C` (`#E74C3C`)
     - Маса / Речовина ($m, \rho$): `TEAL_C` (`#1ABC9C`)
     - Енергія / Робота ($E, A$): `ORANGE` (`#E67E22`)
     - Час ($t$): `PURPLE_B` (`#9B59B6`)

2. **Читабельність та розмір шрифтів:**
   - Для моніторів та планшетів стандартний кегль формул має бути збільшений: `font_size=42` або більше для головних формул, `font_size=32` для підписів.
   - Уникайте перевантаження сцени: одночасно на екрані має бути **не більше однієї активної думки** та максимум 2-3 допоміжні підписи.

3. **Темпоритм (Pacing):**
   - Учням 7 класу потрібен час роздивитися зміни: паузи `self.wait(1)` або `self.wait(1.5)` після кожного кроку трансформації обов'язкові.
   - Швидкість анімацій: `run_time=1.5` для появи фігур, `run_time=2.0` для складних морфінгів формул.

---

## 📐 Ключові паттерни коду Manim CE

### 1. Робота з формулами (`MathTex` та `TransformMatchingTex`)

Завжди використовуйте сирі рядки `r"..."` для LaTeX. Розбивайте формулу на підрядки (`substrings`), щоб фарбувати змінні окремо або робити плавний морфінг:

```python
from manim import *

class KineticEnergyFormula(Scene):
    def construct(self):
        # Розбивка на ізольовані токени для селективного фарбування
        formula1 = MathTex(
            r"E_k", r"=", r"\frac{m \cdot v^2}{2}",
            font_size=48
        )
        formula1.set_color_by_tex(r"E_k", ORANGE)
        formula1.set_color_by_tex(r"m", TEAL_C)
        formula1.set_color_by_tex(r"v", YELLOW_C)
        
        self.play(Write(formula1), run_time=1.5)
        self.wait(1)
        
        # Заміна значення v на конкретну швидкість зі збереженням зв'язків
        formula2 = MathTex(
            r"E_k", r"=", r"\frac{2 \cdot (10)^2}{2}",
            font_size=48
        )
        formula2.set_color_by_tex(r"E_k", ORANGE)
        
        self.play(TransformMatchingTex(formula1, formula2), run_time=2)
        self.wait(1.5)
```

### 2. Динамічні графіки та інтерактивні величини (`ValueTracker` + `always_redraw`)

Найкращий спосіб показати закон фізики чи графік функції — зв'язати геометрію зі змінним параметром (`ValueTracker`):

```python
class UniformMotionGraph(Scene):
    """Ілюстрація залежності шляху від часу: s = v * t (7 клас Фізика)"""
    def construct(self):
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 50, 10],
            x_length=7,
            y_length=4.5,
            axis_config={"include_numbers": True, "color": GREY_A},
            tips=True
        ).to_edge(LEFT, buff=0.8)
        
        labels = axes.get_axis_labels(
            x_label=MathTex("t, \\text{ c}", font_size=32),
            y_label=MathTex("s, \\text{ м}", font_size=32)
        )
        
        v = 5  # швидкість 5 м/с
        graph = axes.plot(lambda t: v * t, x_range=[0, 8], color=YELLOW_C)
        graph_label = axes.get_graph_label(graph, label=r"s(t) = 5t", x_val=7, direction=UP)

        # Рухома точка та проекції
        t_tracker = ValueTracker(0)
        
        dot = always_redraw(lambda: Dot(
            point=axes.c2p(t_tracker.get_value(), v * t_tracker.get_value()),
            color=RED_C,
            radius=0.1
        ))
        
        h_line = always_redraw(lambda: axes.get_horizontal_line(
            dot.get_center(), line_func=DashedLine, color=GREY_B
        ))
        v_line = always_redraw(lambda: axes.get_vertical_line(
            dot.get_center(), line_func=DashedLine, color=GREY_B
        ))

        # Цифровий показник поточного шляху
        s_value_text = always_redraw(lambda: MathTex(
            rf"s = {v * t_tracker.get_value():.1f}\text{{ м}}",
            font_size=36,
            color=YELLOW_C
        ).to_corner(UR, buff=1.0))

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), FadeIn(graph_label))
        self.add(dot, h_line, v_line, s_value_text)
        
        # Плавна зміна часу від 0 до 8 секунд
        self.play(t_tracker.animate.set_value(8), run_time=6, rate_func=linear)
        self.wait(2)
```

### 3. Геометричні моделі (Наочна алгебра: площа $(a+b)^2$)

Для учнів 7 класу формули скороченого множення мають бути показані як площа квадрата зі стороною $(a + b)$:

```python
class SquareOfSumVisual(Scene):
    """Геометричне доведення формули (a + b)^2 = a^2 + 2ab + b^2"""
    def construct(self):
        # Розміри квадратів
        a_len = 2.4
        b_len = 1.2
        
        # Квадрат a^2 (синій)
        sq_a = Square(side_length=a_len, fill_color=BLUE_D, fill_opacity=0.8, stroke_color=WHITE)
        sq_a.move_to(ORIGIN).shift(LEFT * (b_len / 2) + DOWN * (b_len / 2))
        lbl_a2 = MathTex("a^2", font_size=36).move_to(sq_a.get_center())
        
        # Квадрат b^2 (помаранчевий)
        sq_b = Square(side_length=b_len, fill_color=ORANGE, fill_opacity=0.8, stroke_color=WHITE)
        sq_b.next_to(sq_a, UR, buff=0)
        lbl_b2 = MathTex("b^2", font_size=32).move_to(sq_b.get_center())
        
        # Прямокутники ab (зелені)
        rect_ab1 = Rectangle(width=b_len, height=a_len, fill_color=GREEN_D, fill_opacity=0.8, stroke_color=WHITE)
        rect_ab1.next_to(sq_a, RIGHT, buff=0)
        lbl_ab1 = MathTex("ab", font_size=32).move_to(rect_ab1.get_center())
        
        rect_ab2 = Rectangle(width=a_len, height=b_len, fill_color=GREEN_D, fill_opacity=0.8, stroke_color=WHITE)
        rect_ab2.next_to(sq_a, UP, buff=0)
        lbl_ab2 = MathTex("ab", font_size=32).move_to(rect_ab2.get_center())

        group_geo = VGroup(sq_a, lbl_a2, sq_b, lbl_b2, rect_ab1, lbl_ab1, rect_ab2, lbl_ab2).to_edge(LEFT, buff=1.0)
        
        # Формула праворуч
        formula = MathTex(
            r"(a + b)^2", r"=", r"a^2", r"+", r"2ab", r"+", r"b^2",
            font_size=42
        ).to_edge(RIGHT, buff=1.2)
        formula.set_color_by_tex(r"a^2", BLUE_C)
        formula.set_color_by_tex(r"2ab", GREEN_C)
        formula.set_color_by_tex(r"b^2", ORANGE)

        self.play(FadeIn(sq_a), Write(lbl_a2))
        self.wait(0.5)
        self.play(FadeIn(rect_ab1), Write(lbl_ab1), FadeIn(rect_ab2), Write(lbl_ab2))
        self.wait(0.5)
        self.play(FadeIn(sq_b), Write(lbl_b2))
        self.wait(1)
        
        self.play(Write(formula), run_time=2)
        self.wait(2)
```

---

## ⚠️ Типові помилки та як їх уникати

1. **LaTeX Syntax Errors (`MathTex`):**
   - *Помилка:* Використання звичайного рядка `"\alpha"` замість сирого рядка `r"\alpha"`.
   - *Правило:* Завжди пишіть `MathTex(r"...")`. Якщо потрібен бекслеш у тексті, використовуйте подвійний бекслеш `\\text{м/с}` або сирий рядок `r"\text{м/с}"`.
2. **Витік пам'яті та зависання в `always_redraw`:**
   - Не створюйте всередині лямбди нові важкі об'єкти, які не залежать від трекера. Виносьте статичні частини назовні.
3. **Зсув центрів при `Transform`:**
   - Якщо перетворювати текст або фігуру різного розміру, Manim центрує результат. Використовуйте `.move_to(target.get_center())` або `ReplacementTransform(..., path_arc=...)`.
4. **Рендеринг на Windows:**
   - MiKTeX може запитувати встановлення відсутніх пакетів під час першого запуску. Якщо виникає помилка LaTeX, можна тимчасово використати `Text()` замість `Tex()` або перевірити наявність `latex.exe` в системі.

---

## 🎯 Чеклист готовності анімації перед здачею
- [ ] Концепція розбита на кроки: Конкретна дія $\to$ Геометричний образ $\to$ Формула.
- [ ] Кегль шрифту легко читається на екрані смартфона чи планшета.
- [ ] Фізичні змінні узгоджені за кольором між кресленням, графіком та формулою.
- [ ] Немає нагромадження тексту поверх графіків (використано `buff`, `.to_edge`, `.next_to`).
- [ ] Сцена перевірена через `uv run manim -pql scene.py MyScene`.
