"""Generate stable QR assets for the standalone geometry motion pages."""

from pathlib import Path

import qrcode

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "book_geometry"

PAGES = {
    "qr_angle_rotation.png": "https://radchr.github.io/Algebra/geometry-angle-rotation.html",
    "qr_central_angle_arc.png": "https://radchr.github.io/Algebra/geometry-central-angle-arc.html",
    "qr_adjacent_angles.png": "https://radchr.github.io/Algebra/geometry-adjacent-angles.html",
    "qr_vertical_half_turn.png": "https://radchr.github.io/Algebra/geometry-vertical-half-turn.html",
    "qr_adjacent_bisectors.png": "https://radchr.github.io/Algebra/geometry-adjacent-bisectors.html",
    "qr_vertical_bisectors.png": "https://radchr.github.io/Algebra/geometry-vertical-bisectors.html",
}


def main() -> None:
    for filename, url in PAGES.items():
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        image = qr.make_image(fill_color="#172033", back_color="white")
        image.save(OUTPUT_DIR / filename)
        print(f"generated {filename}: {url}")


if __name__ == "__main__":
    main()
