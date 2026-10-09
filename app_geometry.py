import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium", app_title="Геометрія 7 клас · Кисельов")


@app.cell
def _():
    import html
    import sys
    from pathlib import Path

    import marimo as mo

    # Додаємо src до sys.path для імпорту модулів
    _src_path = str(Path(__file__).parent / "src")
    if _src_path not in sys.path:
        sys.path.insert(0, _src_path)

    from geometry_engine.jsx_templates import (
        get_scissors_widget_html,
        get_triangle_congruence_html,
    )
    from geometry_engine.lesson import load_all_lessons
    from geometry_engine.svg_drawings import (
        draw_adjacent_angles,
        draw_angle,
        draw_angle_bisector,
        draw_congruence_showcase,
        draw_segment_addition,
        draw_vertical_angles,
        render_figure_card,
    )
    from geometry_engine.tasks import TASKS

    return (
        TASKS,
        draw_adjacent_angles,
        draw_angle,
        draw_angle_bisector,
        draw_congruence_showcase,
        draw_segment_addition,
        draw_vertical_angles,
        get_scissors_widget_html,
        get_triangle_congruence_html,
        html,
        load_all_lessons,
        mo,
        render_figure_card,
    )


@app.cell
def _(mo):
    # Книжкова типографіка для учня 7 класу: 780px, 19px, line-height 1.75
    mo.Html(
        """
        <style>
        .book-container { max-width: 780px; margin: 0 auto; color: #1e293b; }
        .book-header { text-align: center; padding: 24px 0 20px; border-bottom: 2px solid #e2e8f0; margin-bottom: 16px; }
        .book-title { font-size: 32px; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; margin-bottom: 6px; }
        .book-subtitle { font-size: 17px; color: #64748b; font-weight: 500; }
        .chapter-heading { font-size: 28px; font-weight: 800; color: #0f172a; margin: 28px 0 8px; line-height: 1.3; }

        .book-text, .book-text .paragraph, .book-text li { font-size: 19px; line-height: 1.75; }
        .book-text .paragraph { display: block; margin: 0 0 1em; }
        .book-text h2 { font-size: 24px; font-weight: 800; color: #0f172a; margin: 36px 0 12px;
                        padding-bottom: 6px; border-bottom: 2px solid #e2e8f0; }
        .book-text h3 { font-size: 21px; font-weight: 700; color: #1e293b; margin: 28px 0 10px; }
        .book-text hr { display: none; }
        .book-text blockquote { background: #f0fdf4; border-left: 5px solid #16a34a; border-radius: 8px;
                                padding: 12px 20px; margin: 20px 0; color: #14532d; font-style: normal; }
        .book-text blockquote .paragraph::before,
        .book-text blockquote .paragraph::after { content: none; }

        .feynman-box, .misconception-box { border-radius: 8px; padding: 14px 20px; margin: 20px 0; }
        .feynman-box { background: #f0f9ff; border-left: 5px solid #0284c7; color: #0c4a6e; }
        .misconception-box { background: #fffbeb; border-left: 5px solid #d97706; color: #78350f; }
        .feynman-box .paragraph, .misconception-box .paragraph,
        .feynman-box li, .misconception-box li { font-size: 18px; }
        .feynman-box .paragraph:last-child, .misconception-box .paragraph:last-child { margin-bottom: 0; }

        .widget-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
                       box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05); padding: 18px; margin: 20px 0; }
        .widget-title { font-weight: 700; font-size: 15px; margin-bottom: 10px; color: #0f172a; }
        .predict-card { background: #f5f3ff; border-left: 5px solid #7c3aed; border-radius: 8px;
                        padding: 16px 20px; margin: 20px 0; }
        .locked-observation { background: #f8fafc; border: 1px dashed #94a3b8; border-radius: 10px;
                              padding: 18px; margin: 18px 0; text-align: center; color: #475569; }
        .hint-panel details { border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; margin: 8px 0; }
        .hint-panel summary { cursor: pointer; font-weight: 700; color: #334155; }
        .figure-missing { color: #b91c1c; font-style: italic; text-align: center; margin: 12px 0; }
        </style>
        """
    )
    return


