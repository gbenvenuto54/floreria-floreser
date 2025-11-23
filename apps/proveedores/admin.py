from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("empresa", "contacto", "correo", "telefono")
    search_fields = ("empresa", "contacto", "correo")
