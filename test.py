from twemoji_parser import TwemojiParser
from PIL import Image, ImageFont

font = ImageFont.truetype("consola.ttf", 30)
image = Image.new("RGB", (500, 500), color=(255, 255, 255))
parser = TwemojiParser(image)

parser.draw_text((5, 5), "Hello, H\nHiorld!xixi\nxyou are gay m8", font=font, fill=(0, 0, 0))
image.show()