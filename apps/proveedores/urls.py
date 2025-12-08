from django.urls import path
from .views import gestion_lista, proveedor_crear, proveedor_editar, proveedor_eliminar, registrar_entrega

app_name = 'proveedores'

urlpatterns = [
    path('gestion/', gestion_lista, name='gestion_lista'),
    path('nuevo/', proveedor_crear, name='crear'),
    path('<int:pk>/editar/', proveedor_editar, name='editar'),
    path('<int:pk>/eliminar/', proveedor_eliminar, name='eliminar'),
    path('<int:pk>/entrega/', registrar_entrega, name='registrar_entrega'),
]
