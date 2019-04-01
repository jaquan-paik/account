from django.views import View
from rest_framework.views import APIView
from ridi_django_oauth2.decorators import login_required

from lib.decorators.ridi_oauth2_access_token_login import ridi_oauth2_access_token_login
from lib.django.views.api.mixins import ResponseMixin


class RequestSSOTokenView(ResponseMixin, APIView):
    @ridi_oauth2_access_token_login
    @login_required()
    def get(self, request):
        pass


class VerifySSOTokenView(ResponseMixin, APIView):
    def get(self, request):
        pass


class SSOLoginView(View):
    def get(self, request):
        pass
