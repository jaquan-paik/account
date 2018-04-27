from django.http import HttpResponseRedirect


class InHouseHttpResponseRedirect(HttpResponseRedirect):
    allowed_schemes = HttpResponseRedirect.allowed_schemes + ['app']