@app.cell
def _(load_all_lessons, mo):
    # Уроки з content/geometry/*.md — єдине джерело тексту
    lessons = {les.lesson_id: les for les in load_all_lessons()}
    _options = {f"📖 {les.title}": les.lesson_id for les in lessons.values()}

    lesson_selector = mo.ui.dropdown(
        options=_options,
        value=next(iter(_options)),
        label="Зміст підручника:",
    )

    mo.vstack(
        [
            mo.Html(
                """
                <div class="book-container"><div class="book-header">
                  <div class="book-title">📐 Геометрія (7 клас)</div>
                  <div class="book-subtitle">А. П. Кисельов · Класичний курс у сучасній адаптації за програмою НУШ</div>
                </div></div>
                """
            ),
            lesson_selector,
        ]
    )
    return lesson_selector, lessons


@app.cell
def _(mo):
    # Елементи керування живих креслень (один і той самий повзунок може
    # з'являтися в кількох картках — marimo синхронізує їх)
    ab_slider = mo.ui.slider(start=40, stop=140, step=10, value=80, label="AB:")
    cd_slider = mo.ui.slider(start=40, stop=140, step=10, value=110, label="CD:")
    ef_slider = mo.ui.slider(start=40, stop=140, step=10, value=70, label="EF:")
    angle_slider = mo.ui.slider(start=15, stop=165, step=5, value=60, label="Кут α (°):")
    criterion_selector = mo.ui.radio(
        options={
            "1. Перша ознака (САК — дві сторони і кут між ними)": "SAS",
            "2. Друга ознака (АСА — сторона і прилеглі кути)": "ASA",
            "3. Третя ознака (ССС — три сторони)": "SSS",
        },
        value="1. Перша ознака (САК — дві сторони і кут між ними)",
        label="Оберіть ознаку рівності:",
    )
    return ab_slider, angle_slider, cd_slider, criterion_selector, ef_slider


@app.cell
def _(
    ab_slider,
    angle_slider,
    cd_slider,
    criterion_selector,
    draw_adjacent_angles,
    draw_angle,
    draw_angle_bisector,
    draw_congruence_showcase,
    draw_segment_addition,
    draw_vertical_angles,
    ef_slider,
    get_scissors_widget_html,
    get_triangle_congruence_html,
    mo,
):
    # Живі віджети, на які посилаються уроки через <!-- widget: name -->
    def _card(title, *parts):
        _inner = mo.vstack(list(parts), align="center")
        return mo.Html(
            f'<div class="book-container"><div class="widget-card">'
            f'<div class="widget-title">{title}</div>{_inner}</div></div>'
        )

    def _svg(drawing):
        return mo.Html(drawing.as_svg())

    _a = angle_slider.value
    widgets = {
        "segment_addition": _card(
            "🕹️ Живе креслення (рис. 5): змінюй довжини відрізків повзунками",
            mo.hstack([ab_slider, cd_slider, ef_slider], justify="center", wrap=True),
            _svg(draw_segment_addition(ab_slider.value, cd_slider.value, ef_slider.value)),
        ),
        "angle_rotation": _card(
            "🕹️ Поверни промінь OA повзунком: довжина сторін не впливає на величину кута",
            angle_slider,
            _svg(draw_angle(_a)),
        ),
        "angle_bisector": _card(
            "🕹️ Бісектриса завжди ділить кут на дві рівні половини",
            angle_slider,
            _svg(draw_angle_bisector(_a)),
        ),
        "adjacent_angles": _card(
            "🕹️ Суміжні кути: змінюй α і стеж за сумою α + β",
            angle_slider,
            _svg(draw_adjacent_angles(_a)),
        ),
        "vertical_scissors": _card(
            "🕹️ Модель ножиць: потягни синю точку A пальцем або мишкою",
            mo.Html(get_scissors_widget_html()),
            angle_slider,
            _svg(draw_vertical_angles(_a)),
        ),
        "congruence_criteria": _card(
            "📐 Дослідження ознак рівності на кресленні",
            criterion_selector,
            _svg(draw_congruence_showcase(criterion_selector.value)),
        ),
        "triangle_superposition": _card(
            "🕹️ Спосіб накладання: перетягни помаранчевий трикутник за точку A₁ на синій",
            mo.Html(get_triangle_congruence_html()),
        ),
    }
    return (widgets,)


