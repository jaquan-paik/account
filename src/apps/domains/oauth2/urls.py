from django.urls import path
from oauth2_provider import views

app_name = 'oauth2_app'

urlpatterns = [
    path('authorize/', views.AuthorizationView.as_view(), name="authorize"),
    path('token/', views.TokenView.as_view(), name="token"),
]
