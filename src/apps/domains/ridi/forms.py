from django import forms


class RequestFrom(forms.Form):
    def get_valid_data(self) -> dict:
        if not super().is_valid():
            raise Exception('test')
        return self.clean()


class AuthorizeForm(RequestFrom):
    client_id = forms.CharField()
    redirect_uri = forms.URLField()
