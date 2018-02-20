from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 20

    def get_actions(self, request):
        # Disable delete
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request) -> bool:
        # Disable add
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        # Disable delete
        return False


class BasePrefetchModelAdmin(BaseModelAdmin):
    # inner join 제거를위해 req를 나누어서 하도록함
    list_select_related = ()
    list_prefetch_related = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(self.list_prefetch_related)
