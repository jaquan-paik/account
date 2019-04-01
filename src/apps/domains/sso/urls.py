from django.urls import path

from apps.domains.sso import views

app_name = 'sso_app'

urlpatterns = [
    path('token/generate/', views.GenerateSSOTokenView.as_view(), name='sso_token_generate'),
    path('token/verify/', views.GenerateSSOTokenView.as_view(), name='sso_token_generate'),
    path('login/', views.SSOLoginView.as_view(), name='sso_login_view'),
]
