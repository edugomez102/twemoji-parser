# twemoji_parser
A python module made on top of PIL that draws twemoji from text to image.<br>
```sh
$ python3 -m pip install twemoji-parser
```

## Examples
### Drawing a text with emoji:
```py
from twemoji_parser import TwemojiParser
from PIL import Image, ImageFont

async def main():
	im = Image.new("RGB", (500, 500), color=(255, 255, 255))
	font = ImageFont.truetype("/path/to/font.ttf", 30)
	parser = TwemojiParser(im)
	
	await parser.draw_text((5, 5), "I 💖 Python!", font=font, fill=(0, 0, 0))
	im.show()
```
### Get a twemoji URL from emoji:
```py
from twemoji_parser import emoji_to_url
url = emoji_to_url("❤️")

# returns a URL that displays an image of the emoji. otherwise returns the same text.
```