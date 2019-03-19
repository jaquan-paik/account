from django import forms

from apps.domains.oauth2.constants import ResponseType


# pylint:disable=arguments-differ

class ClientIdField(forms.CharField):
    def validate(self, client_id):
        if not client_id:
            raise forms.ValidationError('client id is required')


class ResponseTypeCodeField(forms.CharField):
    def validate(self, response_type):
        if not response_type:
            raise forms.ValidationError('response_type is required')
        if response_type != ResponseType.CODE:
            raise forms.ValidationError('unsupported response_type')


class RedirectUriField(forms.URLField):
    def validate(self, redirect_uri):
        if not redirect_uri:
            raise forms.ValidationError('redirect_uri is required')
