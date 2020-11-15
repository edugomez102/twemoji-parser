from emoji import UNICODE_EMOJI
from PIL import Image, ImageDraw, ImageFont
from requests import get
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
        for i in list(text.lower()):
            if i in TwemojiParser.NON_EMOJIS:
                continue
            elif i in TwemojiParser.UNICODES:
                count += 1
        return count
    
    @staticmethod
    def get_emojis_from(text: str, *args, **kwargs) -> list:
        """ A static method that gets the list of emojis from a string. """
        
        res = []
        for i in list(text.lower()):
            if i in TwemojiParser.NON_EMOJIS: continue
            elif i in TwemojiParser.UNICODES:
                res.append(i)
        return res

    def __init__(self, image: Image.Image, *args, **kwargs) -> None:
        """ Creates a parser from PIL.Image.Image object. """
        self.image = image
        self.draw = ImageDraw.Draw(image)
        self.__cache = []
    
    def getsize(self, text: str, font, check_for_url: bool = True, spacing: int = 4, *args, **kwargs) -> tuple:
        """ (BETA) Gets the size of a text. """
        
        _parsed = self.__parse_text(text, check_for_url)
        if len(_parsed) == 1 and (not _parsed[0].startswith("https://")):
            return font.getsize(text)
        _width, _height = 0, font.getsize(text)[1]
        for i in _parsed:
            if not i.startswith("https://"):
                _width += font.getsize(i)[0] + spacing
            _width += _height + spacing
        return (_width - spacing, _height)
    
    def __parse_text(self, text: str, check: bool) -> list:
        result = []
        text = text.replace("https://", "<LS>")
        temp_word = ""
        for letter in range(len(text)):
            if text[letter].lower() in TwemojiParser.NON_EMOJIS:
                if (letter == (len(text) - 1)) and temp_word != "":
                    result.append(temp_word + text[letter]) ; break
                temp_word += text[letter] ; continue
            
            if temp_word != "": result.append(temp_word)
            temp_word = ""
            
            __calculate = [i for i in range(len(self.__cache)) if text[letter] in self.__cache[i].keys()]
            
            if len(__calculate) > 0:
                result.append(self.__cache[__calculate[0]][text[letter]])
                continue

            res = emoji_to_url(text[letter], include_check=check)
            if res is not None:
                result.append(res)
                self.__cache.append({text[letter]: res})
            else:
                result.append(text[letter])
        if result == []: return [text]
        return result

    def __image_from_url(self, url: str) -> Image.Image:
        return Image.open(BytesIO(get(url).content))

    def draw_text(
        self,
        xy: tuple,
        text: str,
        with_url_check: bool = True,
        font=None,
        spacing: int = 4,
        *args, **kwargs
    ) -> None:
        """
        Draws a text with the emoji. Parameters are the same as PIL.ImageDraw.text() method.
        """

        _parsed_text = self.__parse_text(text, with_url_check)
        _font = font if font is not None else ImageFont.load_default()
        _font_size = 11 if not hasattr(_font, "size") else _font.size
        _current_x, _current_y = xy[0], xy[1]
        _origin_x = xy[0]

        if len([i for i in _parsed_text if i.startswith("https://")]) == 0:
            self.draw.text(xy, text, font=font, spacing=spacing, *args, **kwargs)
        else:
            for i in range(len(_parsed_text)):
                if (_parsed_text[i].startswith("https://")):
                    _emoji_im = self.__image_from_url(_parsed_text[i]).resize((_font_size, _font_size)).convert("RGBA")
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