from django.contrib import admin
from oauth2_provider.models import get_refresh_token_model

RefreshToken = get_refresh_token_model()
admin.site.unregister(RefreshToken)