@app.cell
def _(lesson_selector, lessons, mo, render_figure_card):
    # Статичні частини уроку (текст, блоки, рисунки з book_kb.db) рахуються
    # лише при зміні розділу, а не при кожному русі повзунка
    lesson = lessons[lesson_selector.value]

    def _wrap(inner, extra=""):
        return mo.Html(f'<div class="book-container {extra}">{inner}</div>')

    static_blocks = {}
    for _i, _seg in enumerate(lesson.segments):
        if _seg.kind == "markdown":
            static_blocks[_i] = _wrap(mo.md(_seg.text).text, "book-text")
        elif _seg.kind == "box":
            static_blocks[_i] = _wrap(
                f'<div class="{_seg.css_class}">{mo.md(_seg.box_markdown()).text}</div>',
                "book-text",
            )
        elif _seg.kind == "figure":
            static_blocks[_i] = _wrap(render_figure_card(_seg.fig_num))
    return lesson, static_blocks


@app.cell
def _(TASKS, lesson, mo):
    task = TASKS[lesson.lesson_id]
    prediction = mo.ui.radio(
        options=task.prediction_options,
        value=None,
        label=task.prediction_prompt,
    )
    mo.Html(
        '<div class="book-container"><div class="predict-card">'
        '<div class="widget-title">🔮 Прогноз: спочатку обери гіпотезу</div>'
        f"{prediction}</div></div>"
    )
    return prediction, task


@app.cell
def _(mo, prediction, task):
    observation_unlocked = prediction.value is not None
    if not observation_unlocked:
        _prediction_feedback = mo.md("*Після вибору відкриються живі досліди цього уроку.*")
    else:
        _correct = prediction.value == task.prediction_answer
        _prefix = "Влучний прогноз." if _correct else "Добре, що ти зафіксував свою думку."
        _prediction_feedback = mo.callout(
            mo.md(f"**{_prefix}** {task.prediction_explanation}"),
            kind="success" if _correct else "info",
        )
    _prediction_feedback
    return (observation_unlocked,)


@app.cell
def _(html, lesson, mo, observation_unlocked, static_blocks, widgets):
    _items = [
        mo.Html(
            f'<div class="book-container"><div class="chapter-heading">'
            f"{html.escape(lesson.title)}</div></div>"
        )
    ]
    for _i, _seg in enumerate(lesson.segments):
        if _seg.kind != "widget":
            _items.append(static_blocks[_i])
        elif observation_unlocked:
            _items.append(widgets[_seg.widget])
        else:
            _items.append(
                mo.Html(
                    '<div class="book-container"><div class="locked-observation">'
                    "🔒 Спочатку обери прогноз угорі — тоді відкриється дослід."
                    "</div></div>"
                )
            )
    mo.vstack(_items, gap=0)
    return


@app.cell
def _(mo, task):
    # «Перевір себе»: задача до поточного уроку
    task_input = mo.ui.text(
        placeholder=task.placeholder,
        label="Твоя відповідь:",
        full_width=True,
    )
    _hint_blocks = "".join(
        f"<details><summary>Підказка {index}</summary>{mo.md(hint).text}</details>"
        for index, hint in enumerate(task.hints, start=1)
    )
    _out = mo.vstack(
        [
            mo.Html(
                '<div class="book-container"><div class="chapter-heading">🎯 Місія: перевір себе</div></div>'
            ),
            mo.Html(f'<div class="book-container book-text">{mo.md(task.text_uk).text}</div>'),
            task_input,
            mo.Html(f'<div class="book-container book-text hint-panel">{_hint_blocks}</div>'),
        ]
    )
    _out
    return (task_input,)


@app.cell
def _(mo, task, task_input):
    if not task_input.value.strip():
        _result = mo.md(
            "*Введи відповідь числом або виразом — SymPy миттєво перевірить її точно, без округлень.*"
        )
    else:
        _res = task.check(task_input.value)
        _result = mo.callout(
            mo.md(_res["message"]), kind="success" if _res["correct"] else "danger"
        )
    _result
    return


if __name__ == "__main__":
    app.run()
