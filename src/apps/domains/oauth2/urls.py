from django.urls import path
from oauth2_provider.views import TokenView
from apps.domains.oauth2.views import AuthorizationView

app_name = 'oauth2_app'

urlpatterns = [
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('token/', TokenView.as_view(), name='token'),
]
