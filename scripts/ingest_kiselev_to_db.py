"""Safe, paced batch ingestion script for Kiselev's Geometry (1931).

Converts book pages from Kiselev-geom PNG images to OCR + NUSH Ukrainian translation
and saves them directly into SQLite (data/geometry/book_kb.db).
Respects Gemini API Free Tier rate limits (15 RPM -> 4.5s delay per page, retries on 429).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from geometry_engine.db import BookDatabase, BookPage

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

IMAGES_DIR = Path("Kiselev-geom")
PDF_PATH = Path("Kisieliev A.P. - Eliemientarnai - 1931.pdf")
BOOK_ID = "kiselev_geometry_1931"

GLOSSARY_PROMPT = """
Суворі правила заміни застарілих термінів на сучасні стандарти НУШ (підручник Мерзляка):
- "чертеж" -> "креслення" або "рисунок (рис.)"
- "признаки равенства треугольников" -> "ознаки рівності трикутників"
- "равенство" -> "рівність"
- "прилежащий угол" -> "прилеглий кут"
- "противолежащий угол" -> "протилежний кут"
- "полупрямая" -> "промінь"
- "отрезок" -> "відрізок"
- "наклонная" -> "похила"
- "перпендикуляр" -> "перпендикуляр"
- "основание перпендикуляра / наклонной" -> "основа перпендикуляра / похилої"
- "равнобедренный треугольник" -> "рівнобедрений трикутник"
- "равносторонний" -> "рівносторонній"
- "разносторонний" -> "різносторонній"
- "боковые стороны" -> "бічні сторони"
- "основание треугольника" -> "основа трикутника"
- "медиана, биссектриса, высота" -> "медіана, бісектриса, висота"
- "способ наложения" -> "спосіб накладання"
- "совместить" -> "сумістити"
- "совпадение" -> "збіг"
- "секущая" -> "січна"
- "внутренние накрест лежащие" -> "внутрішні різносторонні кути"
- "соответственные" -> "відповідні кути"
- "внутренние односторонние" -> "внутрішні односторонні кути"
- "окружность" -> "коло"
- "круг" -> "круг"
- "хорда, радиус, диаметр" -> "хорда, радіус, діаметр"
- "касательная" -> "дотична"
- "геометрическое место точек (ГМТ)" -> "геометричне місце точок (ГМТ)"
- "задачи на построение" -> "задачі на побудову"
- Всі формули, назви точок та теореми записуй виключно у чистому KaTeX ($...$ та $$...$$).
"""


def load_page_image_bytes(pdf_idx: int) -> bytes:
    """Loads page PNG bytes from Kiselev-geom or fallback to PDF."""
    png_path = IMAGES_DIR / f"Kisieliev A.P. - Eliemientarnai - 1931_{pdf_idx}.png"
    if png_path.exists():
        return png_path.read_bytes()

    if PDF_PATH.exists():
        import pypdfium2 as pdfium

        doc = pdfium.PdfDocument(str(PDF_PATH))
        page = doc[pdf_idx]
        bitmap = page.render(scale=200 / 72.0)
        pil_image = bitmap.to_pil()
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        return buf.getvalue()

    raise FileNotFoundError(f"Neither {png_path} nor {PDF_PATH} could be found.")


def process_single_page_with_retry(
    client, image_bytes: bytes, page_num: int, pdf_page: int, max_retries: int = 4
) -> dict:
    """Calls Gemini to perform OCR + NUSH adaptation with retry on 429."""
    from google.genai import types

    prompt = f"""
Ти — провідний експерт з математичної освіти та української мови (стандарт НУШ, підручник Мерзляка).
Перед тобою скан сторінки {page_num} класичного підручника А. П. Кисельова «Елементарна геометрія».

{GLOSSARY_PROMPT}

Зроби повну якісну адаптацію навчального матеріалу цієї сторінки для сучасного українського цифрового курсу:
1. Визнач номери та назви параграфів, номери рисунків.
2. Подай адаптований український текст параграфів сучасною термінологією НУШ, зберігши всю математичну строгість формулювань, доведень, формул (у KaTeX $...$) та структуру.
3. Коротко або за тезами зазнач зміст оригіналу (російська 1931 р.) для збереження контексту.

