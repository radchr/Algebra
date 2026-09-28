import marimo

__generated_with = "0.25.0"
app = marimo.App(
    app_title="Інтерактивний Кисельов: Елементи Алгебри",
    layout_file=None,
)


@app.cell
def __():
    import json
    from pathlib import Path

    import marimo as mo
    import sympy as sp

    from algebra_kiselev.solver import check_answer_equivalence

    return check_answer_equivalence, json, mo, Path, sp


@app.cell
def __(Path, json):
    # Load dataset
    dataset_file = Path("data/problems/section_01.json")
    if dataset_file.exists():
        with open(dataset_file, encoding="utf-8") as f:
            problems_data = json.load(f)
    else:
        problems_data = []
    return dataset_file, problems_data


@app.cell
def __(mo):
    # Top controls: Language selector
    lang_toggle = mo.ui.radio(
        options=["🇺🇦 Українська", "🇬🇧 English"],
        value="🇺🇦 Українська",
        label="🌍 Мова / Language:",
    )
    return (lang_toggle,)


@app.cell
def __(lang_toggle, mo, problems_data):
    is_uk = "Українська" in lang_toggle.value

    # Build options for selector
    options_map = {}
    for _p in problems_data:
        _num = _p["id"]
        _title = _p["text_uk"] if is_uk else _p["text_en"]
        _short_title = _title if len(_title) < 55 else _title[:52] + "..."
        _key = f"№{_num}. {_short_title}"
        options_map[_key] = _num

    problem_select = mo.ui.dropdown(
        options=options_map,
        value=list(options_map.keys())[0] if options_map else None,
        label="📖 Оберіть задачу:" if is_uk else "📖 Select problem:",
    )
    return is_uk, options_map, problem_select


@app.cell
def __(is_uk, lang_toggle, mo, problem_select):
    header_view = mo.vstack(
        [
            mo.md(
                """
            # 📐 Інтерактивний задачник А. П. Кисельова
            ### *«Задачи и упражнения к элементам алгебры» (4-е видання, 1931 р.)*
            """
                if is_uk
                else """
            # 📐 Interactive A. P. Kiselev Problem Book
            ### *«Problems & Exercises in Elements of Algebra» (4th edition, 1931)*
            """
            ),
            mo.hstack([lang_toggle, problem_select], justify="start", align="center"),
            mo.md("---"),
        ]
    )
    header_view
    return (header_view,)


@app.cell
def __(is_uk, mo, problem_select, problems_data):
    chosen_id = problem_select.value
    cur_p = next((_p for _p in problems_data if _p["id"] == chosen_id), None) if chosen_id else None

    if not cur_p:
        card_content = mo.md(
            "*Оберіть задачу зі списку вище.*"
            if is_uk
            else "*Select a problem from the dropdown above.*"
        )
    else:
        _sec_title = cur_p["section_title_uk"] if is_uk else cur_p["section_title_en"]
        _stmt_text = cur_p["text_uk"] if is_uk else cur_p["text_en"]
        _orig_ru = cur_p.get("original_ru", "")

        # Clean problem card WITHOUT any spoiler drawings or answers
        card_content = mo.md(
            f"""
            ### 📌 {_sec_title}
            
            <div style="background: #ffffff; border-left: 5px solid #2563eb; padding: 18px 22px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin: 12px 0;">
                <div style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #2563eb; margin-bottom: 6px;">
                    {"УМОВА ЗАДАЧІ" if is_uk else "PROBLEM STATEMENT"}
                </div>
                <div style="font-size: 1.25rem; font-weight: 600; line-height: 1.6; color: #0f172a;">
                    {_stmt_text}
                </div>
                <div style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed #cbd5e1; font-size: 0.9rem; color: #64748b;">
                    📜 <b>{"Оригінал (рос. 1931 р.):" if is_uk else "Original text (Russian 1931):"}</b>
                    <span style="font-family: serif; color: #334155; font-style: italic;">«{_orig_ru}»</span>
                </div>
            </div>
            """
        )
    card_content
    return card_content, chosen_id, cur_p


@app.cell
def __(cur_p, is_uk, mo):
    # Form with explicit verify button to control evaluation
    if not cur_p:
        problem_form = None
    else:
        _sub_widgets = {
            str(_i): mo.ui.text(
                label=f"**{_sq['label_uk'] if is_uk else _sq['label_en']}**",
                placeholder="наприклад: 4a або 4*a" if is_uk else "e.g. 4a or 4*a",
            )
            for _i, _sq in enumerate(cur_p["sub_questions"])
        }
        problem_form = mo.ui.form(
            element=mo.ui.dictionary(_sub_widgets),
            submit_button_label="🔍 Перевірити розв'язок" if is_uk else "🔍 Check Solution",
            bordered=True,
        )
    return (problem_form,)


