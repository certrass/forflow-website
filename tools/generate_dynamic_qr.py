#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".python-deps"))

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderSVG
from reportlab.graphics.shapes import Drawing
from PIL import Image


def normalize_base_url(value):
    base_url = value.strip().rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        raise SystemExit("--base-url must start with http:// or https://")
    return base_url


def qr_matrix(value):
    widget = QrCodeWidget(value)
    encoder = widget.qr
    encoder.make()
    return encoder.modules


def save_svg(value, destination, pixel_size):
    widget = QrCodeWidget(value)
    left, bottom, right, top = widget.getBounds()
    width = right - left
    height = top - bottom
    drawing = Drawing(
        pixel_size,
        pixel_size,
        transform=[pixel_size / width, 0, 0, pixel_size / height, 0, 0],
    )
    drawing.add(widget)
    renderSVG.drawToFile(drawing, str(destination))


def save_png(value, destination, pixel_size, quiet_zone):
    modules = qr_matrix(value)
    module_count = len(modules)
    cells = module_count + quiet_zone * 2
    cell_size = max(1, pixel_size // cells)
    image_size = cell_size * cells
    image = Image.new("RGB", (image_size, image_size), "white")
    pixels = image.load()

    for row, line in enumerate(modules):
        for col, dark in enumerate(line):
            if not dark:
                continue
            start_x = (col + quiet_zone) * cell_size
            start_y = (row + quiet_zone) * cell_size
            for y in range(start_y, start_y + cell_size):
                for x in range(start_x, start_x + cell_size):
                    pixels[x, y] = (0, 0, 0)

    image.save(destination)


def main():
    parser = argparse.ArgumentParser(description="Generate the printed QR image for a dynamic QR slug.")
    parser.add_argument("--base-url", required=True, help="Public site origin, for example https://www.example.com")
    parser.add_argument("--code", default="forflow", help="Dynamic QR slug configured in netlify/functions/qr-routes.json")
    parser.add_argument("--output-dir", default="assets/qr", help="Directory for generated image files")
    parser.add_argument("--size", type=int, default=1024, help="Output image size in pixels")
    parser.add_argument("--quiet-zone", type=int, default=4, help="White modules around the PNG QR code")
    args = parser.parse_args()

    base_url = normalize_base_url(args.base_url)
    code = args.code.strip().lower()
    if not code:
        raise SystemExit("--code cannot be empty")

    qr_url = f"{base_url}/q/{code}"
    output_dir = (ROOT / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    svg_path = output_dir / f"{code}.svg"
    png_path = output_dir / f"{code}.png"
    url_path = output_dir / f"{code}.url.txt"

    save_svg(qr_url, svg_path, args.size)
    save_png(qr_url, png_path, args.size, args.quiet_zone)
    url_path.write_text(qr_url + "\n", encoding="utf-8")

    print(f"QR URL: {qr_url}")
    print(f"SVG: {svg_path}")
    print(f"PNG: {png_path}")
    print(f"URL: {url_path}")


if __name__ == "__main__":
    main()
