from django.urls import path
from .views import (
    carrito_detalle,
    carrito_agregar,
    carrito_eliminar,
    carrito_actualizar,
    checkout,
    confirmar_pedido,
    comprobante_pdf,
    gestion_pedidos,
    pedido_cambiar_estado,
    pedido_detalle,
)

app_name = 'pedidos'

urlpatterns = [
    path('carrito/', carrito_detalle, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', carrito_agregar, name='carrito_agregar'),
    path('carrito/eliminar/<int:producto_id>/', carrito_eliminar, name='carrito_eliminar'),
    path('carrito/actualizar/<int:producto_id>/', carrito_actualizar, name='carrito_actualizar'),
    path('checkout/', checkout, name='checkout'),
    path('confirmar/', confirmar_pedido, name='confirmar'),
    path('comprobante/<int:pedido_id>/', comprobante_pdf, name='comprobante_pdf'),
    path('gestion/', gestion_pedidos, name='gestion'),
    path('<int:pedido_id>/estado/', pedido_cambiar_estado, name='cambiar_estado'),
    path('<int:pedido_id>/', pedido_detalle, name='detalle'),
]
