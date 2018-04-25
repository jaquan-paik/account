from django.http import HttpResponse


class HttpUnauthorized(HttpResponse):
    status_code = 401
