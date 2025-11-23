from django.db import models
from django.conf import settings


class Proveedor(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_proveedor')
    empresa = models.CharField(max_length=150)
    contacto = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.empresa
