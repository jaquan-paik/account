from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from two_factor.utils import default_device

from infra.configure.config import GeneralConfig


class TwoFactorEnforceMiddleware(MiddlewareMixin):
    def is_two_factor_url(self, request) -> bool:
        return request.path in [
            reverse('two_factor:login'), reverse('two_factor:setup'), reverse('two_factor:qr'), reverse('two_factor:setup_complete')
        ]

    def process_request(self, request):
        user = request.user
        if GeneralConfig.is_enforce_2fa() and not self.is_two_factor_url(request) \
                and user.is_authenticated and default_device(user) is None:
            return redirect('two_factor:setup')
