from hypothesis import given
from hypothesis import strategies as st

from geometry_pipeline.math_validation import (
    run_math_check,
    supplement,
    supplementary_bisectors_are_perpendicular,
)
from geometry_pipeline.schema import AngleMeasure, AngleSumCheck, LineRelationCheck


def test_kiselev_exercise_1_uses_exact_arcminutes() -> None:
    first = AngleMeasure(degrees=38, minutes=29)
    second = supplement(first)

    assert second == AngleMeasure(degrees=141, minutes=31)

    passed, _ = run_math_check(
        AngleSumCheck(
            kind="angle_sum",
            measures=[first, second],
            expected=AngleMeasure(degrees=180),
        )
    )
    assert passed


@given(
    degrees=st.integers(min_value=0, max_value=179),
    minutes=st.integers(min_value=0, max_value=59),
    seconds=st.integers(min_value=0, max_value=59),
)
def test_supplement_is_exact_for_all_valid_angles(
    degrees: int,
    minutes: int,
    seconds: int,
) -> None:
    measure = AngleMeasure(degrees=degrees, minutes=minutes, seconds=seconds)
    other = supplement(measure)

    assert measure.total_arcseconds + other.total_arcseconds == 180 * 3600
    assert supplementary_bisectors_are_perpendicular(measure)


def test_sympy_geometry_checks_perpendicular_lines() -> None:
    check = LineRelationCheck(
        kind="line_relation",
        relation="perpendicular",
        points={
            "A": ("-3", "0"),
            "O": ("0", "0"),
            "B": ("0", "5/2"),
        },
        line_a=("A", "O"),
        line_b=("O", "B"),
    )

    passed, _ = run_math_check(check)
    assert passed
