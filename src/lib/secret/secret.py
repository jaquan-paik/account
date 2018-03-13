import json
import os
from typing import Dict

from infra.storage.ssm.connectors import ParameterStoreConnector
from lib.crypto.encrypt import CryptoHelper
from lib.singleton.singleton import Singleton

DEFAULT_ROOT_PATH = '/htdocs/www'
CRYPTO_KEY = '!Ck[v%W}$5,4@-5R'
ENC_SECRET_FILE_NAME = 'enc_secrets.json'
SECRET_FILE_NAME = 'secrets.json'
VERSION_FILE_NAME = 'version'
ENV_DEV = 'account_dev'
ENV_PROD = 'prod'


class ImproperlyConfigured(Exception):
    pass


class _Secret:
    # private member
    __secrets = None

    version = '-'

    def __init__(self):
        self._set_root_path()
        self.file_handler = SecretFileHandler()
        self._load()

    def get(self, key: str) -> str:
        try:
            return self.__secrets[key]
        except KeyError:
            raise ImproperlyConfigured('Set the {} environment variable!'.format(key))

    def _load(self) -> None:
        self.__secrets = json.loads(self.file_handler.load())
        self.version = self._load_version_file()

    def _load_version_file(self) -> str:
        file_path = '%s/%s' % (self.root_path, VERSION_FILE_NAME)

        try:
            with open(file_path) as file:
                return file.read().strip()
        except (OSError, IOError):
            return '-'

    def _set_root_path(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


Secret = Singleton(_Secret)


class SecretFileHandler:
    def __init__(self):
        self._set_root_path()

    def _set_root_path(self) -> None:
        self.root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    def _get_file_path(self, file_name: str) -> str:
        return os.path.join(self.root_path, file_name)

    def _save_encrypted_file(self, enc_string: str) -> None:
        self._save_file(ENC_SECRET_FILE_NAME, enc_string)

    def _save_decrypted_file(self, dec_string) -> None:
        self._save_file(SECRET_FILE_NAME, dec_string)

    def _save_file(self, file_name: str, content: str) -> None:
        file_path = self._get_file_path(file_name)
        with open(file_path, 'w') as file:
            file.write(content)

    def load(self) -> str:
        enc_file_path = self._get_file_path(ENC_SECRET_FILE_NAME)

        try:
            with open(enc_file_path) as file:
                return CryptoHelper(CRYPTO_KEY).decrypt(file.read())
        except (OSError, IOError):
            raise ImproperlyConfigured('There is no setting file %s' % enc_file_path)


class SecretFileGenerator(SecretFileHandler):
    def generate(self, env: str) -> None:
        secrets = self._load_secrets(env)

        encrypted_secrets_json = self.encrypt_secrets(secrets)
        self._save_encrypted_file(encrypted_secrets_json)

    def _load_secrets(self, env: str) -> Dict:
        return ParameterStoreConnector().load_parameters(env)

    def encrypt_secrets(self, secrets: Dict) -> str:
        secrets_json = json.dumps(secrets)
        return CryptoHelper(CRYPTO_KEY).encrypt(secrets_json)

    def _get_file_path(self, file_name: str) -> str:
        return os.path.join(self.root_path, file_name)


class SecretFileConverter(SecretFileHandler):
    def convert_to_encrypted_file(self) -> None:
        enc_string = self._encrypt_file()
        self._save_file(ENC_SECRET_FILE_NAME, enc_string)

    def _encrypt_file(self) -> str:
        file_path = self._get_file_path(SECRET_FILE_NAME)

        try:
            with open(file_path) as file:
                return CryptoHelper(CRYPTO_KEY).encrypt(file.read())
        except (OSError, IOError):
            raise ImproperlyConfigured('There is no setting file %s' % file_path)
