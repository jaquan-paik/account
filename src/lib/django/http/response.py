from django.http import HttpResponse


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504
