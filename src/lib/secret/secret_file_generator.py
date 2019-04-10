import json
from typing import Dict, List

from lib.aws.parameter_store import ParameterStoreConnector
from lib.secret.constants import SecretEnvironment
from lib.secret.exceptions import ImproperlyConfigured
from lib.secret.secret_file_handler import BaseSecretFileHandler


class BaseRawSecretLoader:
    def __init__(self, secret_key_list: List[str], *args, **kwargs):
        self._secret_key_list = secret_key_list

    def load_secrets(self) -> Dict:
        secrets = self._load_secrets()
        if self._secret_key_list:
            self._assert_if_improperly_configured(secrets, self._secret_key_list)
        return secrets

    def _load_secrets(self) -> Dict:
        raise NotImplementedError

    @staticmethod
    def _assert_if_improperly_configured(secrets: Dict, secret_key_list: List[str]):
        for secret_key in secret_key_list:
            if secret_key not in secrets:
                raise ImproperlyConfigured(f'There is no secret : {secret_key}')


class RawSecretParameterStoreLoader(BaseRawSecretLoader):
    def __init__(self, env: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._env = env

    def _load_secrets(self) -> Dict:
        secret_env = SecretEnvironment.to_string(self._env)
        return ParameterStoreConnector().load_parameters(secret_env)


class RawSecretFileLoader(BaseRawSecretLoader):
    def __init__(self, secret_file_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._secret_file_path = secret_file_path

    def _load_secrets(self) -> Dict:
        try:
            with open(self._secret_file_path) as file:
                return json.loads(file.read())

        except (OSError, IOError):
            raise ImproperlyConfigured('There is no setting file %s' % self._secret_file_path)


class SecretFileGenerator(BaseSecretFileHandler):
    @classmethod
    def generate(cls, raw_secret_loader: BaseRawSecretLoader) -> None:
        secrets = raw_secret_loader.load_secrets()
        encrypted_secrets_json = cls._encrypt_secrets(secrets)
        cls._save_encrypted_file(encrypted_secrets_json)

    @classmethod
    def _encrypt_secrets(cls, secrets: Dict) -> str:
        secrets_json = json.dumps(secrets)
        return cls._encrypt(secrets_json)

    @classmethod
    def _save_encrypted_file(cls, enc_string: str) -> None:
        cls._save_file(cls._get_enc_secret_file_name(), enc_string)

    @classmethod
    def _save_file(cls, file_name: str, content: str) -> None:
        file_path = cls._get_file_path(file_name)
        with open(file_path, 'w') as file:
            file.write(content)