Поверни результат ТІЛЬКИ у форматі JSON з такими полями:
{{
  "sections_covered": "наприклад, § 27. Трикутник та його елементи",
  "ocr_ru": "короткий або тезовий виклад змісту оригіналу...",
  "translation_uk": "повний детальний адаптований текст українською мовою НУШ...",
  "figures": ["рис. 14", "рис. 15"]
}}
"""

    attempt = 0
    models_to_try = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]
    model_name = models_to_try[0]

    while attempt < max_retries:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                    prompt,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            raw_text = response.text or ""
            if not raw_text and response.candidates and response.candidates[0].content:
                parts = response.candidates[0].content.parts
                if parts and hasattr(parts[0], "text"):
                    raw_text = parts[0].text or ""
            raw_text = raw_text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            return json.loads(raw_text.strip())
        except Exception as e:
            err_str = str(e)
            wait_time = (attempt + 1) * 6
            print(
                f"⚠️ Retryable error on page {page_num}: {err_str[:80]}... Backing off {wait_time}s (attempt {attempt + 1}/{max_retries})..."
            )
            time.sleep(wait_time)
            model_name = models_to_try[(attempt + 1) % len(models_to_try)]
            attempt += 1

    raise RuntimeError(f"Failed to process page {page_num} after {max_retries} attempts.")


def main():
    parser = argparse.ArgumentParser(
        description="Paced batch ingestion of Kiselev Geometry into SQLite DB."
    )
    parser.add_argument(
        "--start", type=int, default=21, help="Start printed page number (default 21)"
    )
    parser.add_argument("--end", type=int, default=30, help="End printed page number (default 30)")
    parser.add_argument(
        "--page-offset",
        type=int,
        default=1,
        help="PDF page index = printed_page + offset (default 1)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=4.5,
        help="Delay in seconds between requests (default 4.5s for 13 RPM)",
    )
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(
            "ERROR: GEMINI_API_KEY environment variable is not set. Please add it to your .env file."
        )
        sys.exit(1)

    from google import genai

    client = genai.Client(api_key=api_key)

    db = BookDatabase()

    print("==================================================")
    print("📖 Kiselev Book Ingestion -> SQLite Knowledge Base")
    print(f"Target pages: {args.start} to {args.end}")
    print(f"Image source: {IMAGES_DIR}")
    print(f"Rate-limit delay: {args.delay}s (Safe for 15 RPM free tier)")
    print("==================================================")

    processed_count = 0
    skipped_count = 0

    for page_num in range(args.start, args.end + 1):
        if db.has_page(BOOK_ID, page_num):
            print(f"⚡ Page {page_num} already in DB. Skipping.")
            skipped_count += 1
            continue

        pdf_idx = page_num + args.page_offset
        print(f"\n🔍 Processing page {page_num} (Image index {pdf_idx})...")
        try:
            img_bytes = load_page_image_bytes(pdf_idx)

            # API call with retry
            res = process_single_page_with_retry(client, img_bytes, page_num, pdf_idx)

            bp = BookPage(
                book_id=BOOK_ID,
                page_num=page_num,
                pdf_page=pdf_idx,
                sections_covered=res.get("sections_covered", ""),
                ocr_ru=res.get("ocr_ru", ""),
                translation_uk=res.get("translation_uk", ""),
                figures_json=json.dumps(res.get("figures", []), ensure_ascii=False),
                status="translated",
            )
            db.save_page(bp)
            processed_count += 1
            print(f"✅ Saved page {page_num} ({bp.sections_covered}) to SQLite!")

        except Exception as e:
            print(f"❌ Error processing page {page_num}: {e}")

        # Rate-limiting pause
        time.sleep(args.delay)

    print("\n==================================================")
    print("🎉 Batch Ingestion Completed!")
    print(f"Processed: {processed_count} pages | Skipped (already in DB): {skipped_count} pages")
    print(f"Total verified pages now in DB: {db.count_pages(BOOK_ID)}")
    print("==================================================")


if __name__ == "__main__":
    main()
