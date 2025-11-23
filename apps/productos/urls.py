from django.urls import path
from .views import lista_productos, gestion_lista, producto_crear, producto_editar, producto_eliminar

app_name = 'productos'

urlpatterns = [
    path('', lista_productos, name='lista'),
    path('gestion/', gestion_lista, name='gestion_lista'),
    path('nuevo/', producto_crear, name='crear'),
    path('<int:pk>/editar/', producto_editar, name='editar'),
    path('<int:pk>/eliminar/', producto_eliminar, name='eliminar'),
]
