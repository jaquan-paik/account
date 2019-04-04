import base64

from Crypto.Cipher import AES


class CryptoHelper:
    def __init__(self, key):
        self.__key = key
        self.__bs = 16

    def encrypt(self, message: str) -> str:
        message = message.encode()
        raw = self._pad(message)
        cipher = AES.new(self.__key, AES.MODE_CBC, self._get_iv())
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc: str) -> str:
        enc = base64.b64decode(enc)
        cipher = AES.new(self.__key, AES.MODE_CBC, self._get_iv())
        dec = cipher.decrypt(enc)
        return self._unpad(dec).decode('utf-8')

    def _get_iv(self) -> str:
        return chr(0) * self.__bs

    def _pad(self, string):
        return string + (self.__bs - len(string) % self.__bs) * chr(self.__bs - len(string) % self.__bs).encode()

    def _unpad(self, byte_string: bytes) -> bytes:
        return byte_string[:-ord(byte_string[len(byte_string) - 1:])]
