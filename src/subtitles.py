import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class SubtitleRenderer:

    def __init__(
        self,
        width: int,
        height: int,
    ):
        self.width = width
        self.height = height

    def load_timings(
        self,
        path: Path,
    ) -> list[dict]:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def get_current_word(
        self,
        timings: list[dict],
        current_time: float,
    ):

        for item in timings:

            if (
                item["start"]
                <= current_time
                <= item["end"]
            ):
                return item

        return None

    def get_font(
        self,
        size: int,
    ):

        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]

        for font_path in possible_fonts:

            path = Path(font_path)

            if path.exists():
                return ImageFont.truetype(
                    str(path),
                    size
                )

        return ImageFont.load_default()

    def draw(
        self,
        frame: Image.Image,
        timings: list[dict],
        current_time: float,
    ) -> Image.Image:

        current = self.get_current_word(
            timings,
            current_time,
        )

        if current is None:
            return frame

        word = current["word"].strip()

        if not word:
            return frame

        word = word.upper()

        draw = ImageDraw.Draw(
            frame,
            "RGBA"
        )

        font_size = 76

        # Small pop animation when a word appears.
        elapsed = (
            current_time
            - current["start"]
        )

        scale = 1.0

        if 0 <= elapsed < 0.10:

            progress = elapsed / 0.10

            scale = (
                1.10
                - (0.10 * progress)
            )

        font = self.get_font(
            int(font_size * scale)
        )

        center_x = self.width // 2
        center_y = self.height // 2

        bbox = draw.textbbox(
            (
                center_x,
                center_y,
            ),
            word,
            font=font,
            anchor="mm",
            stroke_width=2,
        )

        padding_x = 26
        padding_y = 18

        draw.rounded_rectangle(
            (
                bbox[0] - padding_x,
                bbox[1] - padding_y,
                bbox[2] + padding_x,
                bbox[3] + padding_y,
            ),
            radius=18,
            fill=(255, 255, 255, 235),
        )

        draw.text(
            (
                center_x,
                center_y,
            ),
            word,
            font=font,
            anchor="mm",
            fill=(0, 0, 0, 255),
            stroke_width=1,
            stroke_fill=(0, 0, 0, 255),
        )

        return frame