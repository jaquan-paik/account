from urllib import parse

from django import forms

from lib.utils.url import is_url


class SSOLoginForm(forms.Form):
    otp = forms.CharField(required=True, label='SSO Otp')
    redirect_uri = forms.CharField(required=False, label='Redirect URI')

    def __init__(self, *args, domain: str, **kwargs):
        super().__init__(*args, **kwargs)
        self._domain = domain

    def clean_redirect_uri(self):
        data = self.cleaned_data.get('redirect_uri', '')
        if not data:
            return data

        if not is_url(data):
            raise forms.ValidationError('URI를 입력해주세요.')

        parsed_url = parse.urlsplit(data)
        if self._domain not in parsed_url.netloc:
            raise forms.ValidationError('유효한 URI를 입력해주세요.')

        return data
