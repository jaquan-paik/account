from django.conf import settings
from django.urls import include, path

from apps.domains.account import urls as account_urls
from apps.domains.oauth2 import urls as oauth2_urls
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/', include(account_urls, namespace='account')),
    path('oauth2/', include(oauth2_urls, namespace='oauth2_provider')),  # namespace 를 라이브러리에서 사용되고 있기 때문에 해당 이름을 사용한다.
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
