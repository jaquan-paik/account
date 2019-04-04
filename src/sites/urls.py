from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from apps.domains.account import urls as account_urls
from apps.domains.oauth2 import urls as oauth2_urls
from apps.domains.ridi import urls as ridi_urls
from apps.domains.sso import urls as sso_urls
from .views import Index, script_serve


handler400 = 'sites.views.bad_request'
handler403 = 'sites.views.permission_denied'
handler404 = 'sites.views.page_not_found'
handler500 = 'sites.views.server_error'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('accounts/', include(account_urls, namespace='account')),
    path('ridi/', include(ridi_urls, namespace='ridi')),
    path('oauth2/', include(oauth2_urls, namespace='oauth2_provider')),  # namespace 를 라이브러리에서 사용되고 있기 때문에 해당 이름을 사용한다.
    path('sso/', include(sso_urls, namespace='sso')),

    re_path(r'^script/(?P<path>.*)$', script_serve, kwargs={'document_root': settings.STATIC_ROOT + '/script'}),
]


if settings.DEBUG:
    from lib.base.custom_schema_view import CustomSchemaView
    import debug_toolbar
    debug_urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('docs/swagger/', CustomSchemaView.with_ui('swagger', cache_timeout=10), name='schemas-swagger-ui'),
        path('docs/swagger.yaml', CustomSchemaView.without_ui(cache_timeout=10), name='schemas-swagger-without-ui'),
        path('docs/redoc/', CustomSchemaView.with_ui('redoc', cache_timeout=10), name='schemas-redoc'),
    ]
    urlpatterns = debug_urlpatterns + urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
