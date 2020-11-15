import emoji
import requests

cdn_fmt = "https://twemoji.maxcdn.com/v/latest/72x72/{code}.png"

def valid_src(url):
    resp = requests.head(url)
    return resp.status_code == 200

def codepoint(codes):
    if "200d" not in codes:
        return "-".join([c for c in codes if c != "fe0f"])
    return "-".join(codes)

def emoji_to_url(char, include_check=True):
    src = cdn_fmt.format(code=codepoint(["{cp:x}".format(cp=ord(c)) for c in char]))

    if not include_check: return src

    if valid_src(src):
        return src
    else:
        return char