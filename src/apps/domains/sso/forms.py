from urllib import parse

from django import forms

from lib.utils.url import is_url


class SSOLoginForm(forms.Form):
    redirect_uri = forms.CharField(required=True, label='Redirect URI')

    def __init__(self, domain: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = domain

    def clean_next(self):
        data = self.cleaned_data['redirect_uri']

        if not is_url(data):
            raise forms.ValidationError('URI를 입력해주세요.')

        parsed_url = parse.urlsplit(data)
        if self.domain not in parsed_url.netloc:
            raise forms.ValidationError('유효한 URI를 입력해주세요.')

        return data
