# twemoji_parser


## Examples
### Drawing a text with emoji:
```py
from twemoji_parser import TwemojiParser
from PIL import Image, ImageFont

im = Image.new("RGB", (500, 500), color=(255, 255, 255))
font = ImageFont.truetype("/path/to/font.ttf", 30)
parser = TwemojiParser(im)

parser.draw_text((5, 5), "I 💖 Python!", font=font, fill=(0, 0, 0))
im.show()
```
### Get a twemoji URL from emoji:
```py
from twemoji_parser import emoji_to_url
from requests import get
url = emoji_to_url("❤️")

with open("emoji.png", "wb") as im:
    response = get(url).content
    im.write(response)
    im.close()
```