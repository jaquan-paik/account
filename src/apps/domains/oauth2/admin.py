from django.contrib import admin
from oauth2_provider.models import get_application_model, get_refresh_token_model, get_access_token_model, get_grant_model


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'client_type', 'authorization_grant_type')
    list_filter = ('client_type', 'authorization_grant_type', 'skip_authorization')
    radio_fields = {
        'client_type': admin.HORIZONTAL,
        'authorization_grant_type': admin.VERTICAL,
    }
    raw_id_fields = ('user', )


class GrantAdmin(admin.ModelAdmin):
    list_display = ('code', 'application', 'user', 'expires')
    raw_id_fields = ('user', )


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'application', 'expires')
    raw_id_fields = ('user', )


class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'application')
    raw_id_fields = ('user', )


Application = get_application_model()
Grant = get_grant_model()
AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()

admin.site.unregister(Application)
admin.site.register(Application, ApplicationAdmin)
admin.site.unregister(Grant)
admin.site.register(Grant, GrantAdmin)
admin.site.unregister(AccessToken)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.unregister(RefreshToken)
admin.site.register(RefreshToken, RefreshTokenAdmin)
