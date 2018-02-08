import re

_emoji_pattern = re.compile(
    '['
    u'\U0001F600-\U0001F64F'  # emoticons
    u'\U0001F300-\U0001F5FF'  # symbols & pictographs
    u'\U0001F680-\U0001F6FF'  # transport & map symbols
    u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
    ']+', flags=re.UNICODE
)

_HANGUL_CODE_MIN = 0xAC00
_HANGUL_CODE_MAX = 0xD7A3


def is_include_emoji(string: str) -> bool:
    if _emoji_pattern.search(string) is None:
        return False

    return True


def is_last_char_has_batchim(char: str) -> bool:

    if len(char) != 1:
        char = char[-1]

    char_code = ord(char)
    if char_code < _HANGUL_CODE_MIN or char_code > _HANGUL_CODE_MAX:
        return False
    elif (char_code - 0xAC00) % 28 == 0:
        return False

    return True
