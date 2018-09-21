class TokenHandler:
    _DELIMITER = ' '
    _BEARER_TOKEN_TYPE = 'Bearer'

    @classmethod
    def make(cls, token: str) -> str:
        return f'{cls._BEARER_TOKEN_TYPE}{cls._DELIMITER}{token}'

    @classmethod
    def parse(cls, token: str) -> str:
        if cls._BEARER_TOKEN_TYPE in token:
            return token.split(cls._DELIMITER)[1]

        return token


class ConfigKeyMaker:
    @staticmethod
    def make_res_key(issuer: str, audience: str) -> str:
        return f'{issuer}:{audience}'

    @staticmethod
    def make_req_key(issuer: str, audience: str) -> str:
        return f'{issuer}:{audience}'
