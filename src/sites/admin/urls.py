from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    info=openapi.Info(
        title="Bootstrap API", default_version='v1'
    ),
)

urlpatterns = [
    path('', admin.site.urls),

    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schemas-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schemas-redoc'),
]
