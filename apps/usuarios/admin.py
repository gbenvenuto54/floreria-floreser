from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y estado', {'fields': ('rol', 'activo')}),
    )
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')

    # Permisos: staff puede ver, solo superusuario puede crear/editar/borrar
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
