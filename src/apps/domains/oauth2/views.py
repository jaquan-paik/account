from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from oauthlib.oauth2 import OAuth2Error
from rest_framework.views import APIView

from apps.domains.oauth2.exceptions import UnsupportedGrantType
from apps.domains.oauth2.forms import AuthorizationCodeForm
from apps.domains.oauth2.serializers import GrantTypeSerializer
from apps.domains.oauth2.services.oauth2_authorization_code_service import OAuth2AuthorizationCodeService
from lib.base.response import get_invalid_form_template_response, get_template_response
from lib.decorators.session_login import ridibooks_session_login_required
from lib.django.views.api.mixins import ResponseMixin
from lib.utils.url import generate_query_url


class AuthorizationView(View):
    @ridibooks_session_login_required()
    def get(self, request):
        authorize_form = AuthorizationCodeForm(request.GET)
        if not authorize_form.is_valid():
            return get_invalid_form_template_response(request, authorize_form)
        cleaned_data = authorize_form.clean()

        try:
            code = OAuth2AuthorizationCodeService.create_code(cleaned_data['client_id'], cleaned_data['redirect_uri'], request.user.idx)
        except OAuth2Error as e:
            return get_template_response(request, e.error, e.description, e.status_code)

        redirect_param = {'code': code}
        if cleaned_data['state']:
            redirect_param['state'] = cleaned_data['state']

        redirect_uri = generate_query_url(cleaned_data['redirect_uri'], redirect_param)
        return HttpResponseRedirect(redirect_uri)


class TokenView(ResponseMixin, APIView):
    def post(self, request):
        grant_type_serializer = GrantTypeSerializer(data=request.data)
        try:
            if not grant_type_serializer.is_valid():
                raise UnsupportedGrantType
        except OAuth2Error as e:
            return JsonResponse(data={"error": e.error, "description": e.description}, status=e.status_code)
