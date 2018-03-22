from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from lib.cache.mixins import CachePageMixin
from lib.utils.file import FileHandler


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'www/index.html')


@method_decorator(never_cache, 'dispatch')
class TokenRefresherView(CachePageMixin, View):
    PAGE_CACHE_TTL = 1200

    def get(self, request):
        file = FileHandler('templates/script/ridi_token_refresher.js').load()
        return HttpResponse(content=file, content_type='application/javascript')


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
    response = render(request, 'www/error/404.html')
    response.status_code = 404
    return response


# HTTP Error 500
def server_error(request, exception):
    response = render(request, 'www/error/500.html')
    response.status_code = 500
    return response
