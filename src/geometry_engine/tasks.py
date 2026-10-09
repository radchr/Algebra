"""«Перевір себе»: задачі до кожного уроку з перевіркою через SymPy.

Чисті дані + функції перевірки; застосунок лише показує поле вводу й результат.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from functools import partial

import sympy as sp

from .sympy_solver import (
    verify_adjacent_angle,
    verify_congruence_mission,
    verify_segment_addition,
)


@dataclass(frozen=True)
class CheckTask:
    text_uk: str
    placeholder: str
    check: Callable[[str], dict]
    reference_answer: sp.Expr
    prediction_prompt: str
    prediction_options: dict[str, str]
    prediction_answer: str
    prediction_explanation: str
    hints: tuple[str, str, str]


_SEGMENT_REFERENCE = sp.Rational("4.5") + sp.Rational("3.2") + sp.Rational("2.8")
_ANGLE_REFERENCE = sp.Integer(180) - sp.Integer(42)
_TRIANGLE_AB = sp.Integer(6)
_TRIANGLE_AC = sp.Integer(8)
_TRIANGLE_ANGLE = sp.Integer(90)
_TRIANGLE_REFERENCE = sp.simplify(
    sp.sqrt(
        _TRIANGLE_AB**2
        + _TRIANGLE_AC**2
        - 2 * _TRIANGLE_AB * _TRIANGLE_AC * sp.cos(sp.pi * _TRIANGLE_ANGLE / 180)
    )
)


TASKS: dict[str, CheckTask] = {
    "00_introduction": CheckTask(
        text_uk=(
            "🎯 **Додавання відрізків.** На прямій послідовно відкладено відрізки "
            "$AB = 4{,}5$ см, $CD = 3{,}2$ см та $EF = 2{,}8$ см. "
            "Знайди довжину їхньої суми $MQ = AB + CD + EF$."
        ),
        placeholder="Наприклад: 10,5 або 4,5 + 3,2 + 2,8",
        check=partial(verify_segment_addition, 4.5, 3.2, 2.8),
        reference_answer=_SEGMENT_REFERENCE,
        prediction_prompt=(
            "Якщо ті самі три відрізки переставити місцями, що станеться з довжиною їхньої суми?"
        ),
        prediction_options={
            "Сума збільшиться": "larger",
            "Сума не зміниться": "same",
            "Сума зменшиться": "smaller",
        },
        prediction_answer="same",
        prediction_explanation=(
            "Порядок не змінює загальної довжини: відрізки заповнюють ту саму сумарну відстань."
        ),
        hints=(
            "Подумай, що відбувається із загальною довжиною, коли доданки лише міняють місцями.",
            "Використай рівність $MQ = AB + CD + EF$.",
            "$MQ = 4{,}5 + 3{,}2 + 2{,}8 = 10{,}5$ см.",
        ),
    ),
    "01_angles": CheckTask(
        text_uk=(
            "🎯 **Вправа 1 (с. 19).** Один із суміжних кутів дорівнює $42^\\circ$. "
            "Обчисли градусну міру другого кута."
        ),
        placeholder="Наприклад: 138 або 180 - 42",
        check=partial(verify_adjacent_angle, 42),
        reference_answer=_ANGLE_REFERENCE,
        prediction_prompt=("Коли один із двох суміжних кутів збільшується, як змінюється другий?"),
        prediction_options={
            "Також збільшується": "grows",
            "Не змінюється": "fixed",
            "Зменшується": "shrinks",
        },
        prediction_answer="shrinks",
        prediction_explanation=(
            "Суміжні кути разом завжди дають 180°. Скільки додалося одному, стільки забралося в іншого."
        ),
        hints=(
            "Другий кут доповнює даний до розгорнутого кута.",
            r"Для суміжних кутів $\alpha + \beta = 180^\circ$.",
            r"$\beta = 180^\circ - 42^\circ = 138^\circ$.",
        ),
    ),
    "02_triangles_equality": CheckTask(
        text_uk=(
            "🎯 **Ознаки рівності.** У трикутниках $ABC$ і $A_1B_1C_1$: "
            f"$AB = A_1B_1 = {_TRIANGLE_AB}$ см, $AC = A_1C_1 = {_TRIANGLE_AC}$ см, "
            f"$\\angle A = \\angle A_1 = {_TRIANGLE_ANGLE}^\\circ$. "
            f"Трикутники рівні за ознакою САК. Якщо $BC = {_TRIANGLE_REFERENCE}$ см, "
            "чому дорівнює $B_1C_1$?"
        ),
        placeholder="Наприклад: 10",
        check=partial(verify_congruence_mission, "B₁C₁", _TRIANGLE_REFERENCE),
        reference_answer=_TRIANGLE_REFERENCE,
        prediction_prompt=(
            "Дві сторони трикутника залишили незмінними, але кут між ними збільшили. "
            "Чи залишиться третя сторона тієї самої довжини?"
        ),
        prediction_options={
            "Так, двох сторін достатньо": "same",
            "Ні, третя сторона зміниться": "changes",
            "Залежить лише від периметра": "perimeter",
        },
        prediction_answer="changes",
        prediction_explanation=(
            "Дві сторони без кута працюють як розкритий шарнір. Лише кут між ними фіксує третю сторону — саме тому в САК потрібен кут між сторонами."
        ),
        hints=(
            "Знайди, яка сторона другого трикутника відповідає стороні $BC$.",
            "У рівних трикутниках відповідні сторони рівні: $B_1C_1 = BC$.",
            "Оскільки $BC = 10$ см, то $B_1C_1 = 10$ см.",
        ),
    ),
}
