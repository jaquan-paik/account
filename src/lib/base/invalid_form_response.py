from django.forms import Form
from django.http import HttpResponse
import json

from infra.network.constants.http_status_code import HttpStatusCodes


class InvalidFormResponse(HttpResponse):

    def __init__(self, form: Form, **kwargs):
        kwargs.setdefault('content_type', 'application/json; charset=utf-8')
        data = json.dumps(form.errors, ensure_ascii=False)
        super().__init__(content=data, status=HttpStatusCodes.C_400_BAD_REQUEST, **kwargs)
