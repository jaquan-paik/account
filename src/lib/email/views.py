from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from lib.log import sentry
from .forms import AddEmailBlacklistFromMailgunForm
from .services import email_blacklist_service


class MailgunFailureCallback(APIView):
    """
    mailgun에 webhook 으로 등록된 url
    https://documentation.mailgun.com/en/latest/user_manual.html#tracking-failures
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        add_email_blacklist_form = AddEmailBlacklistFromMailgunForm(request.POST)

        if not add_email_blacklist_form.is_valid():
            sentry.message(
                '[EMAIL] {}'.format(add_email_blacklist_form.errors_as_text), extra={'post_data': dict(request.POST.lists()), },
            )
            return Response(status=400)

        email = add_email_blacklist_form.cleaned_data['recipient']
        email_blacklist_service.add_blacklist(email)

        return Response()
