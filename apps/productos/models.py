from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Producto(models.Model):
    class Categoria(models.TextChoices):
        AMOR_ANIVERSARIO = 'Amor y Aniversario', 'Amor y Aniversario'
        CUMPLEANOS = 'Cumpleaños', 'Cumpleaños'
        AGRADECIMIENTO = 'Agradecimiento', 'Agradecimiento'
        CONDOLENCIAS = 'Condolencias', 'Condolencias'

    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, choices=Categoria.choices)
    precio = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    stock_minimo = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"


class Review(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="reseñas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reseñas", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    comentario = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.producto} - {self.rating} estrellas"


class MovimientoInventario(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = 'entrada', 'entrada'
        SALIDA = 'salida', 'salida'

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    motivo = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} {self.cantidad} de {self.producto}"
