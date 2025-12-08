from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import transaction


class SeccionInicio(models.Model):
    TIPO_CHOICES = [
        ('banner', 'Banner Principal'),
        ('destacado', 'Producto Destacado'),
        ('testimonio', 'Testimonio'),
    ]

    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, blank=True)
    contenido = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='inicio/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    enlace = models.URLField(blank=True)
    texto_boton = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = _('Sección de Inicio')
        verbose_name_plural = _('Secciones de Inicio')
        ordering = ['orden', 'id']
        app_label = 'home'

    def __str__(self):
        return self.titulo


class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='testimonios/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Testimonio')
        verbose_name_plural = _('Testimonios')
        ordering = ['-fecha_creacion']
        app_label = 'home'

    def __str__(self):
        return f"Testimonio de {self.nombre}"


class Config(models.Model):
    """
    Modelo de configuración del sitio. Forzamos el nombre de tabla a `home_config`
    para que coincida con lo que tu app ya intenta consultar.
    """
    nombre_sitio = models.CharField(max_length=100, default='Florería FloreSer')
    logo = models.ImageField(upload_to='configuracion/', blank=True, null=True)
    favicon = models.ImageField(upload_to='configuracion/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    horario_atencion = models.CharField(max_length=100, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_numero = models.CharField(max_length=20, blank=True)

    # Tamaños globales de imágenes (solo afectan a la presentación, no al archivo almacenado)
    alto_imagen_destacado = models.PositiveIntegerField(
        default=220,
        help_text=_('Altura en píxeles para productos destacados en la página de inicio.'),
    )
    alto_imagen_producto = models.PositiveIntegerField(
        default=220,
        help_text=_('Altura en píxeles para imágenes del catálogo de productos.'),
    )
    alto_imagen_ocasion = models.PositiveIntegerField(
        default=230,
        help_text=_('Altura en píxeles para las tarjetas de "Comprar por Ocación".'),
    )

    class Meta:
        verbose_name = _('Configuración del Sitio')
        verbose_name_plural = _('Configuración del Sitio')
        db_table = 'home_config'   # <- nombre exacto que evita el error
        app_label = 'home'

    def __str__(self):
        return "Configuración del Sitio"

    def save(self, *args, **kwargs):
        """
        Mantener una sola fila (singleton). Hacemos la operación en transacción
        para evitar estados intermedios si hay concurrencia.
        """
        with transaction.atomic():
            if self.pk:
                # Si existe, eliminar las otras
                self.__class__.objects.exclude(pk=self.pk).delete()
            else:
                # Si no existe pk, primero guardar (crea pk) y luego limpiar otras
                super().save(*args, **kwargs)
                self.__class__.objects.exclude(pk=self.pk).delete()
                return
            super().save(*args, **kwargs)


class Contacto(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Mensaje de contacto')
        verbose_name_plural = _('Mensajes de contacto')
        ordering = ['-fecha']
        app_label = 'home'

    def __str__(self):
        return f"Contacto de {self.nombre} ({self.email})"
