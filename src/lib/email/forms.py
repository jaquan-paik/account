from django import forms

from infra.email.helper import MailgunHelper
from lib.django.forms.error_as_text_mixin import ErrorAsTextMixin


class AddEmailBlacklistFromMailgunForm(ErrorAsTextMixin, forms.Form):
    event = forms.CharField(required=True)
    recipient = forms.CharField(required=True)
    domain = forms.CharField(required=True)
    reason = forms.CharField(required=True)
    description = forms.CharField(required=False)
    timestamp = forms.CharField(required=True)
    token = forms.CharField(required=True)
    signature = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AddEmailBlacklistFromMailgunForm, self).__init__(*args, **kwargs)
        self.fields['message-headers'] = forms.CharField(required=True)

    def clean(self) -> None:
        timestamp = self.cleaned_data['timestamp']
        token = self.cleaned_data['token']
        signature = self.cleaned_data['signature']

        if not MailgunHelper.is_valid_webhook_token(timestamp, token, signature):
            raise forms.ValidationError('잘못된 webhook 토큰입니다')
