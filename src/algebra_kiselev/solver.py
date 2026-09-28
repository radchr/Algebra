"""
Symbolic math validation engine powered by SymPy for Kiselev Algebra.
"""

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def safe_parse_math(
    expression_str: str, allowed_symbols: list[str] | None = None
) -> tuple[sp.Expr | None, str | None]:
    """
    Safely parse math string into a SymPy expression.
    Supports implicit multiplication (e.g., '4a' -> '4*a') and '^' as power.
    """
    if not expression_str or not expression_str.strip():
        return None, "Порожнє поле вводу / Empty input"

    cleaned = expression_str.strip().replace("−", "-").replace("·", "*").replace(":", "/")

    local_dict = {}
    if allowed_symbols:
        for s in allowed_symbols:
            local_dict[s] = sp.Symbol(s)

    try:
        expr = parse_expr(cleaned, local_dict=local_dict, transformations=TRANSFORMATIONS)
        return expr, None
    except Exception as e:
        return None, f"Синтаксична помилка: {e!s}"


def check_answer_equivalence(
    user_str: str, expected_str: str, variables: list[str] | None = None, lang: str = "uk"
) -> tuple[bool, str, str]:
    """
    Checks if user math input is algebraically equivalent to expected expression.
    Returns: (is_correct, feedback_message, rendered_user_latex)
    """
    user_expr, err = safe_parse_math(user_str, allowed_symbols=variables)
    if err:
        msg = (
            "⚠️ Не вдалося розпізнати формулу: перевірте правильність знаків або закриття дужок."
            if lang == "uk"
            else "⚠️ Could not parse expression: please check mathematical symbols or closing brackets."
        )
        return False, msg, ""

    expected_expr, _ = safe_parse_math(expected_str, allowed_symbols=variables)
    if expected_expr is None:
        return False, "Помилка конфігурації еталонної відповіді", ""

    user_latex = sp.latex(user_expr)

    # Difference simplification
    try:
        diff = sp.simplify(user_expr - expected_expr)
        if diff == 0:
            msg = (
                "Вираз алгебраїчно тотожний правильній відповіді."
                if lang == "uk"
                else "Expression is algebraically equivalent to the correct answer."
            )
            return True, msg, user_latex
        else:
            msg = (
                "Вираз не є тотожним очікуваній відповіді."
                if lang == "uk"
                else "Expression is not equivalent to the expected answer."
            )
            return False, msg, user_latex
    except Exception as e:
        msg = f"Помилка обчислення: {e}" if lang == "uk" else f"Evaluation error: {e}"
        return False, msg, user_latex
