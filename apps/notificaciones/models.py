from django.db import models
from apps.pedidos.models import Pedido


class Notificacion(models.Model):
    CANALES = [
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'Email'),
    ]
    ESTADOS = [
        ('pendiente', 'pendiente'),
        ('enviado', 'enviado'),
        ('error', 'error'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    canal = models.CharField(max_length=20, choices=CANALES)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_envio = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.canal} - {self.pedido} ({self.estado})"
