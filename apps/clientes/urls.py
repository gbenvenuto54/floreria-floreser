from django.urls import path
from .views import perfil, mis_pedidos

app_name = 'clientes'

urlpatterns = [
    path('perfil/', perfil, name='perfil'),
    path('mis-pedidos/', mis_pedidos, name='mis_pedidos'),
]
