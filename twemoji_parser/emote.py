import emoji
from aiohttp import ClientSession

cdn_fmt = "https://twemoji.maxcdn.com/v/latest/72x72/{code}.png"


async def valid_src(url: str, session: ClientSession):
    async with session.head(url) as resp:
        status = resp.status
    return status == 200


def codepoint(codes):
    if "200d" not in codes:
        return "-".join([c for c in codes if c != "fe0f"])
    return "-".join(codes)


async def emoji_to_url(char, include_check: bool = True, session: ClientSession = None):
    src = cdn_fmt.format(code=codepoint(["{cp:x}".format(cp=ord(c)) for c in char]))
    if not include_check:
        return src
    
    session = session if session else ClientSession()
    is_valid = await valid_src(src, session)
    if not session:
        await session.close()

    if is_valid:
        return src
    return char