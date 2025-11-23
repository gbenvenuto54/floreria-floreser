from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("pedido", "canal", "estado", "fecha_envio")
    list_filter = ("canal", "estado")
    date_hierarchy = "fecha_envio"
