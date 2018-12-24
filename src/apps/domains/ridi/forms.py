from django import forms


class AuthorizeForm(forms.Form):
    client_id = forms.CharField()
    redirect_uri = forms.URLField()


class CallbackForm(forms.Form):
    code = forms.CharField()
    state = forms.CharField()
    client_id = forms.CharField()
    in_house_redirect_uri = forms.URLField()


class TokenForm(forms.Form):
    access_token = forms.CharField(required=False)
    refresh_token = forms.CharField(required=False)
