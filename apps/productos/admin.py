from django.contrib import admin
from .models import Producto, MovimientoInventario, Review


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("sku", "nombre", "categoria", "precio", "stock", "stock_minimo", "destacado")
    search_fields = ("sku", "nombre", "categoria")
    list_filter = ("categoria", "destacado")
    list_editable = ("destacado",)


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo", "cantidad", "fecha", "motivo")
    list_filter = ("tipo", "fecha")
    autocomplete_fields = ("producto",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("producto", "usuario", "rating", "aprobado", "creado_en")
    list_filter = ("aprobado", "rating", "producto")
    search_fields = ("producto__nombre", "usuario__username", "comentario")
    autocomplete_fields = ("producto", "usuario")
