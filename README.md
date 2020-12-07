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
    await parser.close() # this is optional. don't close the parser when you are not finished.
    im.show()

main()
```
### Get a twemoji URL from emoji:
```py
from twemoji_parser import emoji_to_url
from aiohttp import ClientSession

async def main():
    url = await emoji_to_url("❤️")
	# returns a URL that displays an image of the emoji. otherwise returns the same text.
    print(url)

main()
```

## Documentation

***`TwemojiPaser(image: PIL.Image.image, session: aiohttp.ClientSession, ...) -> None`***<br>
**image** (PIL image object)<br>
**session** (optional, aiohttp client session object, defaults to `None`)<br>

***`(async) TwemojiParser.draw_text(xy: tuple, text: str, font: PIL.ImageFont, spacing: int, with_url_check: bool, clear_cache_after_usage: bool) -> None`***<br>
**xy** (X and y coordinates to put the text on.)<br>
**text** (the text content.)<br>
**font** (optional, `PIL.ImageFont` object.)<br>
**spacing** (optional, spacing of the text, defaults to `4`)<br>
**with_url_check** (optional, checks if the URL is valid. This may make the process longer but less error-prone. defaults to `True`)<br>
**clear_cache_after_usage** (optional, Clears the cache after this function is called. adding `delete_all_attributes=True` will also delete all attributes. this defaults to `False`)<br>

***`(async) TwemojiPaser.getsize(text: str, font: PIL.ImageFont, check_for_url: bool, spacing: int, ...) -> tuple`***<br>
**text** (text content.)<br>
**font** (PIL ImageFont object.)<br>
**check_for_url** (optional, checks if image is valid. this makes the process a bit slower but less error-prone. defaults to `True`)<br>
**spacing** (optional, text spacing. defaults to `4`)<br>

***`(async) TwemojiParser.close(delete_all_attributes: bool, ...) -> None`***<br>
**delete_all_attributes** (optional, deletes all object attributes as well to save memory. defaults to `False`)<br>

***`(staticmethod) TwemojiParser.has_emoji(text: str, ...) -> bool`***<br>
**text** (a `string` containing the text to check.)<br>

***`(staticmethod) TwemojiParser.count_emojis(text: str, ...) -> int`***<br>
**text** (a `string` containing the text to check.)<br>

***`(staticmethod) TwemojiParser.get_emojis_from(text: str, ...) -> list[str]`***<br>
**text** (a `string` containing the text to parse.)<br>

***`(async) emoji_to_url(char: str, include_check: bool, use_session: ClientSession, ...)`***<br>
**char** (a `string` of an emoji.)<br>
**include_check** (optional, a `bool` to check if the URL is valid before returning the value. defaults to `True`)<br>
**use_session** (optional, an `aiohttp ClientSession` object to use instead. defaults to `None`)<br>
