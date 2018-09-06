class Config:
    def __init__(self, secret: str, alg: str, issuer: str, audience: str):
        self._secret = secret
        self._alg = alg
        self._issuer = issuer
        self._audience = audience

    @property
    def secret(self):
        return self._secret

    @property
    def alg(self):
        return self._alg

    @property
    def issuer(self):
        return self._issuer

    @property
    def audience(self):
        return self._audience