@app.cell
def __(check_answer_equivalence, cur_p, is_uk, mo, problem_form):
    # Live evaluation of form submission
    if cur_p is None or problem_form is None:
        form_and_eval_view = mo.md("")
    else:
        _lang_code = "uk" if is_uk else "en"
        _allowed_vars = cur_p.get("variables", None)

        if problem_form.value is None:
            _eval_badge = mo.callout(
                mo.md(
                    "✍️ **Введіть ваші формули у поля вище та натисніть кнопку 'Перевірити розв'язок'.**"
                    if is_uk
                    else "✍️ **Enter your formulas above and click 'Check Solution'.**"
                ),
                kind="neutral",
            )
            form_and_eval_view = mo.vstack(
                [
                    mo.md(f"#### ✍️ {'Ваша відповідь:' if is_uk else 'Your Solution:'}"),
                    problem_form,
                    _eval_badge,
                ]
            )
        else:
            _results = []
            _all_correct = True

            for _i, _sq in enumerate(cur_p["sub_questions"]):
                _user_val = problem_form.value.get(str(_i), "").strip()
                _lbl = _sq["label_uk"] if is_uk else _sq["label_en"]

                if not _user_val:
                    _all_correct = False
                    _results.append(
                        mo.callout(
                            mo.md(
                                f"⚠️ Поле **{_lbl}** порожнє. Будь ласка, введіть вираз!"
                                if is_uk
                                else f"⚠️ Field **{_lbl}** is empty. Please enter an expression!"
                            ),
                            kind="warn",
                        )
                    )
                else:
                    _is_ok, _feedback, _user_latex = check_answer_equivalence(
                        _user_val,
                        _sq["sympy_expr"],
                        variables=_allowed_vars,
                        lang=_lang_code,
                    )
                    if not _is_ok:
                        _all_correct = False

                    _callout_kind = "success" if _is_ok else "danger"
                    _status_title = "✅ ПРАВИЛЬНО!" if _is_ok else "❌ НЕПРАВИЛЬНО"
                    _status_text = (
                        f"### {_status_title}\n\n"
                        f"**{_lbl}**\n\n"
                        f"- **{'Ваш ввід' if is_uk else 'Your input'}**: `{_user_val}`\n"
                        f"- **{'Математичний вираз' if is_uk else 'Parsed as'}**: ${_user_latex}$\n\n"
                        f"*{_feedback}*"
                    )
                    _results.append(mo.callout(mo.md(_status_text), kind=_callout_kind))

            _summary_badge = (
                mo.callout(
                    mo.md(
                        "🎉 **ЧУДОВО! Задачу повністю розв'язано правильно!**"
                        if is_uk
                        else "🎉 **CONGRATULATIONS! The problem is completely solved correctly!**"
                    ),
                    kind="success",
                )
                if _all_correct
                else mo.callout(
                    mo.md(
                        "💡 **Відповідь поки не збігається.** Перевірте введені значення, скористайтеся підказками нижче та спробуйте ще раз!"
                        if is_uk
                        else "💡 **The solution is not equivalent yet.** Review your input, check the hints below, and try again!"
                    ),
                    kind="danger",
                )
            )

            form_and_eval_view = mo.vstack(
                [
                    mo.md(f"#### ✍️ {'Ваша відповідь:' if is_uk else 'Your Solution:'}"),
                    problem_form,
                    _summary_badge,
                    mo.vstack(_results, gap=0.5),
                ]
            )

    form_and_eval_view
    return (form_and_eval_view,)


@app.cell
def __(cur_p, is_uk, mo):
    # Socratic Progressive Hints (WITHOUT direct spoilers)
    if not cur_p:
        hints_view = mo.md("")
    else:
        _hints = cur_p["hints_uk"] if is_uk else cur_p["hints_en"]
        _hint_items = {
            f"💡 {'Рівень 1: Концептуальна ідея' if is_uk else 'Level 1: Core Concept'}": _hints[0]
            if len(_hints) > 0
            else "",
            f"🔍 {'Рівень 2: Напрямок дії' if is_uk else 'Level 2: Directional Step'}": _hints[1]
            if len(_hints) > 1
            else "",
            f"🎯 {'Рівень 3: Покроковий логічний розбір' if is_uk else 'Level 3: Step-by-Step Logic'}": _hints[
                2
            ]
            if len(_hints) > 2
            else "",
        }
        hints_view = mo.vstack(
            [
                mo.md(
                    f"#### 🧠 {'Потрібна допомога? Сократівські підказки:' if is_uk else 'Need guidance? Socratic hints:'}"
                ),
                mo.accordion(_hint_items),
            ]
        )
    hints_view
    return (hints_view,)


@app.cell
def __(Path, is_uk, mo):
    # Archive Scan Viewer (collapsed by default)
    scan_path = Path("data/raw_pages/page_005.png")
    if scan_path.exists():
        scan_card = mo.accordion(
            {
                f"📜 {'Переглянути оригінальний архівний скан підручника (Держвидав 1931 р.)' if is_uk else 'View original 1931 archive scan (State Publisher)'}": mo.image(
                    src=str(scan_path),
                    caption="Сторінка 5 (оригінальний номер 7) задачника А.П. Кисельова",
                    rounded=True,
                )
            }
        )
    else:
        scan_card = mo.md("")
    scan_card
    return (scan_card,)


if __name__ == "__main__":
    app.run()
