from django.http import HttpResponseRedirect
from django.views import View
from oauthlib.oauth2 import OAuth2Error

from apps.domains.oauth2.forms import AuthorizationCodeForm
from apps.domains.oauth2.services.oauth2_authorization_code_service import OAuth2AuthorizationCodeService
from lib.base.response import get_invalid_form_template_response, get_template_response
from lib.decorators.session_login import ridibooks_session_login_required
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
