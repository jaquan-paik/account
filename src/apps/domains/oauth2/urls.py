from django.urls import path
from oauth2_provider.views import TokenView
from apps.domains.oauth2.views import AuthorizeView

app_name = 'oauth2_app'

urlpatterns = [
    path('authorize/', AuthorizeView.as_view(), name='authorize'),
    path('token/', TokenView.as_view(), name='token'),
]
