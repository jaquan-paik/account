
class CookieMixin:
    def get_cookie(self, request, key: str, default=None):
        return request.COOKIES.get(key, default)

    def set_cookie(self, response, key: str, value: str, domain: str, **kwargs):
        response.set_cookie(
            key, value, max_age=kwargs.get('expires_in', None), expires=kwargs.get('expires_date', None),
            domain=domain, secure=True, httponly=True
        )

    def clear_cookie(self, response, key: str, domain: str):
        response.set_cookie(
            key, '', max_age=0, expires='Thu, 01-Jan-1970 00:00:00 GMT', domain=domain, secure=True, httponly=True
        )
