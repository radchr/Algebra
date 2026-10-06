"""Refine and update pages in SQLite Knowledge Base (data/geometry/book_kb.db)

Reads pre-rendered high-res PNG images from Kiselev-geom/,
generates meticulous NUSH Ukrainian translation, Feynman intuition notes,
misconceptions, and saves directly to SQLite.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from geometry_engine.db import BookDatabase, BookPage  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

BOOK_ID = "kiselev_geometry_1931"
IMAGES_DIR = Path("Kiselev-geom")
DB_PATH = Path("data/geometry/book_kb.db")
BACKUP_PATH = Path("data/geometry/book_kb.db.bak")

GLOSSARY_RULES = """
Суворі правила української термінології за стандартом НУШ (підручник Мерзляка):
- "чертеж" -> "рисунок (рис.)" або "креслення"
- "признаки равенства треугольников" -> "ознаки рівності трикутників"
- "равенство" -> "рівність"
- "прилежащий угол" -> "прилеглий кут" (УВАГА: не "прилога", а "прилегла сторона" / "прилеглий кут")
- "противолежащий угол" -> "протилежний кут"
- "полупрямая" -> "промінь"
- "отрезок" -> "відрізок"
- "наклонная" -> "похила", "основание наклонной" -> "основа похилої"
- "способ наложения" -> "спосіб накладання", "совместить" -> "сумістити"
- "секущая" -> "січна"
- "внутренние накрест лежащие" -> "внутрішні різносторонні кути"
- "соответственные" -> "відповідні кути"
- "внутренние односторонние" -> "внутрішні односторонні кути"
- "окружность" -> "коло", "круг" -> "круг"
- "геометрическое место точек (ГМТ)" -> "геометричне місце точок (ГМТ)"
- "задачи на построение" -> "задачі на побудову"
- Математичні формули, назви точок та кутів оформлюй строго у KaTeX ($...$ та $$...$$).
- ЖОДНИХ вставних мета-фраз на кшталт "У цьому курсі...", "Оригінал містить...", "Учитель підготував...". Текст має читатися як чистий, академічний, зрозумілий підручник для дитини 7 класу.
"""


def backup_database():
    if DB_PATH.exists() and not BACKUP_PATH.exists():
        shutil.copyfile(DB_PATH, BACKUP_PATH)
        print(f"📦 Created backup: {BACKUP_PATH}")


def process_page(client, page_num: int, pdf_page: int, max_retries: int = 3) -> dict:
    image_file = IMAGES_DIR / f"Kisieliev A.P. - Eliemientarnai - 1931_{pdf_page}.png"
    if not image_file.exists():
        raise FileNotFoundError(f"Image not found: {image_file}")

    image_bytes = image_file.read_bytes()
    sha256 = hashlib.sha256(image_bytes).hexdigest()

    prompt = f"""Ти — провідний методист з математики та автор сучасних підручників геометрії 7 класу за програмою НУШ.
Перед тобою скан друкованої сторінки {page_num} класичного підручника А. П. Кисельова «Елементарна геометрія» (1931 р.).

{GLOSSARY_RULES}

Завдання:
1. 'sections_covered': Номери та точні назви параграфів/пунктів/задач на цій сторінці.
2. 'translation_uk': Повний, детальний, високоякісний навчальний текст українською мовою. Переклади ВСІ означення, теореми, їхні доведення, примітки, кроки побудови та вправи. Не скорочуй жодної логічної думки автора!
3. 'feynman_notes': Коротка інтуїтивна фізична модель чи яскрава аналогія у стилі Річарда Фейнмана для дитини (1-2 абзаци).
4. 'misconceptions': Аналіз типової учнівської помилки чи пастки мислення до матеріалу цієї сторінки (1 абзац).
5. 'figures': Номери рисунків на сторінці (наприклад: ["рис. 41", "рис. 42"]).

Поверни результат строго у форматі JSON з такими ключами:
{{
  "sections_covered": "...",
  "translation_uk": "...",
  "feynman_notes": "...",
  "misconceptions": "...",
  "figures": [...]
}}
"""

    models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.7-flash"]
    attempt = 0

    while attempt < max_retries:
        model = models[attempt % len(models)]
        try:
            resp = client.models.generate_content(
                model=model,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            raw = (resp.text or "").strip()
            if raw.startswith("```json"):
                raw = raw[7:]
            if raw.startswith("```"):
                raw = raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            data = json.loads(raw.strip())
            data["sha256"] = sha256
            return data
        except Exception as e:
            wait_time = (attempt + 1) * 6
            print(f"⚠️ Error on page {page_num} with {model}: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            attempt += 1

    raise RuntimeError(f"Failed to process page {page_num} after {max_retries} attempts.")


def main():
    parser = argparse.ArgumentParser(description="Refine specific pages in book_kb.db.")
    parser.add_argument(
        "--pages", type=int, nargs="+", help="Specific page numbers (e.g. --pages 25 38 48)"
    )
    parser.add_argument("--start", type=int, help="Start page range")
    parser.add_argument("--end", type=int, help="End page range")
    parser.add_argument(
        "--delay", type=float, default=5.0, help="Delay between requests in seconds"
    )
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    backup_database()
    db = BookDatabase()

    if args.pages:
        target_pages = args.pages
    elif args.start and args.end:
        target_pages = list(range(args.start, args.end + 1))
    else:
        print("Please specify either --pages or --start/--end.")
        sys.exit(1)

    print("==================================================")
    print(f"🎯 Refining {len(target_pages)} pages: {target_pages}")
    print("==================================================")

    for i, p in enumerate(target_pages):
        pdf_page = p + 1
        print(f"\n[{i + 1}/{len(target_pages)}] 📄 Processing page {p} (image: {pdf_page})...")
        try:
            res = process_page(client, p, pdf_page)

            # Fetch existing ocr_ru if present
            existing = db.get_page(BOOK_ID, p)
            ocr_ru = existing.ocr_ru if existing and existing.ocr_ru else f"Кісельов 1931, с. {p}"

            page = BookPage(
                book_id=BOOK_ID,
                page_num=p,
                pdf_page=pdf_page,
                sections_covered=res.get("sections_covered", ""),
                ocr_ru=ocr_ru,
                translation_uk=res.get("translation_uk", ""),
                feynman_notes=res.get("feynman_notes", ""),
                misconceptions=res.get("misconceptions", ""),
                figures_json=json.dumps(res.get("figures", []), ensure_ascii=False),
                status="verified",
                sha256=res.get("sha256", ""),
            )
            db.save_page(page)
            print(
                f"✅ Saved page {p} to DB: {len(page.translation_uk)} chars | Sections: {page.sections_covered[:60]}"
            )
        except Exception as err:
            print(f"❌ Failed to process page {p}: {err}")

        if i < len(target_pages) - 1:
            time.sleep(args.delay)

    print("\n🎉 Completed refinement!")


if __name__ == "__main__":
    main()
