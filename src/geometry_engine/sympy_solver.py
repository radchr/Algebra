"""SymPy analytical geometry brain and answer verification engine.

Uses sympy.geometry for exact calculations, theorem proofs, and verifying student solutions.

Відповіді учня порівнюються точно: введений вираз і очікуване значення
переводяться у раціональні числа SymPy, а рівність перевіряється як
``simplify(user - expected) == 0``. Довільний текст ніколи не передається
у ``sympify`` — спочатку він проходить білий список символів.
"""

from __future__ import annotations

import re

import sympy as sp
from sympy.geometry import Point, Triangle

# Дозволені символи після нормалізації: цифри, крапка, дужки, пробіли та + - * /
_ALLOWED_RE = re.compile(r"[0-9.+\-*/()\s]+")
# Одиниці виміру, які учень може дописати до відповіді («7,2 см», «138°»)
_UNIT_RE = re.compile(r"(градус\w*|град|см|мм|дм|м|°)", re.IGNORECASE)
_REPLACEMENTS = {
    ",": ".",
    "−": "-",  # типографський мінус
    "–": "-",
    "×": "*",
    "·": "*",
    ":": "/",
    "÷": "/",
    "^": "**",
}


def _exact(value: float | int | str | sp.Expr) -> sp.Rational:
    """Точне раціональне подання числа: 3.2 -> 16/5 (без двійкових похибок float)."""
    return sp.Rational(str(value))


def _fmt(value: sp.Expr | float) -> str:
    """Число для дитини: 138 -> «138», 10.5 -> «10,5», 1/3 -> «0,33»."""
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def parse_math_input(expr_str: str) -> sp.Expr | None:
    """Безпечно розбирає числовий вираз учня; повертає точне скінченне число або None."""
    if not isinstance(expr_str, str):
        return None
    cleaned = expr_str.strip()
    for old, new in _REPLACEMENTS.items():
        cleaned = cleaned.replace(old, new)
    cleaned = _UNIT_RE.sub("", cleaned).strip()
    if not cleaned or not _ALLOWED_RE.fullmatch(cleaned):
        return None
    try:
        value = sp.sympify(cleaned, rational=True)
    except (sp.SympifyError, SyntaxError, TypeError, ZeroDivisionError):
        return None
    if (
        not isinstance(value, sp.Expr)
        or not value.is_number
        or value.is_finite is not True
        or value.is_real is not True
    ):
        return None
    return value


def _equals(user_value: sp.Expr, expected: sp.Expr) -> bool:
    return sp.simplify(user_value - expected) == 0


def verify_adjacent_angle(given_alpha_deg: float, user_answer_str: str) -> dict:
    """Перевіряє правильність обчислення суміжного кута β = 180° - α."""
    parsed = parse_math_input(user_answer_str)
    if parsed is None:
        return {
            "correct": False,
            "message": "⚠️ Введи число або математичний вираз (наприклад, 180 - 65 або 115).",
        }

    alpha = _exact(given_alpha_deg)
    expected = 180 - alpha
    if _equals(parsed, expected):
        return {
            "correct": True,
            "message": f"🎉 Точно! Сума суміжних кутів {_fmt(alpha)}° + {_fmt(parsed)}° = 180°.",
            "expected": float(expected),
        }
    return {
        "correct": False,
        "message": (
            f"❌ Не зовсім. Твоя відповідь {_fmt(parsed)}°. Пам'ятай: сума суміжних кутів "
            f"завжди дорівнює 180° (тобто 180° - {_fmt(alpha)}°)."
        ),
        "expected": float(expected),
    }


def verify_vertical_angles(given_angle_1: float, user_angle_3: str, user_angle_2: str) -> dict:
    """Перевіряє правильність обчислення вертикального (∠3) та суміжних кутів (∠2)."""
    p3 = parse_math_input(user_angle_3)
    p2 = parse_math_input(user_angle_2)

    if p3 is None or p2 is None:
        return {"correct": False, "message": "⚠️ Заповни обидва поля для кутів числами."}

    angle_1 = _exact(given_angle_1)
    exp_3 = angle_1
    exp_2 = 180 - angle_1

    c3 = _equals(p3, exp_3)
    c2 = _equals(p2, exp_2)

    if c3 and c2:
        return {
            "correct": True,
            "message": f"🎉 Бездоганно! Вертикальний кут ∠3 = {_fmt(p3)}°, а суміжний ∠2 = {_fmt(p2)}°.",
        }
    if not c3:
        return {
            "correct": False,
            "message": f"❌ Помилка в ∠3: вертикальні кути рівні між собою! ∠3 має дорівнювати ∠1 ({_fmt(angle_1)}°).",
        }
    return {
        "correct": False,
        "message": f"❌ Помилка в ∠2: кут ∠2 є суміжним до ∠1, його градусна міра 180° - {_fmt(angle_1)}° = {_fmt(exp_2)}°.",
    }


