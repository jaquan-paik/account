from django.forms import Form
from django.shortcuts import render
from infra.network.constants.http_status_code import HttpStatusCodes


def invalid_form_response(request, form: Form):
    response = render(request, 'www/error/invalid_form.html', {'message': form.errors})
    response.status_code = HttpStatusCodes.C_400_BAD_REQUEST
    return response
