from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Cliente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil_cliente')
    nombre = models.CharField(max_length=150)
    rut = models.CharField(
        max_length=12,
        validators=[RegexValidator(r"^\d{7,8}-[\dkK]$", message="RUT inválido. Formato: XXXXXXXX-X")],
        unique=True,
    )
    direccion = models.CharField(max_length=255, blank=True)
    comuna = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.rut}"
