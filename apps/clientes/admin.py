from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "rut", "comuna", "telefono")
    search_fields = ("nombre", "rut", "comuna")

    def has_module_permission(self, request):
        return bool(getattr(request.user, 'is_staff', False))

    def has_view_permission(self, request, obj=None):
        return bool(getattr(request.user, 'is_staff', False))

    def has_add_permission(self, request):
        return bool(getattr(request.user, 'is_superuser', False))

    def has_change_permission(self, request, obj=None):
        return bool(getattr(request.user, 'is_superuser', False))

    def has_delete_permission(self, request, obj=None):
        return bool(getattr(request.user, 'is_superuser', False))
