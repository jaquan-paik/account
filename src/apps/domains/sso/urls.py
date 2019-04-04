from django.urls import path

from apps.domains.sso import views

app_name = 'sso_app'

urlpatterns = [
    path('otp/', views.GenerateSSOOtpView.as_view(), name='sso_otp_generate'),
    path('otp/verify/', views.VerifySSOOtpView.as_view(), name='sso_otp_verify'),

    path('login/', views.SSOLoginView.as_view(), name='sso_login_view'),
]
