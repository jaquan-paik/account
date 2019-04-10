from django.urls import path
from apps.domains.oauth2.views import AuthorizationView, TokenView

app_name = 'oauth2_app'

urlpatterns = [
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('token/', TokenView.as_view(), name='token'),
]
