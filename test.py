from twemoji_parser import TwemojiParser
import asyncio
import PIL as p
from time import time

async def main(text):
    f = p.ImageFont.truetype(r"C:\Users\user\Documents\githubsite\username601\assets\fonts\NotoSansDisplay-Bold.otf", 30)
    i = p.Image.new("RGB", (500, 500), color=(255, 255, 255))
    a = time()
    parse = TwemojiParser(i)
    await parse.draw_text((5, 5), text, font=f, fill="black")
    print(time() - a)
    await parse.close()
    i.show()

loop = asyncio.get_event_loop()
loop.run_until_complete(main("hello world🗿asdasd🗿🗿asdsadasd"))