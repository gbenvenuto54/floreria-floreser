from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from apps.usuarios.decorators import role_required
from .models import Notificacion


@role_required('Administrador', 'Empleado')
def enviar_pendientes(request):
    # Stub: aquí se integraría con la API real de WhatsApp
    pendientes = Notificacion.objects.filter(canal='WhatsApp', estado='pendiente')
    count = 0
    for n in pendientes:
        # Simular envío exitoso
        n.estado = 'enviado'
        n.fecha_envio = timezone.now()
        n.save(update_fields=['estado', 'fecha_envio'])
        count += 1
    if count:
        messages.success(request, f'{count} notificaciones enviadas.')
    else:
        messages.info(request, 'No hay notificaciones pendientes.')
    # Volver a la página anterior si es posible
    return redirect(request.META.get('HTTP_REFERER', 'index'))
