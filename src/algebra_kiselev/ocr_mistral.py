"""
Mistral OCR extractor for Kiselev Algebra problems.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()


def run_mistral_ocr(pdf_path: str, pages: list[int], output_dir: str = "data/ocr_mistral") -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set in environment or .env file.")

    client = Mistral(api_key=api_key)
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"Uploading '{pdf_file.name}' to Mistral Files API...")
    with open(pdf_file, "rb") as f:
        uploaded_file = client.files.upload(
            file={"file_name": pdf_file.name, "content": f}, purpose="ocr"
        )

    file_id = uploaded_file.id
    print(f"File uploaded successfully! File ID: {file_id}")

    print(f"Processing OCR with model 'mistral-ocr-latest' for pages {pages}...")
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "file", "file_id": file_id},
        pages=pages,
        include_image_base64=False,
    )

    combined_markdown = []
    for page in ocr_response.pages:
        page_num = page.index + 1
        page_md = page.markdown
        combined_markdown.append(f"<!-- Page {page_num} -->\n{page_md}\n")

        # Save individual page
        page_file = out_path / f"page_{page_num:03d}.md"
        with open(page_file, "w", encoding="utf-8") as pf:
            pf.write(page_md)
        print(f"Saved OCR markdown for Page {page_num} to {page_file}")

    full_text = "\n\n".join(combined_markdown)
    summary_file = out_path / f"pages_{'_'.join(map(str, pages))}.md"
    with open(summary_file, "w", encoding="utf-8") as sf:
        sf.write(full_text)

    print(f"OCR Complete! Full result saved to: {summary_file}")
    return full_text


if __name__ == "__main__":
    # Default: test page 4 (page 5 of book, §§ 1-5, problems 1-17)
    target_pages = [4]
    pdf = "Zadachi i upr. k eliemientam al - Nievidomii.pdf"

    print(f"Starting Mistral OCR Test on {pdf}, pages={target_pages}...")
    result = run_mistral_ocr(pdf, target_pages)
    print("\n" + "=" * 40 + " EXTRACTED MARKDOWN " + "=" * 40 + "\n")
    print(result)
