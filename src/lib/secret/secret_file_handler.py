import os
from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError

from lib.aws.parameter_store import ParameterStoreConnector
from lib.crypto.encrypt import CryptoHelper
from lib.secret.exceptions import ImproperlyConfigured

_SECRET_FILE_CRYPTO_KEY_NAME = 'SECRET_FILE_CRYPTO_KEY'
_PARAMETER_STORE_KEY_NAME = '/library/secret_file_crypto_key/0000'
_DEFAULT_SECRET_FILE_CRYPTO_KEY = '}rWWzHGU6G@t2d#9'
_ENC_SECRET_FILE_NAME = 'enc_secrets.json'


class CryptoKeyHandler:
    @classmethod
    def get_crypto_key(cls) -> str:
        # 키 사용 우선순위
        # 1. 환경변수 2. ParameterStore 3. 기본값
        try:
            return cls._load_from_os_env()
        except ImproperlyConfigured:
            pass

        try:
            return cls._load_from_parameter_store()
        except ImproperlyConfigured:
            pass

        return _DEFAULT_SECRET_FILE_CRYPTO_KEY

    @staticmethod
    def _load_from_os_env() -> str:
        _crypto_key = os.environ.get(_SECRET_FILE_CRYPTO_KEY_NAME)
        if _crypto_key:
            return _crypto_key

        raise ImproperlyConfigured

    @staticmethod
    def _load_from_parameter_store() -> str:
        try:
            return ParameterStoreConnector().load_parameter(_PARAMETER_STORE_KEY_NAME)
        except (BotoCoreError, Boto3Error):
            raise ImproperlyConfigured


class BaseSecretFileHandler:
    @staticmethod
    def _get_root_path() -> str:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    @staticmethod
    def _get_enc_secret_file_name() -> str:
        return _ENC_SECRET_FILE_NAME

    @classmethod
    def _get_file_path(cls, file_name: str) -> str:
        return os.path.join(cls._get_root_path(), file_name)

    @staticmethod
    def _get_crypto_key() -> str:
        return CryptoKeyHandler.get_crypto_key()

    @classmethod
    def _encrypt(cls, data: str):
        return CryptoHelper(cls._get_crypto_key()).encrypt(data)

    @classmethod
    def _decrypt(cls, data: str):
        return CryptoHelper(cls._get_crypto_key()).decrypt(data)


class SecretFileLoader(BaseSecretFileHandler):
    @classmethod
    def load(cls) -> str:
        enc_file_path = cls._get_file_path(cls._get_enc_secret_file_name())

        try:
            with open(enc_file_path) as file:
                return cls._decrypt(file.read())

        except (OSError, IOError):
            raise ImproperlyConfigured('There is no setting file %s' % enc_file_path)
