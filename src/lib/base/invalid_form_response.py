from django.forms import Form
from django.shortcuts import render
from infra.network.constants.http_status_code import HttpStatusCodes

import json


def invalid_form_response(request, form: Form):
    data = json.dumps(form.errors, ensure_ascii=False)
    response = render(request, 'www/error/invalid_form.html', {'message': data})
    response.status_code = HttpStatusCodes.C_400_BAD_REQUEST
    return response
