from django import forms

from apps.domains.ridi.helpers.client_helper import ClientHelper
from apps.domains.ridi.helpers.state_helper import StateHelper

from lib.ridibooks.common.constants import ACCESS_TOKEN_COOKIE_KEY, REFRESH_TOKEN_COOKIE_KEY


class RequestFrom(forms.Form):
    def get_valid_data(self) -> dict:
        if not super().is_valid():
            raise Exception('test')  # TODO : invalid reqeust로 error 연동 (뭐가 없는지), 아니면 form error 관련 찾아서 추가
        return self.clean()


class AuthorizeForm(RequestFrom):
    client_id = forms.CharField()
    redirect_uri = forms.URLField()

    def get_valid_data_with_client_check(self):
        valid_data = super().get_valid_data()
        client = ClientHelper.get_in_house_client(valid_data['client_id'])
        ClientHelper.validate_redirect_uri(client, valid_data['redirect_uri'])
        return valid_data


class CallbackForm(RequestFrom):
    code = forms.CharField()
    state = forms.CharField()
    client_id = forms.CharField()
    in_house_redirect_uri = forms.URLField()

    def get_valid_data_with_state_check(self, u_idx) -> dict:
        valid_data = self.get_valid_data()
        StateHelper.validate_state(valid_data['state'], u_idx)
        return valid_data


class TokenForm(RequestFrom):
    access_token = forms.CharField(required=False)
    refresh_token = forms.CharField()

    def get_valid_data(self):
        self.data['access_token'] = self.data.get(ACCESS_TOKEN_COOKIE_KEY, None)
        self.data['refresh_token'] = self.data.get(REFRESH_TOKEN_COOKIE_KEY, None)
        return super().get_valid_data()
