from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.cache import never_cache, cache_page
from django.views.static import serve

from apps.domains.callback.helpers.url_helper import UrlHelper

script_serve = cache_page(timeout=1200, key_prefix='script-serve')(never_cache(serve))


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return redirect(UrlHelper.get_root_uri())


# HTTP Error 400
def bad_request(request, exception):
    context = {
        'message': exception
    }

    response = render(request, 'www/error/400.html', context)
    response.status_code = 400
    return response


# HTTP Error 403
def permission_denied(request, exception):
    response = render(request, 'www/error/403.html')
    response.status_code = 403
    return response


# HTTP Error 404
def page_not_found(request, exception):
    return redirect(UrlHelper.get_root_uri())


# HTTP Error 500
def server_error(request):
    response = render(request, 'www/error/500.html')
    response.status_code = 500
    return response
