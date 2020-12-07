from emoji import UNICODE_EMOJI
from PIL import Image, ImageDraw, ImageFont
from aiohttp import ClientSession
from io import BytesIO
from .emote import emoji_to_url

class TwemojiParser:
    UNICODES = UNICODE_EMOJI.keys()
    NON_EMOJIS = list("abcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()_+-=[]\;',./{}|: <>?")

    @staticmethod
    def has_emoji(text: str, *args, **kwargs) -> bool:
        """ A static method that checks if a text has an emoji. """
        
        return TwemojiParser.count_emojis(text) > 0

    @staticmethod
    def count_emojis(text: str, *args, **kwargs) -> int:
        """ A static method that counts the emojis from a string. """
        
        count = 0
        for i in list(text.lower().replace(" ", "")):
            if i.isalpha() or i.isnumeric() or i in TwemojiParser.NON_EMOJIS:
                continue
            elif i in TwemojiParser.UNICODES:
                count += 1
        return count
    
    @staticmethod
    def get_emojis_from(text: str, *args, **kwargs) -> list:
        """ A static method that gets the list of emojis from a string. """
        
        res = []
        for i in list(text.lower()):
            if i.isalpha() or i.isnumeric() or i in TwemojiParser.NON_EMOJIS: continue
            elif i in TwemojiParser.UNICODES:
                res.append(i)
        return res

    def __init__(self, image: Image.Image, *args, **kwargs) -> None:
        """ Creates a parser from PIL.Image.Image object. """
        self.image = image
        self.draw = ImageDraw.Draw(image)
        self._emoji_cache = {}
        self._image_cache = {}
        self.__session = ClientSession()
    
    async def getsize(self, text: str, font, check_for_url: bool = True, spacing: int = 4, *args, **kwargs) -> tuple:
        """ (BETA) Gets the size of a text. """
        
        _parsed = await self.__parse_text(text, check_for_url)
        if len(_parsed) == 1 and (not _parsed[0].startswith("https://")):
            return font.getsize(text)
        _width, _height = 0, font.getsize(text)[1]
        for i in _parsed:
            if not i.startswith("https://"):
                _width += font.getsize(i)[0] + spacing
            _width += _height + spacing
        return (_width - spacing, _height)
    
    async def __parse_text(self, text: str, check: bool) -> list:
        result = []
        # please don't put <lS> on your text, thank you
        text = text.replace("https://", "<LS>")
        temp_word = ""
        for letter in range(len(text)):
            if text[letter].isalpha() or text[letter].isnumeric() or (text[letter] in TwemojiParser.NON_EMOJIS):
                # basic text case
                if (letter == (len(text) - 1)) and temp_word != "":
                    result.append(temp_word + text[letter]) ; break
                temp_word += text[letter] ; continue
            
            # check if there is an empty string in the array
            if temp_word != "": result.append(temp_word)
            temp_word = ""
            
            if text[letter] in self._emoji_cache.keys():
                # store in cache so it uses less HTTP requests
                result.append(self._emoji_cache[text[letter]])
                continue

            # include_check will check the URL if it's valid. Disabling it will make the process faster, but more error-prone
            res = await emoji_to_url(text[letter], include_check=check)
            if res != text[letter]:
                result.append(res)
                self._emoji_cache[text[letter]] = res
            else:
                result.append(text[letter])
        
        if result == []: return [text]
        return result

    async def __image_from_url(self, url: str) -> Image.Image:
        """ Gets an image from URL. """
        resp = await self.__session.get(url)
        _byte = await resp.read()
        return Image.open(BytesIO(_byte))

    async def draw_text(
        self,
        # Same PIL options
        xy: tuple,
        text: str,
        with_url_check: bool = True,
        font=None,
        spacing: int = 4,
        
        # Parser options
        clear_cache_after_usage: bool = False,
        
        *args, **kwargs
    ) -> None:
        """
        Draws a text with the emoji.
        clear_cache_after_usage will clear the cache after this method is finished. (defaults to False)
        """

        _parsed_text = await self.__parse_text(text, with_url_check)
        _font = font if font is not None else ImageFont.load_default()
        _font_size = 11 if not hasattr(_font, "size") else _font.size
        _current_x, _current_y = xy[0], xy[1]
        _origin_x = xy[0]

        if len([i for i in _parsed_text if i.startswith("https://")]) == 0:
            self.draw.text(xy, text, font=font, spacing=spacing, *args, **kwargs)
        else:
            for i in range(len(_parsed_text)):
                if (_parsed_text[i].startswith("https://")):
                    # check if image is in cache
                    if _parsed_text[i] in self._image_cache.keys():
                        _emoji_im = self._image_cache[_parsed_text[i]].copy()
                    else:
                        _emoji_im = await self.__image_from_url(_parsed_text[i]).resize((_font_size, _font_size))
                        self._image_cache[_parsed_text[i]] = _emoji_im.copy()
                    
                    self.image.paste(_emoji_im, (_current_x, _current_y), _emoji_im)
                    _current_x += _font_size + spacing
                    continue
                _deparsed_text = _parsed_text[i].replace("<LS>", "https://")
                _size = _font.getsize(_deparsed_text.replace("\n", ""))
                if _deparsed_text.count("\n") > 0:
                    _current_x = _origin_x - spacing
                    _current_y += (_font_size * _deparsed_text.count("\n"))
                self.draw.text((_current_x, _current_y), _deparsed_text, font=font, *args, **kwargs)
                _current_x += _size[0] + spacing
    
    async def close(self):
        """ Closes the aiohttp ClientSession and clears all the cache. """
        
        await self.__session.close()
        self._emoji_cache = {}
        self._image_cache = {}
