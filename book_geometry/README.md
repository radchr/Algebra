# Книга «Елементарна геометрія»

Основний продукт проєкту — PDF-книга, яку збирає `main.tex`.

## Поточна композиція

- `generated/sections/00_introduction.tex` — згенеровані §§ 1–12, друковані сторінки 9–12;
- `sections/section_01_angles.tex` — редакторський еталон розділу «Кути»;
- `figures/` — окремі TikZ-джерела рисунків 1–27;
- `review_generated.tex` — автономна збірка всіх 33 структурованих блоків;
- `build/main.pdf` — основна книга;
- `build/generated_review/review_generated.pdf` — PDF для порівняння з генератором.

## Відтворення змісту

```powershell
uv run python -m geometry_pipeline.migrate_figures
uv run python -m geometry_pipeline.migrate_pilot
uv run geometry-pipeline validate-content
uv run geometry-pipeline build-manifest
uv run geometry-pipeline render-latex
uv run pytest -q
```

Після цього `main.tex` і `review_generated.tex` компілюються XeLaTeX у два проходи.
Не редагуйте файли в `generated/` вручну: зміни слід вносити у структуровані блоки,
міграцію або фінальні Markdown-джерела.
