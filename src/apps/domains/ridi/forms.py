from django import forms

from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.state_helper import StateHelper


class AuthorizeForm(forms.Form):
    client_id = forms.CharField()
    redirect_uri = forms.URLField()

    def clean(self) -> dict:
        cleaned_data = super().clean()
        client = ClientHelper.get_in_house_client(cleaned_data.get('client_id'))
        ClientHelper.validate_redirect_uri(client, cleaned_data.get('redirect_uri'))
        return cleaned_data


class CallbackForm(forms.Form):
    code = forms.CharField()
    state = forms.CharField()
    client_id = forms.CharField()
    in_house_redirect_uri = forms.URLField()
    u_idx = forms.IntegerField()

    def clean(self) -> dict:
        cleaned_data = super().clean()
        StateHelper.validate_state(cleaned_data.get('state'), cleaned_data.get('u_idx'))
        return cleaned_data


class TokenForm(forms.Form):
    access_token = forms.CharField(required=False)
    refresh_token = forms.CharField(required=False)
