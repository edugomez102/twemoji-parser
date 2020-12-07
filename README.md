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

`TwemojiParser(image: PIL.Image.image, session: aiohttp.ClientSession, ...) -> None`<br>
<ul>
<li><b>image</b> (PIL image object)</li>
<li><b>session</b> (optional, aiohttp client session object, defaults to None)</li>
</ul>

`(async) TwemojiParser.draw_text(xy: tuple, text: str, font: PIL.ImageFont, spacing: int, with_url_check: bool, clear_cache_after_usage: bool, ...) -> None`<br>
<ul>
<li><b>xy</b> (X and y coordinates to put the text on.)</li>
<li><b>text</b> (the text content.)</li>
<li><b>font</b> (optional, PIL.ImageFont object.)</li>
<li><b>spacing</b> (optional, spacing of the text, defaults to 4)</li>
<li><b>with_url_check</b> (optional, checks if the URL is valid. This may make the process longer but less error-prone. defaults to True)</li>
<li><b>clear_cache_after_usage</b> (optional, Clears the cache after this function is called. adding delete_all_attributes=True will also delete all attributes. this defaults to True)</li>
</ul>

`(async) TwemojiPaser.getsize(text: str, font: PIL.ImageFont, check_for_url: bool, spacing: int, ...) -> tuple`<br>
<ul>
<li><b>text</b> (text content.)</li>
<li><b>font</b> (PIL ImageFont object.)</li>
<li><b>check_for_url</b> (optional, checks if image is valid. this makes the process a bit slower but less error-prone. defaults to True)</li>
<li><b>spacing</b> (optional, text spacing. defaults to 4)</li>
</ul>

`(async) TwemojiParser.close(delete_all_attributes: bool, close_session: bool ...) -> None`<br>
<ul>
<li><b>delete_all_attributes</b> (optional, deletes all object attributes as well to save memory. defaults to True)</li>
<li><b>close_session</b> (optional, removes the session object that was either generated or passed into the __init__ of the parser. defaults to True)</li>
</ul>

`(staticmethod) TwemojiParser.has_emoji(text: str, ...) -> bool`<br>
<ul><li><b>text</b> (a string containing the text to check.)</li></ul>

`(staticmethod) TwemojiParser.count_emojis(text: str, ...) -> int`<br>
<ul><li><b>text</b> (a string containing the text to check.)</li></ul>

`(staticmethod) TwemojiParser.get_emojis_from(text: str, ...) -> list[str]`<br>
<ul><li><b>text</b> (a string containing the text to parse.)</li></ul>

`(async) emoji_to_url(char: str, include_check: bool, use_session: ClientSession, ...) -> str`<br>
<ul>
<li><b>char</b> (a string of an emoji.)<br>
<li><b>include_check</b> (optional, a boolean to check if the URL is valid before returning the value. defaults to True)
<li><b>use_session</b> (optional, an aiohttp ClientSession object to use instead. defaults to None)
</ul>
