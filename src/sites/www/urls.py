from django.urls import include, path

from apps.domains.account import urls as account_urls
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/', include(account_urls, namespace='account')),
]
