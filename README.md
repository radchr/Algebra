# Інтерактивна геометрія Кисельова — 7 клас

Приватний україномовний цифровий курс планіметрії для індивідуального навчання. Поточний продукт — жива книга у [Marimo](https://marimo.io/), побудована на адаптованому тексті Кисельова, точній перевірці SymPy та векторних кресленнях DrawSVG.

## Поточний стан

Реалізовано три наскрізні уроки:

1. §§ 1–12 — найпростіші геометричні фігури;
2. §§ 13–26 — кути, суміжні та вертикальні кути;
3. §§ 30–38 — трикутники й ознаки їхньої рівності.

Кожен урок проходить цикл POEM:

- **Прогноз** — учень фіксує гіпотезу;
- **Дослід** — після прогнозу відкривається DrawSVG або JSXGraph;
- **Пояснення** — повний текст, інтуїція Фейнмана та пастки мислення;
- **Місія** — задача з точною перевіркою SymPy і трьома рівнями підказок.

## Архітектура

```text
content/geometry/*.md
        │
        ▼
src/geometry_engine/lesson.py
        │
        ├── data/geometry/book_kb.db ── перевірені сторінки та готові SVG
        ├── svg_drawings.py           ── реактивні DrawSVG-креслення
        ├── jsx_templates.py          ── тактильні моделі JSXGraph
        └── sympy_solver.py           ── точна перевірка відповідей
        │
        ▼
app_geometry.py
```

Урок завантажується лише тоді, коли всі сторінки, зазначені в його мітці `source-pages`, присутні в SQLite та мають статус `verified`. Це виконує правило «спочатку повний кеш — потім компонування».

## Локальний запуск

```powershell
uv sync
uv run marimo run app_geometry.py
```

Відкрити редактор Marimo:

```powershell
uv run marimo edit app_geometry.py
```

## Перевірка

Активний набір тестів не запускає заморожені PDF, GitHub Pages або старий LaTeX pipeline:

```powershell
uv run pytest tests/test_geometry_engine.py tests/test_lessons_and_app.py
uv run ruff check app_geometry.py src/geometry_engine tests/test_geometry_engine.py tests/test_lessons_and_app.py
uv run ruff format --check app_geometry.py src/geometry_engine tests/test_geometry_engine.py tests/test_lessons_and_app.py
```

## Робота з контентом

1. Завершити OCR, український переклад, педагогічні поля й SVG у `book_kb.db`.
2. Позначити перевірені сторінки статусом `verified`.
3. Додати або змінити Markdown-урок у `content/geometry/`.
4. Вказати точний діапазон, наприклад `<!-- source-pages: 21-28 -->`.
5. Запустити активні тести — вони перевірять статус сторінок, рисунки, структуру уроку та Marimo smoke test.

Для відтворюваного завершення перевірених сторінок активного блоку використовується:

```powershell
uv run python scripts/verify_active_geometry_cache.py
```

## Мережева межа

Текст уроків, SQLite-кеш, DrawSVG-рисунки й SymPy-місії працюють локально. Два тактильні віджети JSXGraph зараз завантажують бібліотеку з `cdn.jsdelivr.net`, тому для них потрібне з’єднання з інтернетом. Якщо CDN недоступний, застосунок показує повідомлення, а решта уроку продовжує працювати.

## Межі активної розробки

У роботі лише `app_geometry.py`, `content/geometry/`, `src/geometry_engine/` і `data/geometry/book_kb.db`. Алгебра, статичний сайт, PDF/XeLaTeX/TikZ та старий `geometry_pipeline` залишаються замороженими.
