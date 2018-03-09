from django.urls import path

from . import views

app_name = 'callback_app'

urlpatterns = [
    path('callback/', views.CallbackView.as_view(), name='callback'),
    path('authorize/', views.AuthorizeView.as_view(), name='authorize'),
]
