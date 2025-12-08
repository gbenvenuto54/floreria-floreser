from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMINISTRADOR = 'Administrador', 'Administrador'
        EMPLEADO = 'Empleado', 'Empleado'
        CLIENTE = 'Cliente', 'Cliente'
        PROVEEDOR = 'Proveedor', 'Proveedor'

    rol = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENTE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
