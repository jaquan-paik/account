from django import forms
from apps.domains.oauth2.fields import ClientIdField, ResponseTypeCodeField, RedirectUriField, ClientSecretField, CodeField, \
    RefreshTokenField, UsernameField, PasswordField


class AuthorizationCodeForm(forms.Form):
    client_id = ClientIdField()
    response_type = ResponseTypeCodeField()
    redirect_uri = RedirectUriField()
    state = forms.CharField(required=False)


class AuthorizationTokenForm(forms.Form):
    client_id = ClientIdField()
    client_secret = ClientSecretField()
    code = CodeField()
    redirect_uri = RedirectUriField()


class RefreshTokenForm(forms.Form):
    client_id = ClientIdField()
    client_secret = ClientSecretField()
    refresh_token = RefreshTokenField()


class PasswordTokenForm(forms.Form):
    client_id = ClientIdField()
    client_secret = ClientSecretField()
    username = UsernameField()
    password = PasswordField()
