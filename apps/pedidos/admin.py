from django.contrib import admin
from .models import Pedido, PedidoItem
from django.utils.html import format_html


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "fecha_pedido", "estado", "total", "metodo_pago", "referencia_pago", "comprobante_link")
    list_filter = ("estado", "fecha_pedido")
    date_hierarchy = "fecha_pedido"
    inlines = [PedidoItemInline]
    search_fields = ("id", "cliente__nombre", "estado")

    def comprobante_link(self, obj):
        if getattr(obj, 'comprobante_pago', None):
            url = obj.comprobante_pago.url
            return format_html('<a href="{}" target="_blank">Ver comprobante</a>', url)
        return "—"
    comprobante_link.short_description = "Comprobante"


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ("pedido", "producto", "cantidad", "precio_unitario")
    autocomplete_fields = ("producto", "pedido")
