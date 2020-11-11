"""
A python module made on top of PIL that draws emoji from text to image.
Example:

from twemoji_parser import TwemojiParser
from PIL import Image, ImageFont

im = Image.new("RGB", (500, 500), color=(255, 255, 255))
font = ImageFont.truetype("/path/to/font.ttf", 30)
parser = TwemojiParser(im)

parser.draw_text((5, 5), "I 💖 Python!", font=font, fill=(0, 0, 0))
im.show()

"""

from .emote import emoji_to_url
from .image import TwemojiParser

__version__ = "0.2"
__all__ = ["emoji_to_url", "TwemojiParser"]