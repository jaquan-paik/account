from django.urls import path

from . import views

app_name = 'callback_app'

urlpatterns = [
    path('', views.CallbackView.as_view(), name='callback'),
    path('login/', views.LoginView.as_view(), name='login'),
]
