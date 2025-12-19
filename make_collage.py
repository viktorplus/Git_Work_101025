import argparse
import os
import re
from typing import Iterable

from PIL import Image


PNG_OPTIMIZE_DEFAULT = True
PNG_COMPRESS_LEVEL_DEFAULT = 9
COLLAGE_BG = (255, 255, 255)
COLLAGE_MARGIN_PX = 0


PAGE_PREFIX_RE = re.compile(r"^(\d+)_")
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_\-]+")


def list_pngs_with_page(root: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for name in os.listdir(root):
        if not name.lower().endswith(".png"):
            continue
        match = PAGE_PREFIX_RE.match(name)
        if not match:
            continue
        page_number = int(match.group(1))
        result.append((page_number, os.path.join(root, name)))
    return sorted(result, key=lambda item: item[0])


def stitch_vertical(images: Iterable[Image.Image]) -> Image.Image:
    image_list = list(images)
    if not image_list:
        raise ValueError("No images to stitch")

    max_width = max(image.width for image in image_list)
    total_height = sum(image.height for image in image_list) + COLLAGE_MARGIN_PX * (
        len(image_list) - 1
    )
    background_color = tuple(COLLAGE_BG)
    result = Image.new("RGB", (max_width, total_height), background_color)

    offset_y = 0
    for image in image_list:
        result.paste(image, (0, offset_y))
        offset_y += image.height + COLLAGE_MARGIN_PX
    return result


def stitch_horizontal(images: Iterable[Image.Image]) -> Image.Image:
    image_list = list(images)
    if not image_list:
        raise ValueError("No images to stitch")

    max_height = max(image.height for image in image_list)
    total_width = sum(image.width for image in image_list) + COLLAGE_MARGIN_PX * (
        len(image_list) - 1
    )
    background_color = tuple(COLLAGE_BG)
    result = Image.new("RGB", (total_width, max_height), background_color)

    offset_x = 0
    for image in image_list:
        result.paste(image, (offset_x, 0))
        offset_x += image.width + COLLAGE_MARGIN_PX
    return result


def build_collage_from_images(
    images: Iterable[Image.Image],
    direction: str,
) -> Image.Image:
    if direction == "horizontal":
        return stitch_horizontal(images)
    return stitch_vertical(images)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Склеивает все PNG-скриншоты в папке, где лежит этот скрипт, "
            "в один коллаж по вертикали или горизонтали."
        )
    )
    parser.add_argument(
        "-d",
        "--direction",
        choices=["vertical", "horizontal"],
        default="vertical",
        help="Направление коллажа: vertical или horizontal (по умолчанию vertical).",
    )
    parser.add_argument(
        "-l",
        "--label",
        default="ALL",
        help="Метка для имени файла коллажа (по умолчанию ALL).",
    )
    parser.add_argument(
        "--keep-112",
        action="store_true",
        help="Не исключать страницу 112 из коллажа с меткой ALL.",
    )
    args = parser.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))

    all_images = list_pngs_with_page(root)
    if not all_images:
        print("PNG-скриншоты в папке не найдены.")
        return

    chosen_images = all_images
    if (args.label or "").upper() == "ALL" and not args.keep_112:
        chosen_images = [(page, path) for (page, path) in chosen_images if page != 112]
        if not chosen_images:
            print("После исключения страницы 112 не осталось страниц для коллажа.")
            return

    loaded_images: list[Image.Image] = []
    for _, path in chosen_images:
        with Image.open(path) as image:
            loaded_images.append(image.convert("RGB"))

    try:
        result = build_collage_from_images(loaded_images, args.direction)
    finally:
        for image in loaded_images:
            try:
                image.close()
            except Exception:
                pass

    safe_label = SAFE_NAME_RE.sub("_", (args.label or "").strip()) or "ALL"
    output_path = os.path.join(root, f"collage_{safe_label}.png")

    save_kwargs: dict = {}
    if PNG_OPTIMIZE_DEFAULT:
        save_kwargs["optimize"] = True
    if isinstance(PNG_COMPRESS_LEVEL_DEFAULT, int):
        save_kwargs["compress_level"] = max(0, min(9, PNG_COMPRESS_LEVEL_DEFAULT))

    try:
        result.save(output_path, **save_kwargs)
    except TypeError:
        save_kwargs.pop("compress_level", None)
        result.save(output_path, **save_kwargs)

    print(f"Коллаж создан: {output_path}")


if __name__ == "__main__":
    main()

