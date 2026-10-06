import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    from pathlib import Path
    import sys

    # Додаємо src до sys.path для імпорту модулів
    src_path = str(Path(__file__).parent / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    from geometry_engine.svg_drawings import (
        draw_adjacent_angles,
        draw_angle,
        draw_angle_bisector,
        draw_circle_elements,
        draw_congruence_showcase,
        draw_line_segment_ray,
        draw_segment_addition,
        draw_triangle,
        draw_vertical_angles,
    )
    from geometry_engine.sympy_solver import (
        verify_adjacent_angle,
        verify_congruence_criterion,
        verify_congruence_mission,
        verify_segment_addition,
        verify_vertical_angles,
    )
    from geometry_engine.jsx_templates import (
        get_scissors_widget_html,
        get_triangle_congruence_html,
    )

    return (
        Path,
        draw_adjacent_angles,
        draw_angle,
        draw_angle_bisector,
        draw_circle_elements,
        draw_congruence_showcase,
        draw_line_segment_ray,
        draw_segment_addition,
        draw_triangle,
        draw_vertical_angles,
        get_scissors_widget_html,
        get_triangle_congruence_html,
        mo,
        sys,
        verify_adjacent_angle,
        verify_congruence_criterion,
        verify_congruence_mission,
        verify_segment_addition,
        verify_vertical_angles,
    )


@app.cell
def __(mo):
    # Книжкова типографіка та оформлення для учня 7 класу
    styles = mo.Html(
        """
        <style>
        /* Оптимальна зона читання для дитини (65-75 символів у рядку, max-width 780px) */
        .book-container {
            max-width: 780px;
            margin: 0 auto;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #1e293b;
        }
        .book-header {
            text-align: center;
            padding: 24px 0 20px 0;
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 24px;
        }
        .book-title {
            font-size: 32px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }
        .book-subtitle {
            font-size: 17px;
            color: #64748b;
            font-weight: 500;
        }
        .chapter-heading {
            font-size: 26px;
            font-weight: 800;
            color: #0f172a;
            margin: 32px 0 16px 0;
            line-height: 1.3;
        }
        .section-heading {
            font-size: 21px;
            font-weight: 700;
            color: #1e293b;
            margin: 28px 0 12px 0;
            line-height: 1.35;
        }
        .book-p {
            font-size: 19px;
            line-height: 1.75;
            color: #1e293b;
            margin-bottom: 1.25em;
            text-align: justify;
            text-justify: inter-word;
        }
        .theorem-box {
            background-color: #f0fdf4;
            border-left: 5px solid #16a34a;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 22px 0;
            font-size: 19px;
            line-height: 1.7;
            color: #14532d;
        }
        .feynman-box {
            background-color: #f0f9ff;
            border-left: 5px solid #0284c7;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 22px 0;
            font-size: 18px;
            line-height: 1.7;
            color: #0c4a6e;
        }
        .misconception-box {
            background-color: #fffbeb;
            border-left: 5px solid #d97706;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 22px 0;
            font-size: 18px;
            line-height: 1.7;
            color: #78350f;
        }
        .widget-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
            border-radius: 12px;
            padding: 18px;
            margin: 22px 0;
        }
        .widget-title {
            font-weight: bold;
            font-size: 15px;
            margin-bottom: 10px;
            color: #0f172a;
        }
        .figure-caption {
            font-size: 14px;
            color: #64748b;
            text-align: center;
            margin-top: 8px;
            font-style: italic;
        }
        .katex {
            font-size: 1.12em !important;
        }
        </style>
        """
    )
    styles
    return (styles,)


@app.cell
def __(mo):
    # Шапка підручника та вибір розділу
    header = mo.Html(
        """
        <div class="book-container">
            <div class="book-header">
                <div class="book-title">📐 Геометрія (7 клас)</div>
                <div class="book-subtitle">А. П. Кисельов · Класичний курс у сучасній адаптації за програмою НУШ</div>
            </div>
        </div>
        """
    )

    chapter_options = {
        "📖 Вступ. Найпростіші фігури: Пряма, відрізок, промінь, коло (§§ 1–12)": "intro",
        "📖 Розділ 1. Кути та їх вимірювання. Суміжні та вертикальні кути (§§ 13–26)": "angles",
        "📖 Розділ 2. Трикутники та три ознаки їхньої рівності (§§ 27–45)": "triangles",
    }

    chapter_selector = mo.ui.dropdown(
        options=chapter_options,
        value="📖 Вступ. Найпростіші фігури: Пряма, відрізок, промінь, коло (§§ 1–12)",
        label="Зміст підручника:",
    )

    mo.vstack([header, chapter_selector])
    return chapter_options, chapter_selector, header


@app.cell
def __(chapter_selector, mo):
    # Інтерактивні елементи керування для поточного розділу
    _ch = chapter_selector.value

    if _ch == "intro":
        ab_slider = mo.ui.slider(
            start=40, stop=140, step=10, value=80, label="Довжина відрізка AB (од.):"
        )
        cd_slider = mo.ui.slider(
            start=40, stop=140, step=10, value=110, label="Довжина відрізка CD (од.):"
        )
        ef_slider = mo.ui.slider(
            start=40, stop=140, step=10, value=70, label="Довжина відрізка EF (од.):"
        )
        angle_slider = None
        criterion_selector = None
    elif _ch == "angles":
        ab_slider = None
        cd_slider = None
        ef_slider = None
        angle_slider = mo.ui.slider(
            start=15, stop=165, step=5, value=60, label="Кут розхилу променя α (°):"
        )
        criterion_selector = None
    else:
        ab_slider = None
        cd_slider = None
        ef_slider = None
        angle_slider = None
        criterion_selector = mo.ui.radio(
            options={
                "1. Перша ознака (САК — за двома сторонами і кутом між ними)": "SAS",
                "2. Друга ознака (АСА — за стороною і прилеглими кутами)": "ASA",
                "3. Третя ознака (ССС — за трьома сторонами)": "SSS",
            },
            value="1. Перша ознака (САК — за двома сторонами і кутом між ними)",
            label="Оберіть ознаку рівності для дослідження:",
        )

    return ab_slider, angle_slider, cd_slider, criterion_selector, ef_slider


@app.cell
def __(
    ab_slider,
    angle_slider,
    cd_slider,
    chapter_selector,
    criterion_selector,
    draw_adjacent_angles,
    draw_angle,
    draw_angle_bisector,
    draw_circle_elements,
    draw_congruence_showcase,
    draw_line_segment_ray,
    draw_segment_addition,
    draw_vertical_angles,
    ef_slider,
    get_scissors_widget_html,
    get_triangle_congruence_html,
    mo,
):
    _ch = chapter_selector.value

    if _ch == "intro":
        _ab = ab_slider.value if ab_slider is not None else 80
        _cd = cd_slider.value if cd_slider is not None else 110
        _ef = ef_slider.value if ef_slider is not None else 70

        _svg_lines = draw_line_segment_ray()
        _svg_add = draw_segment_addition(_ab, _cd, _ef)
        _svg_circle = draw_circle_elements()

        book_content = mo.vstack(
            [
                mo.md(
                    r"""
                    <div class="book-container">

                    <div class="chapter-heading">Вступ. Найпростіші геометричні фігури (§§ 1–12)</div>

                    <div class="section-heading">§ 1. Початкові геометричні поняття (§§ 1–4)</div>
                    <div class="book-p">
                    Частину простору, яку займає фізичне тіло, називають <strong>геометричним тілом</strong>.
                    Геометричне тіло відокремлюється від навколишнього простору <strong>поверхнею</strong>. Частина поверхні відокремлюється від сусідньої частини <strong>лінією</strong>, а частина лінії — <strong>точкою</strong>.
                    </div>

                    <div class="book-p">
                    Геометричне тіло, поверхня, лінія і точка в реальному світі не існують окремо. Проте за допомогою абстрагування ми можемо розглядати поверхню незалежно від тіла, лінію — незалежно від поверхні, а точку — незалежно від лінії. У математичній моделі:
                    <ul>
                        <li><strong>Поверхня</strong> не має товщини.</li>
                        <li><strong>Лінія</strong> не має ні товщини, ні ширини (має тільки довжину).</li>
                        <li><strong>Точка</strong> не має жодних розмірів (ні довжини, ні ширини, ні висоти).</li>
                    </ul>
                    </div>

                    <div class="feynman-box">
                        <strong>🧠 Інтуїція Фейнмана: Чому геометричну точку неможливо розрізати навпіл?</strong><br>
                        Уяви піщинку на морському березі. Вона крихітна, але якщо покласти її під мікроскоп, вона виявиться велетенською скелею з тріщинами, шириною і висотою. Ти можеш розколоти її молотком на дві половинки.<br>
                        Але в геометрії <strong>точка</strong> — це не цятка олівця на папері. Точка — це <strong>чиста адреса в просторі</strong>, координата «тут і більше ніде». Вона не має розмірів, тому її неможливо збільшити в мікроскоп, зменшити чи розрізати навпіл!
                    </div>

                    <div class="book-p">
                    Будь-яку сукупність точок, ліній, поверхонь або тіл, розміщених у просторі певним чином, називають <strong>геометричною фігурою</strong>.
                    Науку про властивості геометричних фігур називають <strong>геометрією</strong> (від грецьких слів «гео» — земля і «метрео» — вимірюю).
                    </div>

                    <div class="book-p">
                    Наочне уявлення про пряму дає туго натягнута нитка або промінь світла. Пряма має основну аксіому:
                    <strong>через будь-які дві різні точки можна провести одну й тільки одну пряму</strong>.
                    Звідси випливає: дві різні прямі можуть перетинатися не більш ніж в одній точці.
                    </div>

                    <div class="book-p">
                    Пряма лінія нескінченно продовжується в обидва боки (рис. 1). Частину прямої, обмежену з обох боків двома точками, називають <strong>відрізком</strong> (відрізок $CD$, рис. 2). 
                    Частину прямої, обмежену лише з одного боку початковою точкою, називають <strong>променем</strong> (рис. 3).
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">📐 Креслення Кисельова: Пряма, відрізок і промінь</div>
                    """
                ),
                mo.Html(_svg_lines.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="misconception-box">
                        <strong>⚠️ Пастка мислення: Пряма лінія не має «кінців»!</strong><br>
                        Часто учні малюють у зошиті лінію завдовжки 5 см і кажуть: «Це пряма $AB$». Пам'ятай: пряма нескінченна в обидва боки! Те, що має початок і кінець — це <strong>відрізок</strong>. Те, що має початок, але не має кінця — це <strong>промінь</strong>.
                    </div>

                    <div class="section-heading">§ 2. Дії над відрізками (§§ 5–7)</div>
                    <div class="book-p">
                    Два відрізки вважають <strong>рівними</strong>, якщо їх можна накласти один на один так, щоб збіглися обидва їхні кінці. Щоб відкласти на прямій відрізок, рівний даному, використовують <strong>циркуль</strong>.
                    </div>

                    <div class="book-p">
                    <strong>Сумою відрізків</strong> $AB$, $CD$, $EF$ називають відрізок $MQ$, складений із частин $MN = AB$, $NP = CD$, $PQ = EF$, відкладених послідовно на одній прямій в одному напрямку (рис. 5):
                    $$MQ = AB + CD + EF$$
                    Сума відрізків підпорядковується переставній та сполучній властивостям додавання.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">🕹️ Живе креслення: Додавання відрізків на прямій (змінюй довжини повзунками)</div>
                    """
                ),
                mo.hstack([ab_slider, cd_slider, ef_slider]),
                mo.Html(_svg_add.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="section-heading">§ 3. Коло та круг (§§ 8–10)</div>
                    <div class="book-p">
                    Якщо одну ніжку циркуля закріпити в точці $O$, а іншою обертатися навколо неї, олівець накреслить <strong>коло</strong> — замкнену лінію, усі точки якої однаково віддалені від центра $O$ (рис. 6).
                    </div>

                    <div class="book-p">
                    Відрізки $OA$, $OB$, що сполучають центр із точками кола, називаються <strong>радіусами</strong> ($r$). Усі радіуси одного кола рівні. Пряма, що перетинає коло у двох точках, називається <strong>січною</strong> ($s$); відрізок із кінцями на колі — <strong>хордою</strong> ($EF$); хорда, що проходить через центр, — <strong>діаметром</strong> ($CD$, $d = 2r$). Частина кола називається <strong>дугою</strong>.
                    </div>

                    <div class="book-p">
                    Частина площини, обмежена колом, називається <strong>кругом</strong>. Частина круга між двома радіусами є <strong>сектором</strong> ($AOB$), а частина між хордою та дугою — <strong>сегментом</strong>.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">📐 Креслення: Коло, круг та їхні складові елементи</div>
                    """
                ),
                mo.Html(_svg_circle.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="misconception-box">
                        <strong>⚠️ Пастка мислення: Коло — це обруч, а круг — це монета!</strong><br>
                        <strong>Коло</strong> — це тонка межова лінія (як гімнастичний обруч чи кільце). Воно має довжину, але не має площі.<br>
                        <strong>Круг</strong> — це плоска суцільна фігура разом із внутрішньою областю (як монета чи диск). Круг має площу!
                    </div>

                    <div class="section-heading">§ 4. Площина та поділ геометрії (§§ 11–12)</div>
                    <div class="book-p">
                    Наочне уявлення про площину дає поверхня спокійної води або рівного скла. Для площини фундаментальними є дві властивості:
                    <ol>
                        <li>Якщо дві точки прямої лежать у площині, то вся пряма повністю лежить у цій площині.</li>
                        <li>Будь-яку частину площини можна сумістити з будь-яким іншим місцем тієї самої площини, зокрема й після перевертання.</li>
                    </ol>
                    </div>

                    <div class="book-p">
                    Геометрія поділяється на <strong>планіметрію</strong> (вивчає фігури на площині) та <strong>стереометрію</strong> (вивчає просторові тіла: куб, кулю, піраміду). 7 клас цілком присвячено планіметрії!
                    </div>

                    </div>
                    """
                ),
            ]
        )

    elif _ch == "angles":
        _a = angle_slider.value if angle_slider is not None else 60
        _svg_angle = draw_angle(_a)
        _svg_adj = draw_adjacent_angles(_a)
        _svg_vert = draw_vertical_angles(_a)
        _svg_bis = draw_angle_bisector(_a)

        book_content = mo.vstack(
            [
                mo.md(
                    r"""
                    <div class="book-container">

                    <div class="chapter-heading">Розділ 1. Кути та їх вимірювання. Суміжні та вертикальні кути (§§ 13–26)</div>

                    <div class="section-heading">13. Поняття про кут та його елементи</div>
                    <div class="book-p">
                    Фігура, утворена двома променями ($OA$ і $OB$, рис. 8), що виходять з однієї точки, називається <strong>кутом</strong>. 
                    Промені, які утворюють кут, називаються <strong>сторонами кута</strong>, а точка $O$, з якої вони виходять, — <strong>вершиною кута</strong>. 
                    Сторони кута слід уявляти собі нескінченно продовженими від вершини.
                    </div>

                    <div class="book-p">
                    Кут зазвичай позначають трьома буквами, з яких середня ставиться біля вершини, а крайні — біля будь-яких точок на сторонах; наприклад, кажуть: «кут $AOB$» або «кут $BOA$». Проте можна позначати кут і однією буквою, поставленою біля вершини (кут $O$), якщо при цій вершині немає інших кутів. Слово «кут» на письмі замінюють символом $\angle$.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">🕹️ Живе векторне креслення кута AOB (рухай повзунок)</div>
                    """
                ),
                angle_slider,
                mo.Html(_svg_angle.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="feynman-box">
                        <strong>🧠 Інтуїція Фейнмана: Кут — це динамічний процес повороту!</strong><br>
                        Коли ми дивимося на креслення в зошиті, кут здається застиглим трикутним шматочком паперу. 
                        Проте в реальному фізичному світі кут — це <strong>міра обертання</strong>.<br>
                        Уяви стрілку годинника чи промінь обертового маяка. Спочатку промінь лежав уздовж рейки $OB$. Потім його повернули навколо шарніра $O$ до положення $OA$. 
                        Самі промені нескінченні, тому довжина намальованих ліній у зошиті ніяк не змінює величину самого кута!
                    </div>

                    <div class="section-heading">14–16. Рівність кутів, розгорнутий і повний кути</div>
                    <div class="book-p">
                    Два кути вважаються <strong>рівними</strong>, якщо при накладанні вони можуть повністю суміститися. Припустимо, що ми накладаємо кут $AOB$ на кут $A_1O_1B_1$ так, щоб вершина $O$ збіглася з $O_1$, сторона $OB$ пішла по $O_1B_1$, і щоб кути накрили один одного своїми внутрішніми областями. Якщо при цьому сторона $OA$ суміститься з $O_1A_1$, то кути рівні.
                    </div>

                    <div class="book-p">
                    Коли сторони кута є доповняльними променями (становлять продовження одна одної та утворюють одну пряму лінію), такий кут називається <strong>розгорнутим</strong>. Його градусна міра дорівнює $180^\circ$. Внутрішня область розгорнутого кута становить половину всієї площини. Кут у $360^\circ$ називається <strong>повним кутом</strong>.
                    </div>

                    <div class="section-heading">18–21. Градуси, види кутів та бісектриса</div>
                    <div class="book-p">
                    Кут у $90^\circ$ (половина розгорнутого кута) називають <strong>прямим кутом</strong>. Кут, менший від прямого, називається <strong>гострим</strong>, а більший за прямий, але менший від розгорнутого, — <strong>тупим</strong>.
                    </div>
                    <div class="book-p">
                    Промінь, що виходить з вершини кута і ділить його навпіл (на два рівні кути), називається <strong>бісектрисою кута</strong>.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">📐 Креслення: Бісектриса ділить кут рівно на дві однакові половинки</div>
                    """
                ),
                mo.Html(_svg_bis.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="section-heading">22. Суміжні кути та їхня головна теорема</div>
                    <div class="book-p">
                    Два кути називаються <strong>суміжними</strong>, якщо одна сторона в них спільна, а дві інші сторони є доповняльними променями (утворюють одну суцільну пряму лінію).
                    </div>

                    <div class="theorem-box">
                        <strong>🎯 Теорема про суму суміжних кутів:</strong><br>
                        Сума двох суміжних кутів завжди дорівнює $180^\circ$ (розгорнутому куту):
                        $$\angle \alpha + \angle \beta = 180^\circ$$
                    </div>

                    <div class="book-p">
                    <em>Доведення:</em> Оскільки сторони, що не є спільними, утворюють пряму лінію, то разом зі спільною стороною вони утворюють розгорнутий кут. А розгорнутий кут дорівнює $180^\circ$. Отже, сума суміжних кутів дорівнює $180^\circ$.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">🎯 Живе креслення суміжних кутів: α + β = 180°</div>
                    """
                ),
                mo.Html(_svg_adj.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="misconception-box">
                        <strong>⚠️ Пастка мислення: 180° ≠ обов'язково суміжні!</strong><br>
                        Не будь-які два кути, сума яких дорівнює $180^\circ$, є суміжними! 
                        Щоб кути були суміжними, вони обов'язково повинні мати <strong>спільну вершину</strong> та <strong>спільну сторону</strong>. Якщо один кут $60^\circ$ накреслений угорі зошита, а інший $120^\circ$ — унизу, вони не є суміжними, хоч їхня сума й дорівнює $180^\circ$.
                    </div>

                    <div class="section-heading">25. Вертикальні кути та їхня властивість</div>
                    <div class="book-p">
                    Два кути називаються <strong>вертикальними</strong>, якщо сторони одного кута є доповняльними променями сторін другого (утворені при перетині двох прямих ліній).
                    </div>

                    <div class="theorem-box">
                        <strong>🎯 Теорема про вертикальні кути:</strong><br>
                        Вертикальні кути рівні між собою:
                        $$\angle 1 = \angle 3, \quad \angle 2 = \angle 4$$
                    </div>

                    <div class="book-p">
                    <em>Доведення:</em> Кут $\angle 1$ і кут $\angle 2$ є суміжними, тому $\angle 1 + \angle 2 = 180^\circ$, звідки $\angle 1 = 180^\circ - \angle 2$. 
                    Кут $\angle 3$ і кут $\angle 2$ також є суміжними, тому $\angle 3 + \angle 2 = 180^\circ$, звідки $\angle 3 = 180^\circ - \angle 2$. 
                    Оскільки праві частини рівні, то й ліві частини рівні: $\angle 1 = \angle 3$.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">🕹️ Тактильна пісочниця ножиць (потягни синю точку A пальцем або мишкою)</div>
                    """
                ),
                mo.Html(get_scissors_widget_html()),
                mo.Html(_svg_vert.as_svg()),
                mo.md(
                    r"""
                    </div>

                    <div class="feynman-box">
                        <strong>🧠 Інтуїція ножиць:</strong><br>
                        Уяви звичайні кравецькі ножиці. Кожне лезо разом із протилежною ручкою — це суцільна жорстка пряма смуга сталі, закріплена на центральному шарнірі $O$. Коли ти розкриваєш передні леза на кут $\alpha$, задні ручки через жорсткість металу змушені дзеркально розкритися рівно на такий самий кут!
                    </div>

                    </div>
                    """
                ),
            ]
        )

    else:
        # Розділ 2: Трикутники
        _crit = criterion_selector.value if criterion_selector is not None else "SAS"
        _svg_crit = draw_congruence_showcase(_crit)

        _feynman_crit_notes = {
            "SAS": (
                "<strong>🧠 Інтуїція жорсткого кута (САК):</strong><br>"
                "Коли зафіксовано дві рейки $AC$ і $BC$ та жорстко задано кут між ними $\\angle C$, "
                "кінці рейок $A$ та $B$ більше не можуть зрушити ані на міліметр. "
                "Третя сторона $AB$ натягується між ними абсолютно однозначно!"
            ),
            "ASA": (
                "<strong>🧠 Інтуїція тріангуляції та маяка (АСА):</strong><br>"
                "Якщо відома довжина берегової лінії $AC$ та виміряно кути на корабель у морі з обох кінців, "
                "промені зору можуть перетнутися лише в одній точці простору. Корабель не має свободи вибору!"
            ),
            "SSS": (
                "<strong>🧠 Чому кран і ферма даху будуються з трикутників (ССС):</strong><br>"
                "З'єднай 3 дерев'яні планки цвяхами — таку конструкцію неможливо деформувати, не зламавши планок. "
                "Чотирикутник хитається, а трикутник — моноліт! Фіксуючи 3 сторони, ми намертво блокуємо всі кути."
            ),
        }

        book_content = mo.vstack(
            [
                mo.md(
                    r"""
                    <div class="book-container">

                    <div class="chapter-heading">Розділ 2. Трикутники та три ознаки їхньої рівності (§§ 27–45)</div>

                    <div class="section-heading">30–33. Поняття про трикутник та його елементи</div>
                    <div class="book-p">
                    Фігура, утворена замкненою ламаною лінією з трьох ланок, називається <strong>трикутником</strong>. 
                    Точки з'єднання називаються <strong>вершинами трикутника</strong>, а відрізки — його <strong>сторонами</strong>. 
                    Сума довжин усіх трьох сторін називається <strong>периметром</strong> ($P = a + b + c$).
                    </div>

                    <div class="book-p">
                    Трикутники класифікують за сторонами: <strong>різносторонні</strong> (всі сторони різної довжини), <strong>рівнобедрені</strong> (дві сторони рівні між собою) та <strong>рівносторонні</strong> (всі три сторони рівні).<br>
                    За кутами трикутники бувають: <strong>гострокутні</strong> (всі три кути гострі), <strong>прямокутні</strong> (мають прямий кут $90^\circ$, сторони називаються <em>катетами</em> та <em>гіпотенузою</em>) та <strong>тупокутні</strong> (мають один тупий кут).
                    </div>

                    <div class="book-p">
                    У кожному трикутнику розрізняють три найважливіші відрізки:
                    <ul>
                        <li><strong>Медіана</strong> — відрізок, що сполучає вершину трикутника із серединою протилежної сторони.</li>
                        <li><strong>Бісектриса</strong> — відрізок бісектриси кута від вершини до перетину з протилежною стороною.</li>
                        <li><strong>Висота</strong> — перпендикуляр, опущений з вершини на протилежну сторону або її продовження.</li>
                    </ul>
                    </div>

                    <div class="section-heading">34. Властивості рівнобедреного трикутника</div>
                    <div class="book-p">
                    У рівнобедреному трикутнику рівні сторони називаються <strong>бічними сторонами</strong>, а третя сторона — <strong>основою</strong>.
                    </div>

                    <div class="theorem-box">
                        <strong>🎯 Теореми про рівнобедрений трикутник:</strong><br>
                        1. У рівнобедреному трикутнику <strong>кути при основі рівні</strong>: $\angle A = \angle B$.<br>
                        2. <strong>Бісектриса</strong>, проведена до основи рівнобедреного трикутника, є одночасно і його <strong>медіаною</strong>, і <strong>висотою</strong>.
                    </div>

                    <div class="section-heading">37–38. Три ознаки рівності трикутників</div>
                    <div class="book-p">
                    Два трикутники називаються <strong>рівними</strong>, якщо їх можна сумістити способом накладання. У рівних трикутниках усі відповідні сторони і всі відповідні кути рівні.
                    Проте щоб довести рівність, не обов'язково перевіряти всі 6 елементів — достатньо перевірити лише 3 пари згідно з ознаками!
                    </div>

                    <div class="theorem-box">
                        <strong>🎯 Три ознаки рівності трикутників:</strong><br>
                        <strong>1. Перша ознака (за двома сторонами і кутом між ними — САК):</strong><br>
                        Якщо дві сторони і кут між ними одного трикутника відповідно дорівнюють двом сторонам і куту між ними іншого трикутника, то такі трикутники рівні.<br><br>
                        <strong>2. Друга ознака (за стороною і прилеглими кутами — АСА):</strong><br>
                        Якщо сторона і прилеглі до неї кути одного трикутника відповідно дорівнюють стороні та прилеглим до неї кутам іншого трикутника, то такі трикутники рівні.<br><br>
                        <strong>3. Третя ознака (за трьома сторонами — ССС):</strong><br>
                        Якщо три сторони одного трикутника відповідно дорівнюють трьом сторонам іншого трикутника, то такі трикутники рівні.
                    </div>

                    <div class="widget-card">
                        <div class="widget-title">📐 Дослідження ознак рівності на векторному кресленні:</div>
                    """
                ),
                criterion_selector,
                mo.Html(_svg_crit.as_svg()),
                mo.md(
                    f"""
                    <div class="feynman-box">
                        {_feynman_crit_notes.get(_crit, "")}
                    </div>
                    """
                ),
                mo.md(
                    r"""
                    <div class="widget-card">
                        <div class="widget-title">🕹️ Тактильне накладання трикутників (перетягни помаранчевий трикутник за точку A₁ на синій)</div>
                    """
                ),
                mo.Html(get_triangle_congruence_html()),
                mo.md(
                    r"""
                    </div>

                    <div class="misconception-box">
                        <strong>⚠️ Пастка мислення: Чому ознаки ССК не існує?</strong><br>
                        Якщо дві сторони і кут НЕ між ними рівні, трикутники <strong>не обов'язково рівні</strong>! 
                        Вільна сторона може засікти протилежний промінь у двох різних точках, утворивши два абсолютно різні трикутники (один гострокутний, інший тупокутний). Кут обов'язково має бути СТРОГО між сторонами (САК)!
                    </div>

                    </div>
                    """
                ),
            ]
        )

    return (book_content,)


@app.cell
def __(book_content):
    book_content
    return


@app.cell
def __(chapter_selector, mo):
    # Блок перевірки знань (Задачі Кисельова з автоматичною перевіркою SymPy)
    _ch = chapter_selector.value

    if _ch == "intro":
        task_label = (
            "🎯 Задача Кисельова (Додавання відрізків): "
            "На прямій послідовно відкладено відрізки AB = 4.5 см, CD = 3.2 см та EF = 2.8 см. "
            "Знайди довжину суми відрізків MQ = AB + CD + EF:"
        )
        task_placeholder = "Введи число або вираз (наприклад: 10.5 або 4.5 + 3.2 + 2.8)"
    elif _ch == "angles":
        task_label = (
            "🎯 Задача Кисельова (Вправа 1 зі с. 19): "
            "Один із суміжних кутів дорівнює 42°. Обчисли градусну міру другого кута:"
        )
        task_placeholder = "Введи число або вираз (наприклад: 138 або 180 - 42)"
    else:
        task_label = (
            "🎯 Задача Кисельова на ознаки рівності: "
            "У трикутниках △ABC та △A₁B₁C₁ відомо: AB = 6.5 см, AC = 9 см, ∠A = 50° та A₁B₁ = 6.5 см, A₁C₁ = 9 см, ∠A₁ = 50°. "
            "Трикутники рівні за ознакою САК. Якщо BC = 7.2 см, чому дорівнює сторона B₁C₁?"
        )
        task_placeholder = "Введи число (наприклад: 7.2)"

    task_input = mo.ui.text(
        placeholder=task_placeholder,
        label=task_label,
    )

    mo.vstack(
        [
            mo.Html(
                "<div class='book-container'><div class='chapter-heading'>📝 Перевір себе (Задачі Кисельова)</div></div>"
            ),
            task_input,
        ]
    )
    return (task_input,)


@app.cell
def __(
    chapter_selector,
    mo,
    task_input,
    verify_adjacent_angle,
    verify_congruence_mission,
    verify_segment_addition,
):
    if task_input.value:
        _val = task_input.value.strip()
        _ch = chapter_selector.value

        if _ch == "intro":
            _res = verify_segment_addition(4.5, 3.2, 2.8, _val)
        elif _ch == "angles":
            _res = verify_adjacent_angle(42.0, _val)
        else:
            _res = verify_congruence_mission("B₁C₁", 7.2, _val)

        if _res["correct"]:
            badge = mo.callout(mo.md(_res["message"]), kind="success")
        else:
            badge = mo.callout(mo.md(_res["message"]), kind="danger")
    else:
        badge = mo.md(
            "<div class='book-container'><em>Введи відповідь у поле вище, і система комп'ютерної алгебри SymPy миттєво перевірить твій результат.</em></div>"
        )

    badge
    return (badge,)


if __name__ == "__main__":
    app.run()