def analyze_triangle_by_points(
    p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]
) -> dict:
    """Аналізує трикутник через модуль sympy.geometry."""
    A = Point(p1[0], p1[1])
    B = Point(p2[0], p2[1])
    C = Point(p3[0], p3[1])

    if Point.is_collinear(A, B, C):
        return {"valid": False, "message": "Точки лежать на одній прямій — трикутник вироджений!"}

    t = Triangle(A, B, C)

    return {
        "valid": True,
        "perimeter": float(t.perimeter.evalf()),
        "area": float(t.area.evalf()),
        "is_right": t.is_right(),
        "is_isosceles": t.is_isosceles(),
        "is_equilateral": t.is_equilateral(),
        "sides": [float(s.length.evalf()) for s in t.sides],
    }


def verify_congruence_criterion(selected_criterion: str, target_criterion: str = "SAS") -> dict:
    """Перевіряє правильність вибору ознаки рівності трикутників (САК, АСА, ССС)."""
    synonyms = {
        "SAS": ["SAS", "САК", "1", "перша", "перша ознака", "дві сторони і кут між ними"],
        "ASA": ["ASA", "АСА", "2", "друга", "друга ознака", "сторона і прилеглі кути"],
        "SSS": ["SSS", "ССС", "3", "третя", "третя ознака", "три сторони"],
    }
    sel = selected_criterion.strip().upper()
    target_syns = [s.upper() for s in synonyms.get(target_criterion, [target_criterion])]

    if sel in target_syns:
        descriptions = {
            "SAS": "🎉 Правильно! Це Перша ознака (САК): дві сторони та кут строго між ними.",
            "ASA": "🎉 Правильно! Це Друга ознака (АСА): сторона і два прилеглі до неї кути.",
            "SSS": "🎉 Правильно! Це Третя ознака (ССС): три відповідні сторони (жорсткість фігури).",
        }
        return {"correct": True, "message": descriptions.get(target_criterion, "🎉 Правильно!")}
    return {
        "correct": False,
        "message": "❌ Ні, тут діє інша ознака. Зверни увагу на те, чи кут лежить саме між даними сторонами, чи кути прилеглі до сторони!",
    }


def verify_congruence_mission(
    target_side_name: str,
    expected_length: float | int | str | sp.Expr,
    user_answer_str: str,
    target_angle_name: str | None = None,
    expected_angle: float | None = None,
    user_angle_str: str | None = None,
) -> dict:
    """Перевіряє розв'язок задачі на відповідні рівні елементи у рівних трикутниках."""
    p_side = parse_math_input(user_answer_str)
    if p_side is None:
        return {
            "correct": False,
            "message": "⚠️ Введи довжину сторони числом або виразом (наприклад, 7,2).",
        }

    length = _exact(expected_length)
    side_ok = _equals(p_side, length)

    if target_angle_name and expected_angle is not None and user_angle_str:
        p_ang = parse_math_input(user_angle_str)
        if p_ang is None:
            return {"correct": False, "message": "⚠️ Введи градусну міру кута числом."}
        angle = _exact(expected_angle)
        ang_ok = _equals(p_ang, angle)

        if side_ok and ang_ok:
            return {
                "correct": True,
                "message": f"🎉 Блискуче! Оскільки △ABC = △A₁B₁C₁, то {target_side_name} = {_fmt(length)} та {target_angle_name} = {_fmt(angle)}°.",
            }
        if not side_ok:
            return {
                "correct": False,
                "message": f"❌ Помилка у стороні {target_side_name}. Відповідна сторона дорівнює {_fmt(length)}.",
            }
        return {
            "correct": False,
            "message": f"❌ Помилка у куті {target_angle_name}. Відповідний кут дорівнює {_fmt(angle)}°.",
        }

    if side_ok:
        return {
            "correct": True,
            "message": f"🎉 Точно! {target_side_name} = {_fmt(length)}: у рівних трикутниках відповідні сторони рівні.",
        }
    return {
        "correct": False,
        "message": f"❌ Ні. У рівних трикутниках відповідні сторони рівні, тож {target_side_name} = {_fmt(length)}.",
    }


def verify_segment_addition(ab: float, cd: float, ef: float, user_answer_str: str) -> dict:
    """Перевіряє правильність обчислення довжини суми відрізків MQ = AB + CD + EF."""
    parsed = parse_math_input(user_answer_str)
    if parsed is None:
        return {
            "correct": False,
            "message": "⚠️ Введи число або математичний вираз (наприклад, 4,5 + 3,2 + 2,8).",
        }
    a, c, e = _exact(ab), _exact(cd), _exact(ef)
    expected = a + c + e
    if _equals(parsed, expected):
        return {
            "correct": True,
            "message": f"🎉 Чудово! Довжина суми відрізків MQ = {_fmt(a)} + {_fmt(c)} + {_fmt(e)} = {_fmt(expected)} см.",
            "expected": float(expected),
        }
    return {
        "correct": False,
        "message": (
            f"❌ Неправильно. Твоя відповідь {_fmt(parsed)} см. Пам'ятай: MQ = AB + CD + EF = "
            f"{_fmt(a)} + {_fmt(c)} + {_fmt(e)} = {_fmt(expected)} см."
        ),
        "expected": float(expected),
    }
