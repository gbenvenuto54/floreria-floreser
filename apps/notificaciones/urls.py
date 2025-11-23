from django.urls import path
from .views import enviar_pendientes

app_name = 'notificaciones'

urlpatterns = [
    path('enviar-pendientes/', enviar_pendientes, name='enviar_pendientes'),
]
