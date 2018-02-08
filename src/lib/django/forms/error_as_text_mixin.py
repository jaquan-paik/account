from django import forms
from django.utils.html import strip_tags


class ErrorAsTextMixin(forms.Form):
    @property
    def errors_as_text(self) -> str:
        messages = [value for key, value in self.errors.items()]

        return strip_tags(messages).replace('[', '').replace(']', '').replace('\'', '').replace('\'', '')
