from django.contrib import admin

from lib.django.admin.base_admin import BaseModelAdmin
from .models import AdminUrlAccessHistory


class AdminUrlAccessHistoryAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {'fields': ('staff_id', 'url', )}),
        ('날짜 정보', {'fields': ('created', 'last_modified',)}),
    )

    readonly_fields = ('id', 'staff_id', 'url', 'created', 'last_modified', )
    list_display = ('id', 'staff_id', 'url', 'created', )

    ordering = ['-id', ]
    search_fields = ['staff_id', 'url', ]


admin.site.register(AdminUrlAccessHistory, AdminUrlAccessHistoryAdmin)
