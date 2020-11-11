from emoji import UNICODE_EMOJI
from PIL import Image, ImageDraw, ImageFont
from requests import get
from io import BytesIO
from .emote import emoji_to_url

class TwemojiParser:
    def __init__(self, image) -> None:
        """ Creates a parser from PIL.Image.Image object. """
        self.image = image
        self.draw = ImageDraw.Draw(image)
        self.alphabet = list("abcdefghijklmnopqrstuvwxyz0123456789`~!@#$%^&*()_+-=[]\;',./{}|: <>?")
        self.unicode = UNICODE_EMOJI.keys()
    
    def __parse_text(self, text) -> list:
        result = []
        text = text.replace("https://", "<LS>")
        temp_word = ""
        for letter in range(len(text)):
            if text[letter].lower() in self.alphabet:
                if (letter == (len(text) - 1)) and temp_word != "":
                    result.append(temp_word + text[letter]) ; break
                temp_word += text[letter] ; continue
            
            if temp_word != "": result.append(temp_word)
            temp_word = ""
            
            res = emoji_to_url(text[letter])
            if res is not None:
                result.append(res)
            else:
                result.append(text[letter])
        if result == []: return [text]
        return result

    def __image_from_url(self, url) -> Image.Image:
        return Image.open(BytesIO(get(url).content))

    def draw_text(self, xy, text, font=None, spacing=4, *args, **kwargs) -> None:
        """
        Draws a text with the emoji. Parameters are the same as PIL.ImageDraw.text() method.
        WARNING: newlines (like \\n) is not yet supported yet in beta.
        """

        _parsed_text = self.__parse_text(text)
        _font = font if font is not None else ImageFont.load_default()
        _font_size = 11 if not hasattr(_font, "size") else _font.size
        _current_x, _current_y = xy[0], xy[1]

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
                _size = _font.getsize_multiline(_deparsed_text)
                self.draw.text((_current_x, _current_y), _deparsed_text, font=font, *args, **kwargs)
                _current_x += _size[0] + spacing