import json
import os

from lib.secret.exceptions import ImproperlyConfigured
from lib.secret.secret_file_handler import SecretFileLoader
from lib.utils.dict import update_only_existed_keys


class _Secret:
    def __init__(self):
        self._secrets = {}
        self._load()

    def get(self, key: str) -> str:
        if key not in self._secrets:
            raise ImproperlyConfigured('Set the {} environment variable!'.format(key))

        return self._secrets[key]

    def _load(self) -> None:
        _secrets = json.loads(SecretFileLoader.load())

        update_only_existed_keys(_secrets, dict(os.environ))

        self._secrets = _secrets


Secret = _Secret()
