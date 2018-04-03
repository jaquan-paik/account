

class SessionMixin:
    def get_session(self, key: str, default=None):
        return self.request.session.get(key, default)

    def set_session(self, key: str, value: str):
        self.request.session[key] = value
