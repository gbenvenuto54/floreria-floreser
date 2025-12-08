from django.urls import path
from .views import index, reporte_ventas, reporte_stock_bajo, reporte_proveedores_activos, reporte_auditoria

app_name = 'reportes'

urlpatterns = [
    path('', index, name='index'),
    path('ventas/', reporte_ventas, name='ventas'),
    path('stock-bajo/', reporte_stock_bajo, name='stock_bajo'),
    path('proveedores-activos/', reporte_proveedores_activos, name='proveedores_activos'),
    path('auditoria/', reporte_auditoria, name='auditoria'),
]
