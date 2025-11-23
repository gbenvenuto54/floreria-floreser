from django.contrib import admin
from .models import Empleado


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cargo", "telefono", "fecha_ingreso")
    search_fields = ("usuario__username", "cargo")
