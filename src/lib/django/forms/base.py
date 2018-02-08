from django import forms

from .error_as_text_mixin import ErrorAsTextMixin


class BaseForm(ErrorAsTextMixin, forms.Form):
    pass


class BaseModelForm(ErrorAsTextMixin, forms.ModelForm):
    pass
