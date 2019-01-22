from django.http import HttpResponseRedirect
from django.forms import Form
from django.shortcuts import render
from infra.network.constants.http_status_code import HttpStatusCodes


class InHouseHttpResponseRedirect(HttpResponseRedirect):
    allowed_schemes = HttpResponseRedirect.allowed_schemes + ['app']


def get_invalid_form_template_response(request, form: Form):
    response = render(request, 'www/error/invalid_form.html', {'message': form.errors})
    response.status_code = HttpStatusCodes.C_400_BAD_REQUEST
    return response
