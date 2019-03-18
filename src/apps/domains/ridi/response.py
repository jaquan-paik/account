import json

from django.http import HttpResponseRedirect
from django.forms import Form
from django.shortcuts import render

from apps.domains.oauth2.constants import ErrorMessage
from infra.network.constants.http_status_code import HttpStatusCodes


class InHouseHttpResponseRedirect(HttpResponseRedirect):
    allowed_schemes = HttpResponseRedirect.allowed_schemes + ['app']


def get_invalid_form_template_response(request, form: Form):
    message = ''
    for key, value in form.errors.items():
        message += f"{key}: {', '.join(value)}\n"
    response = render(request, 'www/error/400.html', {'message': message})
    response.status_code = HttpStatusCodes.C_400_BAD_REQUEST
    return response


def get_template_from_form_error(request, errors: Form.errors):
    message = ''
    errors_details = errors.get_json_data()
    code = HttpStatusCodes.C_400_BAD_REQUEST
    for error_key, error_list in errors_details.items():
        message += f"{error_key}: "
        for error in error_list:
            message += f"{error.get('message')}\n"
            code = error.get('code')
        response = render(request, 'www/error/400.html', {'message': message})
        response.status_code = ErrorMessage.get_code_from_error_message(code)
        return response
