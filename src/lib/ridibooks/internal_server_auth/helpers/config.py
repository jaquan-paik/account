from typing import Dict, List, Tuple

from lib.ridibooks.internal_server_auth.utils import make_auth_data_key

ISSUER_KEY_NAME = 'iss'
SUBJECT_KEY_NAME = 'sub'
SECRET_KEY_NAME = 'secret'
ALGORITHM_KEY_NAME = 'alg'

DEFAULT_ALGORITHM = 'RS256'


class ConfigHelper:
    @staticmethod
    def generate_auth_data(auth_data_list: List) -> Dict:
        _validate_type(auth_data_list)

        config = {}

        for auth_data in auth_data_list:
            issuer, subject, secret, algorithm = _destruct_auth_data(auth_data=auth_data)
            key = make_auth_data_key(issuer=issuer, subject=subject)
            config[key] = (secret, algorithm)

        return config


def _destruct_auth_data(auth_data: Dict) -> Tuple[str, str, str, str]:
    issuer = auth_data[ISSUER_KEY_NAME]
    subject = auth_data[SUBJECT_KEY_NAME]
    secret = auth_data[SECRET_KEY_NAME]
    algorithm = auth_data.get(ALGORITHM_KEY_NAME, DEFAULT_ALGORITHM)

    return issuer, subject, secret, algorithm


def _validate_type(auth_data_list: List):
    if isinstance(auth_data_list, list):
        return

    raise TypeError
