from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from apps.domains.account import urls as account_urls
from apps.domains.oauth2 import urls as oauth2_urls
from apps.domains.callback import urls as callback_urls
from .views import Index, TokenRefresherView

handler400 = 'sites.www.views.bad_request'
handler403 = 'sites.www.views.permission_denied'
handler404 = 'sites.www.views.page_not_found'
handler500 = 'sites.www.views.server_error'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('token-refresher/', TokenRefresherView.as_view(), name='index'),

    path('accounts/', include(account_urls, namespace='account')),
    path('ridi/', include(callback_urls, namespace='ridi')),
    path('oauth2/', include(oauth2_urls, namespace='oauth2_provider')),  # namespace 를 라이브러리에서 사용되고 있기 때문에 해당 이름을 사용한다.
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
