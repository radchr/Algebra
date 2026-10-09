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
    analyze_triangle_by_points,
    verify_adjacent_angle,
    verify_congruence_criterion,
    verify_congruence_mission,
    verify_segment_addition,
    verify_vertical_angles,
)


def test_svg_drawings_generate():
    """Ensure all svg drawing functions produce valid SVG strings."""
    d1 = draw_angle(45)
    assert "<svg" in d1.as_svg()

    d2 = draw_adjacent_angles(70)
    assert "<svg" in d2.as_svg()
    assert "α = 70°" in d2.as_svg()
    assert "β = 110°" in d2.as_svg()

    d3 = draw_vertical_angles(50)
    assert "<svg" in d3.as_svg()

    d4 = draw_angle_bisector(80)
    assert "<svg" in d4.as_svg()
    assert "бісектриса" in d4.as_svg()

    d5 = draw_triangle(120, 100, 60)
    assert "<svg" in d5.as_svg()

    d6 = draw_congruence_showcase("SAS")
    assert "<svg" in d6.as_svg()
    assert "САК" in d6.as_svg()

    d7 = draw_congruence_showcase("ASA")
    assert "<svg" in d7.as_svg()
    assert "АСА" in d7.as_svg()

    d8 = draw_congruence_showcase("SSS")
    assert "<svg" in d8.as_svg()
    assert "ССС" in d8.as_svg()

    d9 = draw_line_segment_ray()
    assert "<svg" in d9.as_svg()
    assert "Рис. 1" in d9.as_svg()
    assert "Рис. 2" in d9.as_svg()
    assert "Рис. 3" in d9.as_svg()

    d10 = draw_segment_addition(60, 90, 50)
    assert "<svg" in d10.as_svg()
    assert "Рис. 5" in d10.as_svg()
    assert "MQ = MN + NP + PQ" in d10.as_svg()

    d11 = draw_circle_elements()
    assert "<svg" in d11.as_svg()
    assert "Рис. 6" in d11.as_svg()
    assert "радіус" in d11.as_svg()


def test_verify_adjacent_angle():
    res_correct = verify_adjacent_angle(65, "115")
    assert res_correct["correct"] is True

    res_expr = verify_adjacent_angle(65, "180 - 65")
    assert res_expr["correct"] is True

    res_wrong = verify_adjacent_angle(65, "100")
    assert res_wrong["correct"] is False


def test_verify_segment_addition():
    res_correct = verify_segment_addition(4.5, 3.2, 2.8, "10.5")
    assert res_correct["correct"] is True

    res_expr = verify_segment_addition(4.5, 3.2, 2.8, "4.5 + 3.2 + 2.8")
    assert res_expr["correct"] is True

    res_wrong = verify_segment_addition(4.5, 3.2, 2.8, "9.5")
    assert res_wrong["correct"] is False


def test_verify_vertical_angles():
    res = verify_vertical_angles(50, "50", "130")
    assert res["correct"] is True

    res_bad = verify_vertical_angles(50, "60", "130")
    assert res_bad["correct"] is False


def test_analyze_triangle_by_points():
    res = analyze_triangle_by_points((0, 0), (3, 0), (0, 4))
    assert res["valid"] is True
    assert res["is_right"] is True
    assert abs(res["perimeter"] - 12.0) < 1e-4
    assert abs(res["area"] - 6.0) < 1e-4


def test_verify_congruence_criterion():
    assert verify_congruence_criterion("SAS", "SAS")["correct"] is True
    assert verify_congruence_criterion("САК", "SAS")["correct"] is True
    assert verify_congruence_criterion("ASA", "ASA")["correct"] is True
    assert verify_congruence_criterion("SSS", "SSS")["correct"] is True
    assert verify_congruence_criterion("SSS", "SAS")["correct"] is False


def test_verify_congruence_mission():
    res1 = verify_congruence_mission("A₁C₁", 12.5, "12.5")
    assert res1["correct"] is True

    res2 = verify_congruence_mission("A₁C₁", 12.5, "10 + 2.5")
    assert res2["correct"] is True

    res3 = verify_congruence_mission("A₁C₁", 12.5, "14")
    assert res3["correct"] is False

    res4 = verify_congruence_mission("A₁C₁", 10.0, "10", "∠A₁", 60.0, "60")
    assert res4["correct"] is True


def test_jsx_templates():
    from geometry_engine.jsx_templates import (
        get_scissors_widget_html,
        get_triangle_congruence_html,
    )

    h1 = get_scissors_widget_html()
    assert "<iframe" in h1
    assert "srcdoc=" in h1
    assert "jxgbox_scissors" in h1

    h2 = get_triangle_congruence_html()
    assert "<iframe" in h2
    assert "srcdoc=" in h2
    assert "jxgbox_triangles" in h2


def test_jsx_scissors_uses_initial_angle_and_has_network_fallback():
    from geometry_engine.jsx_templates import get_scissors_widget_html

    angle_30 = get_scissors_widget_html(initial_angle=30)
    angle_80 = get_scissors_widget_html(initial_angle=80)
    assert angle_30 != angle_80
    assert 'data-initial-angle="30"' in angle_30
    assert 'data-initial-angle="80"' in angle_80
    assert "Не вдалося завантажити JSXGraph" in angle_30


def test_all_jsx_widgets_have_visible_network_fallback():
    from geometry_engine.jsx_templates import (
        get_scissors_widget_html,
        get_triangle_congruence_html,
    )

    for widget_html in (get_scissors_widget_html(), get_triangle_congruence_html()):
        assert "Не вдалося завантажити JSXGraph" in widget_html


def test_book_database_figures():
    from geometry_engine.db import BookDatabase

    db = BookDatabase()
    assert db.count_figures("kiselev_geometry_1931") == 89

    # Test individual figure retrieval
    fig1 = db.get_figure("fig_001")
    assert fig1 is not None
    assert fig1.fig_num == 1
    assert "Пряма лінія" in fig1.title
    assert "<svg" in fig1.svg_content

    # Test page-based figure retrieval
    page9_figs = db.get_figures_for_page("kiselev_geometry_1931", 9)
    assert len(page9_figs) == 3
    assert [f.fig_num for f in page9_figs] == [1, 2, 3]


def test_figure_lookup_helpers():
    from geometry_engine.svg_drawings import (
        get_book_figure,
        get_book_figure_svg,
        render_figure_card,
    )

    fig = get_book_figure(1)
    assert fig is not None
    assert fig.fig_num == 1

    svg = get_book_figure_svg(1)
    assert svg is not None
    assert "<svg" in svg

    card = render_figure_card(1)
    assert "figure-card" in card
    assert "<svg" in card

    # Non-existent figure
    assert get_book_figure(9999) is None
    assert get_book_figure_svg(9999) is None
    missing_card = render_figure_card(9999)
    assert "figure-missing" in missing_card
