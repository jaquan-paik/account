from django.urls import include, path

from sites.www.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
