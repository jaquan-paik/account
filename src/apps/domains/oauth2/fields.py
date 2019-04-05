from django import forms

from apps.domains.oauth2.constants import ResponseType


# pylint:disable=arguments-differ

class ClientIdField(forms.CharField):
    def validate(self, client_id):
        if not client_id:
            raise forms.ValidationError('client id is required')


class ClientSecretField(forms.ChoiceField):
    def validate(self, client_secret):
        if not client_secret:
            raise forms.ValidationError('client secret is required')


class ResponseTypeCodeField(forms.CharField):
    def validate(self, response_type):
        if not response_type:
            raise forms.ValidationError('response_type is required')
        if response_type != ResponseType.CODE:
            raise forms.ValidationError('this response_type is unsupported')


class RedirectUriField(forms.URLField):
    def validate(self, redirect_uri):
        if not redirect_uri:
            raise forms.ValidationError('redirect_uri is required')


class CodeField(forms.CharField):
    def validate(self, code):
        if not code:
            raise forms.ValidationError('code is required')


class RefreshTokenField(forms.CharField):
    def validate(self, refresh_token):
        if not refresh_token:
            raise forms.ValidationError('refresh token is required')


class UsernameField(forms.CharField):
    def validate(self, username):
        if not username:
            raise forms.ValidationError('username is required')


class PasswordField(forms.CharField):
    def validate(self, password):
        if not password:
            raise forms.ValidationError('password is required')
