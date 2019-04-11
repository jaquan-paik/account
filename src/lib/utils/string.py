import random
import re
import string as string_lib

_emoji_pattern = re.compile(
    '['
    u'\U0001F600-\U0001F64F'  # emoticons
    u'\U0001F300-\U0001F5FF'  # symbols & pictographs
    u'\U0001F680-\U0001F6FF'  # transport & map symbols
    u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
    ']+', flags=re.UNICODE
)
_UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                                'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                '0123456789')
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


def generate_random_str(n: int, alphabet_and_number_only=False) -> str:
    if alphabet_and_number_only:
        return ''.join(random.choices(_UNICODE_ASCII_CHARACTER_SET, k=n))
    return ''.join(random.choices(_filter_generatable_char(string_lib.ascii_letters + string_lib.digits + string_lib.punctuation), k=n))


def _filter_generatable_char(generatable_char: str) -> str:
    not_allow_chars = "\"'"

    for char in not_allow_chars:
        generatable_char = generatable_char.replace(char, "")

    return generatable_char
