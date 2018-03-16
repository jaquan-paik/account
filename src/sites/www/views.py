from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'www/index.html')


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
