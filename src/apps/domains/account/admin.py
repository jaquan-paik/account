
from datetime import date

from django.contrib import admin
from django.contrib.auth import admin as django_user_admin

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


class StaffAdmin(django_user_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('개인 정보', {'fields': ('email',)}),
        ('상태 정보', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
        ('권한 정보', {'fields': ('groups', 'user_permissions',)}),
        ('관련 날짜', {'fields': ('last_login', 'last_change_password_date', 'created', 'last_modified', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )

    readonly_fields = ('last_login', 'last_change_password_date', 'created', 'last_modified', )
    list_display = (
        'email', 'print_group', 'print_user_permissions', 'is_active', 'is_superuser', 'last_login',
        'print_last_change_password_date',
    )
    list_filter = ('is_active', 'is_superuser', )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def print_group(self, obj) -> str:
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else '지정된 그룹이 없습니다.'
    print_group.short_description = '그룹'

    def print_user_permissions(self, obj) -> str:
        return ','.join(
            [g.name for g in obj.user_permissions.all()]
        ) if obj.user_permissions.count() else '지정된 권한이 없습니다.'
    print_user_permissions.short_description = '권한'

    def print_last_change_password_date(self, obj) -> str:
        today = date.today()
        if obj.last_change_password_date is None:
            return '없음'

        diff = (today - obj.last_change_password_date.date()).days
        return '%s일전' % (diff, )
    print_last_change_password_date.short_description = '마지막 암호 변경일'


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
