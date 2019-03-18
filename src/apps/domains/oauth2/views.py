from django.http import JsonResponse
from rest_framework.views import APIView

from infra.network.constants.http_status_code import HttpStatusCodes
from lib.ridibooks.store_auth.drf_middlewares import DrfAuthentication


class AuthorizeView(APIView):
    authentication_classes = (DrfAuthentication,)

    def get(self, request):
        # authorize_form = AuthorizeForm(request.GET)
        # if not authorize_form.is_valid():
        #     return get_invalid_form_template_response(request, authorize_form)
        # cleaned_data = authorize_form.clean()
        # url = AuthorizationCodeService.get_oauth2_authorize_url(cleaned_data['client_id'], cleaned_data['redirect_uri'], request.user.idx)
        return JsonResponse(data={}, status=HttpStatusCodes.C_200_OK)
