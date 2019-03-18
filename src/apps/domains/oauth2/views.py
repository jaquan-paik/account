from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View

from apps.domains.oauth2.forms import AuthorizationForm
from apps.domains.oauth2.services.oauth2_authorization_code_service import OAuth2AuthorizationCodeService
from apps.domains.ridi.response import get_template_from_form_error
from lib.utils.url import generate_query_url


class AuthorizationView(LoginRequiredMixin, View):
    def get(self, request):
        authorize_form = AuthorizationForm(request.GET)
        if not authorize_form.is_valid():
            return get_template_from_form_error(request, authorize_form.errors)
        cleaned_data = authorize_form.clean()
        code = OAuth2AuthorizationCodeService.create_code(cleaned_data['client_id'], cleaned_data['redirect_uri'], request.user.idx)

        redirect_param = {'code': code}
        if cleaned_data['state']:
            redirect_param['state'] = cleaned_data['state']

        redirect_uri = generate_query_url(cleaned_data['redirect_uri'], redirect_param)
        return HttpResponseRedirect(redirect_uri)
