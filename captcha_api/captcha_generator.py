import os
from io import BytesIO
from random import randint, choice
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps


def _get_random_color():
    #  random color rgb
    return randint(120, 200), randint(120, 200), randint(120, 200)


def _get_random_code():
    #  random characters
    codes = [
        [chr(i) for i in range(49, 58)],
        [chr(i) for i in range(65, 91)],
        [chr(i) for i in range(97, 123)],
    ]
    codes = codes[randint(0, 2)]
    return codes[randint(0, len(codes) - 1)]


def _generate_rotated_char(c, font):
    txt = Image.new("L", font.getsize(c))
    blank_image = ImageDraw.Draw(txt)
    blank_image.text((0, 0), c, font=font, fill=255)
    rotated_text = txt.rotate(randint(-35, 35), expand=1)
    return rotated_text


class CaptchaGenerator:
    """
    Generates captcha images based on the parameters
    """

    def __init__(self, fonts_dir="captcha_api/fonts", width=250, height=60):
        self.width = width
        self.height = height
        self.font = self._get_random_font(fonts_dir)

    def _get_random_font(self, fonts_dir):
        font_files = [f for f in os.listdir(fonts_dir) if f.endswith(('.otf', '.ttf'))]
        if not font_files:
            raise ValueError("No .otf or .ttf fonts found in the specified directory.")
        random_font_file = choice(font_files)
        return ImageFont.truetype(os.path.join(fonts_dir, random_font_file), size=40)

    def generate_captcha(self, length=6) -> Tuple[BytesIO, str]:
        """
        Generate a captcha image
        :return: A tuple consisting of the image bytes and the text
        """
        img = Image.new("RGB", (self.width, self.height), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        #  captcha text
        text = ""
        for i in range(length):
            char = _get_random_code()
            text += char

            rotated = _generate_rotated_char(char, self.font)
            colorized = ImageOps.colorize(rotated, (0, 0, 0), _get_random_color())
            img.paste(
                colorized,
                (int(self.width * 0.13 * (i + 1)), int(self.height * 0.2)),
                rotated,
            )
        #  add interference line
        for i in range(15):
            x_1 = randint(0, self.width)
            y_1 = randint(0, self.height)
            x_2 = randint(0, self.width)
            y_2 = randint(0, self.height)
            draw.line((x_1, y_1, x_2, y_2), fill=_get_random_color())
        #  add interference point
        for i in range(16):
            draw.point(
                (randint(0, self.width), randint(0, self.height)),
                fill=_get_random_color(),
            )
        #  save the picture
        img_byte_array = BytesIO()
        img.save(img_byte_array, format="jpeg")
        return img_byte_array, text
