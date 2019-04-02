from django.urls import path

from apps.domains.sso import views

app_name = 'sso_app'

urlpatterns = [
    path('otp/generate/', views.GenerateSSOOtpView.as_view(), name='sso_token_generate'),
    path('otp/verify/', views.VerifySSOOtpView.as_view(), name='sso_token_generate'),

    path('login/', views.SSOLoginView.as_view(), name='sso_login_view'),
]
