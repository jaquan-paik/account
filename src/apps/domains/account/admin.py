
from datetime import date

from django.contrib import admin

from apps.domains.account.models import OAuth2User, Staff, User
from lib.django.admin.base_admin import BaseModelAdmin


class OAuth2UserAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'name',)}),
        ('관련 날짜', {'fields': ('created', 'last_modified',)}),
    )
    readonly_fields = ('id', 'created', 'last_modified',)
    list_display = ('name', 'created', 'last_modified',)

    def has_add_permission(self, request) -> bool:
        return True


class StaffAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {'fields': ('id', 'admin_id',)}),
        ('관련 날짜', {'fields': ('last_login', 'created', 'last_modified',)}),
    )
    readonly_fields = ('id', 'admin_id', 'last_login', 'created', 'last_modified',)
    list_display = ('admin_id', 'print_last_change_password_date', 'created', 'last_modified',)

    def print_last_change_password_date(self, obj) -> str:
        today = date.today()
        if obj.last_change_password_date is None:
            return '없음'

        diff = (today - obj.last_change_password_date.date()).days
        return '%s일전' % (diff, )
    print_last_change_password_date.short_description = '마지막 암호 변경일'

    def has_add_permission(self, request) -> bool:
        return False


class UserAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인 정보', {'fields': ('email',)}),
        ('상태 정보', {'fields': ('is_active',)}),
        ('관련 날짜', {'fields': ('last_login', 'last_change_password_date',)}),
    )


admin.site.register(Staff, StaffAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(OAuth2User, OAuth2UserAdmin)
