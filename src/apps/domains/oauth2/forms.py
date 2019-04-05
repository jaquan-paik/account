from django import forms
from apps.domains.oauth2.fields import ClientIdField, ResponseTypeCodeField, RedirectUriField


class AuthorizationCodeForm(forms.Form):
    client_id = ClientIdField()
    response_type = ResponseTypeCodeField()
    redirect_uri = RedirectUriField()
    state = forms.CharField(required=False)
