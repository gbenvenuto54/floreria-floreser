from django.views.generic import TemplateView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Config, SeccionInicio, Testimonio, Contacto
from apps.productos.models import Producto


class InicioView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Obtener la configuración del sitio
            configuracion = Config.objects.first()
            
            # Obtener banners activos
            banners = SeccionInicio.objects.filter(
                activo=True, 
                tipo='banner'
            ).order_by('orden')
            
            # Obtener productos destacados desde Producto
            productos_destacados = Producto.objects.filter(destacado=True)[:8]

            # Tiles de "Comprar por Ocación"
            categorias_objetivo = [
                ("Amor y Aniversario", "Amor y Aniversario"),
                ("Cumpleaños", "Cumple"),
                ("Agradecimiento", "Agrade"),
                ("Condolencias", "Condol"),
            ]
            ocasion_tiles = []
            for titulo, patron in categorias_objetivo:
                prod = (
                    Producto.objects
                    .filter(
                        Q(categoria__icontains=patron) | Q(categoria__icontains=titulo),
                        imagen__isnull=False
                    )
                    .exclude(imagen="")
                    .first()
                )
                imagen_url = prod.imagen.url if prod and getattr(prod, 'imagen', None) else None
                ocasion_tiles.append({
                    'titulo': titulo,
                    'categoria': patron,
                    'imagen_url': imagen_url,
                })

            # Obtener testimonios activos
            testimonios = Testimonio.objects.filter(activo=True).order_by('-fecha_creacion')

            context.update({
                'configuracion': configuracion,
                'banners': banners if banners.exists() else [],
                'productos_destacados': list(productos_destacados),
                'ocasion_tiles': ocasion_tiles,
                'testimonios': list(testimonios) if testimonios.exists() else [],
            })
            
        except Exception as e:
            # En caso de error, devolver contextos vacíos
            context.update({
                'configuracion': None,
                'banners': [],
                'productos_destacados': [],
                'testimonios': [],
            })
        
        return context

def faq(request):
    """Página de Preguntas Frecuentes."""
    configuracion = Config.objects.first()
    return render(request, "home/faq.html", {"configuracion": configuracion})


def sobre_nosotros(request):
    """Página independiente Sobre Nosotros."""
    configuracion = Config.objects.first()
    return render(request, "home/sobre_nosotros.html", {"configuracion": configuracion})


def testimonios_lista(request):
    """Página independiente con todos los testimonios activos."""
    configuracion = Config.objects.first()
    testimonios = Testimonio.objects.filter(activo=True).order_by('-fecha_creacion')
    return render(request, "home/testimonios.html", {
        "configuracion": configuracion,
        "testimonios": testimonios,
    })


@require_POST
def enviar_contacto(request):
    nombre = request.POST.get('nombre', '').strip()
    email = request.POST.get('email', '').strip()
    mensaje = request.POST.get('mensaje', '').strip()
    if nombre and email and mensaje:
        # Guardar el mensaje en el modelo Contacto
        Contacto.objects.create(nombre=nombre, email=email, mensaje=mensaje)
        messages.success(request, 'Gracias por tu mensaje. Te contactaremos pronto.')
    else:
        messages.error(request, 'Por favor completa todos los campos.')
    return redirect('home:index')