from django.contrib import admin

from lib.django.admin.base_admin import BaseModelAdmin
from .models import EmailBlacklist


@admin.register(EmailBlacklist)
class EmailBlacklistAdmin(BaseModelAdmin):
    list_display = ('email', 'is_active', 'created', 'last_modified')
    readonly_fields = ('created', 'last_modified',)
    list_filter = ('is_active', )
    search_fields = ('email', )
