from django.urls import path

from .views import MailgunFailureCallback

urlpatterns = [
    path('mailgun/callback/', MailgunFailureCallback.as_view(), name='mailgun-callback'),
]
