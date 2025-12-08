from django.contrib import admin
from django.utils.html import format_html
from .models import SeccionInicio, Testimonio, Config, Contacto


@admin.register(SeccionInicio)
class SeccionInicioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'orden', 'activo', 'preview_imagen')
    list_filter = ('tipo', 'activo')
    search_fields = ('titulo', 'subtitulo', 'contenido')
    list_editable = ('orden', 'activo')
    ordering = ('orden',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'subtitulo', 'contenido', 'tipo')
        }),
        ('Imagen y Enlace', {
            'fields': ('imagen', 'preview_imagen', 'enlace', 'texto_boton')
        }),
        ('Configuración', {
            'fields': ('orden', 'activo')
        }),
    )
    readonly_fields = ('preview_imagen',)

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    preview_imagen.short_description = 'Vista previa'


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'fecha_creacion', 'activo', 'preview_imagen')
    list_filter = ('activo',)
    search_fields = ('nombre', 'cargo', 'contenido')
    list_editable = ('activo',)
    readonly_fields = ('fecha_creacion', 'preview_imagen')
    fieldsets = (
        ('Información del Testimonio', {
            'fields': ('nombre', 'cargo', 'contenido')
        }),
        ('Imagen', {
            'fields': ('imagen', 'preview_imagen')
        }),
        ('Configuración', {
            'fields': ('activo', 'fecha_creacion')
        }),
    )

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    preview_imagen.short_description = 'Vista previa'


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('nombre_sitio', 'telefono', 'email', 'preview_logo')
    search_fields = ('nombre_sitio', 'telefono', 'email', 'direccion')
    readonly_fields = ('preview_logo', 'preview_favicon')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_sitio', 'logo', 'preview_logo', 'favicon', 'preview_favicon')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'email', 'direccion', 'horario_atencion')
        }),
        ('Redes Sociales', {
            'fields': ('facebook_url', 'instagram_url', 'whatsapp_numero')
        }),
        ('Imágenes', {
            'fields': ('alto_imagen_destacado', 'alto_imagen_producto', 'alto_imagen_ocasion')
        }),
    )
    
    def preview_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 100px;" />',
                obj.logo.url
            )
        return "Sin logo"
    preview_logo.short_description = 'Vista previa del logo'
    
    def preview_favicon(self, obj):
        if obj.favicon:
            return format_html(
                '<img src="{}" style="max-height: 32px;" />',
                obj.favicon.url
            )
        return "Sin favicon"
    preview_favicon.short_description = 'Vista previa del favicon'


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "fecha", "leido")
    list_filter = ("leido", "fecha")
    search_fields = ("nombre", "email", "mensaje")
    readonly_fields = ("fecha",)
