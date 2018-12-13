from datetime import datetime, timedelta
from lib.utils.date import generate_cookie_expire_time


class TokenData:
    def __init__(self, token: str, expires_in: int):
        now = datetime.now()

        self.token = token
        self.expires_in = expires_in
        self.expires_at = int((now + timedelta(seconds=expires_in)).timestamp())
        self.cookie_expire_time = generate_cookie_expire_time(expires_in, now)
