"""SymPy analytical geometry brain and answer verification engine.

Uses sympy.geometry for exact calculations, theorem proofs, and verifying student solutions.
"""

from __future__ import annotations

import sympy as sp
from sympy.geometry import Point, Triangle


def parse_math_input(expr_str: str) -> sp.Expr | None:
    """Safely parse user mathematical input using SymPy."""
    cleaned = expr_str.strip().replace(",", ".").replace("°", "")
    if not cleaned:
        return None
    try:
        return sp.sympify(cleaned)
    except Exception:
        return None


def verify_adjacent_angle(given_alpha_deg: float, user_answer_str: str) -> dict:
    """Перевіряє правильність обчислення суміжного кута β = 180° - α."""
    parsed = parse_math_input(user_answer_str)
    if parsed is None:
        return {
            "correct": False,
            "message": "⚠️ Введи число або математичний вираз (наприклад, 180 - 65 або 115).",
        }

    expected = 180 - given_alpha_deg
    try:
        user_val = float(parsed.evalf())
        is_correct = abs(user_val - expected) < 1e-4
        if is_correct:
            return {
                "correct": True,
                "message": f"🎉 Точно! Сума суміжних кутів {given_alpha_deg:.0f}° + {user_val:.0f}° = 180°.",
                "expected": expected,
            }
        else:
            return {
                "correct": False,
                "message": f"❌ Не зовсім. Твоя відповідь {user_val:.0f}°. Пам'ятай: сума суміжних кутів завжди дорівнює 180° (тобто 180° - {given_alpha_deg:.0f}°).",
                "expected": expected,
            }
    except Exception:
        return {"correct": False, "message": "⚠️ Помилка обчислення виразу."}


def verify_vertical_angles(given_angle_1: float, user_angle_3: str, user_angle_2: str) -> dict:
    """Перевіряє правильність обчислення вертикального (∠3) та суміжних кутів (∠2)."""
    p3 = parse_math_input(user_angle_3)
    p2 = parse_math_input(user_angle_2)

    if p3 is None or p2 is None:
        return {"correct": False, "message": "⚠️ Заповни обидва поля для кутів."}

    exp_3 = given_angle_1
    exp_2 = 180 - given_angle_1

    try:
        val_3 = float(p3.evalf())
        val_2 = float(p2.evalf())

        c3 = abs(val_3 - exp_3) < 1e-4
        c2 = abs(val_2 - exp_2) < 1e-4

        if c3 and c2:
            return {
                "correct": True,
                "message": f"🎉 Бездоганно! Вертикальний кут ∠3 = {val_3:.0f}°, а суміжний ∠2 = {val_2:.0f}°.",
            }
        elif not c3:
            return {
                "correct": False,
                "message": f"❌ Помилка в ∠3: вертикальні кути рівні між собою! ∠3 має дорівнювати ∠1 ({given_angle_1:.0f}°).",
            }
        else:
            return {
                "correct": False,
                "message": f"❌ Помилка в ∠2: кут ∠2 є суміжним до ∠1, його градусна міра 180° - {given_angle_1:.0f}° = {exp_2:.0f}°.",
            }
    except Exception:
        return {"correct": False, "message": "⚠️ Помилка обчислення виразів."}


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
    else:
        return {
            "correct": False,
            "message": "❌ Ні, тут діє інша ознака. Зверни увагу на те, чи кут лежить саме між даними сторонами, чи кути прилеглі до сторони!",
        }


def verify_congruence_mission(
    target_side_name: str,
    expected_length: float,
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
            "message": "⚠️ Введи довжину сторони у числовому або формульному вигляді.",
        }

    side_val = float(p_side.evalf())
    side_ok = abs(side_val - expected_length) < 1e-4

    if target_angle_name and expected_angle is not None and user_angle_str:
        p_ang = parse_math_input(user_angle_str)
        if p_ang is None:
            return {"correct": False, "message": "⚠️ Введи градусну міру кута."}
        ang_val = float(p_ang.evalf())
        ang_ok = abs(ang_val - expected_angle) < 1e-4

        if side_ok and ang_ok:
            return {
                "correct": True,
                "message": f"🎉 Блискуче! Оскільки △ABC = △A₁B₁C₁, то {target_side_name} = {expected_length:.1f} та {target_angle_name} = {expected_angle:.0f}°.",
            }
        elif not side_ok:
            return {
                "correct": False,
                "message": f"❌ Помилка у стороні {target_side_name}. Відповідна сторона дорівнює {expected_length:.1f}.",
            }
        else:
            return {
                "correct": False,
                "message": f"❌ Помилка у куті {target_angle_name}. Відповідний кут дорівнює {expected_angle:.0f}°.",
            }

    if side_ok:
        return {
            "correct": True,
            "message": f"🎉 Точно! {target_side_name} = {expected_length:.1f} за ознакою рівності.",
        }
    else:
        return {
            "correct": False,
            "message": f"❌ Невірно. За рівністю трикутників {target_side_name} має дорівнювати {expected_length:.1f}.",
        }


def verify_segment_addition(ab: float, cd: float, ef: float, user_answer_str: str) -> dict:
    """Перевіряє правильність обчислення довжини суми відрізків MQ = AB + CD + EF."""
    parsed = parse_math_input(user_answer_str)
    if parsed is None:
        return {
            "correct": False,
            "message": "⚠️ Введи число або математичний вираз (наприклад, 4.5 + 3.2 + 2.8).",
        }
    expected = ab + cd + ef
    try:
        user_val = float(parsed.evalf())
        if abs(user_val - expected) < 1e-4:
            return {
                "correct": True,
                "message": f"🎉 Чудово! Довжина суми відрізків MQ = {ab} + {cd} + {ef} = {expected:.1f} см.",
                "expected": expected,
            }
        else:
            return {
                "correct": False,
                "message": f"❌ Неправильно. Твоя відповідь {user_val:.1f} см. Пам'ятай: MQ = AB + CD + EF = {ab} + {cd} + {ef} = {expected:.1f} см.",
                "expected": expected,
            }
    except Exception:
        return {"correct": False, "message": "⚠️ Помилка обчислення виразу."}
