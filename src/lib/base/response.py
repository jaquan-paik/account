from django.http import HttpResponseRedirect
from django.forms import Form
from django.shortcuts import render

from infra.network.constants.http_status_code import HttpStatusCodes


class InHouseHttpResponseRedirect(HttpResponseRedirect):
    allowed_schemes = HttpResponseRedirect.allowed_schemes + ['app']


def get_invalid_form_template_response(request, form: Form):
    message = ''
    for key, value in form.errors.items():
        message += f"{key}: {', '.join(value)}\n"
    return get_template_response(request, '오류가 발생하였습니다.', message, HttpStatusCodes.C_400_BAD_REQUEST)


def get_template_response(request, title: str, message: str, status_code: int):
    response = render(request, 'www/error/error_template.html', {'title': title, 'message': message})
    response.status_code = status_code
    return response
