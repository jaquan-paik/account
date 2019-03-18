from django import forms

from apps.domains.oauth2.constants import ResponseType, ErrorMessage


# pylint:disable=arguments-differ

class ClientIdField(forms.CharField):
    def validate(self, client_id):
        if not client_id:
            raise forms.ValidationError('client_id는 필수 값입니다.', ErrorMessage.REQUIRED_CLIENT_ID)


class ResponseTypeCodeField(forms.CharField):
    def validate(self, response_type):
        if not response_type:
            raise forms.ValidationError('response_type은 필수 값입니다.', ErrorMessage.REQUIRED_RESPONSE_TYPE)
        if response_type != ResponseType.CODE:
            raise forms.ValidationError('지원되지 않는 response_type 입니다.', ErrorMessage.UNSUPPORTED_RESPONSE_TYPE)


class RedirectUriField(forms.URLField):
    def validate(self, redirect_uri):
        if not redirect_uri:
            raise forms.ValidationError('redirect_uri는 필수 값입니다.', ErrorMessage.REQUIRED_REDIRECT_URI)
