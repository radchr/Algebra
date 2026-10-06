"""Exact mathematical checks for geometry content blocks."""

from __future__ import annotations

from fractions import Fraction

from sympy import Rational, pi, simplify
from sympy.geometry import Line, Point

from .schema import AngleMeasure, AngleSumCheck, LineRelationCheck, MathCheck

STRAIGHT_ANGLE_ARCSECONDS = 180 * 3600


def supplement(measure: AngleMeasure) -> AngleMeasure:
    """Return the exact supplementary angle to ``measure``."""

    remainder = STRAIGHT_ANGLE_ARCSECONDS - measure.total_arcseconds
    if remainder < 0:
        raise ValueError("A supplementary angle requires a measure not greater than 180°")
    degrees, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return AngleMeasure(degrees=degrees, minutes=minutes, seconds=seconds)


def supplementary_bisectors_are_perpendicular(measure: AngleMeasure) -> bool:
    """Verify the bisector theorem using exact symbolic radians."""

    if not 0 <= measure.total_arcseconds <= STRAIGHT_ANGLE_ARCSECONDS:
        return False
    alpha = Rational(measure.total_arcseconds, 3600) * pi / 180
    beta = pi - alpha
    return simplify(alpha / 2 + beta / 2 - pi / 2) == 0


def _coordinate(value: str) -> Rational:
    """Parse a rational coordinate without evaluating arbitrary Python."""

    fraction = Fraction(value)
    return Rational(fraction.numerator, fraction.denominator)


def _line(check: LineRelationCheck, names: tuple[str, str]) -> Line:
    try:
        first = check.points[names[0]]
        second = check.points[names[1]]
    except KeyError as exc:
        raise ValueError(f"Unknown point in line definition: {exc.args[0]}") from exc

    point_a = Point(_coordinate(first[0]), _coordinate(first[1]))
    point_b = Point(_coordinate(second[0]), _coordinate(second[1]))
    if point_a == point_b:
        raise ValueError(f"Line points must be distinct: {names[0]}, {names[1]}")
    return Line(point_a, point_b)


def run_math_check(check: MathCheck) -> tuple[bool, str]:
    """Run a declared mathematical check and return a human-readable result."""

    if isinstance(check, AngleSumCheck):
        actual = sum(item.total_arcseconds for item in check.measures)
        expected = check.expected.total_arcseconds
        if actual == expected:
            return True, "Angle sum is exact"
        return False, f"Angle sum mismatch: {actual} arcseconds != {expected} arcseconds"

    if isinstance(check, LineRelationCheck):
        line_a = _line(check, check.line_a)
        line_b = _line(check, check.line_b)
        if check.relation == "parallel":
            passed = bool(line_a.is_parallel(line_b))
        else:
            passed = bool(line_a.is_perpendicular(line_b))
        return (
            passed,
            f"Lines are {check.relation}" if passed else f"Lines are not {check.relation}",
        )

    raise TypeError(f"Unsupported math check: {type(check).__name__}")
