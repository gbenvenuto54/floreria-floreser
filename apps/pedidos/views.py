from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from apps.productos.models import Producto, MovimientoInventario
from apps.clientes.models import Cliente
from .models import Pedido, PedidoItem
from apps.notificaciones.models import Notificacion
from apps.usuarios.decorators import role_required
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

IVA_RATE = Decimal('0.19')


def _get_cart(session):
    return session.setdefault('cart', {})


def _clp_fmt(value: int) -> str:
    s = f"{int(value):,}".replace(",", ".")
    return f"$ {s}"


def carrito_detalle(request):
    cart = _get_cart(request.session)
    producto_ids = [int(pid) for pid in cart.keys()]
    productos = {p.id: p for p in Producto.objects.filter(id__in=producto_ids)}
    items = []
    subtotal = 0
    for pid, qty in cart.items():
        p = productos.get(int(pid))
        if not p:
            continue
        cantidad = int(qty)
        line_total = int(p.precio) * cantidad
        items.append({
            'producto': p,
            'cantidad': cantidad,
            'precio': int(p.precio),
            'total': line_total,
        })
        subtotal += line_total
    iva = int(subtotal * IVA_RATE)
    total = subtotal + iva
    context = {
        'items': items,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'fmt': _clp_fmt,
    }
    return render(request, 'pedidos/carrito.html', context)


def carrito_agregar(request, producto_id: int):
    producto = get_object_or_404(Producto, pk=producto_id)
    cart = _get_cart(request.session)
    qty = int(request.POST.get('cantidad', '1'))
    if qty < 1:
        qty = 1
    # Validación de stock: no permitir más que stock disponible
    nueva_cantidad = int(cart.get(str(producto.id), 0)) + qty
    if nueva_cantidad > producto.stock:
        messages.error(request, 'No hay stock suficiente para agregar esa cantidad.')
        return redirect('pedidos:carrito')
    cart[str(producto.id)] = nueva_cantidad
    request.session.modified = True
    messages.success(request, 'Producto agregado al carrito.')
    return redirect('pedidos:carrito')


def carrito_eliminar(request, producto_id: int):
    cart = _get_cart(request.session)
    cart.pop(str(producto_id), None)
    request.session.modified = True
    messages.info(request, 'Producto eliminado del carrito.')
    return redirect('pedidos:carrito')


def carrito_actualizar(request, producto_id: int):
    producto = get_object_or_404(Producto, pk=producto_id)
    cart = _get_cart(request.session)
    qty = int(request.POST.get('cantidad', '1'))
    if qty < 1:
        qty = 1
    if qty > producto.stock:
        messages.error(request, 'No hay stock suficiente para esa cantidad.')
        return redirect('pedidos:carrito')
    cart[str(producto.id)] = qty
    request.session.modified = True
    messages.success(request, 'Cantidad actualizada.')
    return redirect('pedidos:carrito')


@login_required
def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        messages.error(request, 'El carrito está vacío.')
        return redirect('pedidos:carrito')

    cliente = getattr(request.user, 'perfil_cliente', None)
    if not cliente:
        messages.error(request, 'Debes tener perfil de cliente para continuar.')
        return redirect('pedidos:carrito')

    # Resumen
    producto_ids = [int(pid) for pid in cart.keys()]
    productos = {p.id: p for p in Producto.objects.filter(id__in=producto_ids)}
    items = []
    subtotal = 0
    for pid, qty in cart.items():
        p = productos.get(int(pid))
        cantidad = int(qty)
        line_total = int(p.precio) * cantidad
        items.append((p, cantidad, line_total))
        subtotal += line_total
    iva = int(subtotal * IVA_RATE)
    total = subtotal + iva

    if request.method == 'POST':
        direccion = request.POST.get('direccion', cliente.direccion)
        comuna = request.POST.get('comuna', cliente.comuna)
        metodo_pago = request.POST.get('metodo_pago', 'Efectivo')
        referencia_pago = request.POST.get('referencia_pago', '').strip()

        # Validación de stock al confirmar
        for p, cantidad, _ in items:
            if cantidad > p.stock:
                messages.error(request, f'Sin stock suficiente para {p.nombre}.')
                return redirect('pedidos:carrito')

        # Validar método de pago permitido
        metodos_permitidos = {'Tarjeta', 'Débito', 'Transferencia', 'Efectivo'}
        if metodo_pago not in metodos_permitidos:
            messages.error(request, 'Método de pago inválido.')
            return render(request, 'pedidos/checkout.html', {
                'items': items,
                'subtotal': subtotal,
                'iva': iva,
                'total': total,
                'fmt': _clp_fmt,
                'cliente': cliente,
            })

        # Validación adicional por método de pago
        if metodo_pago == 'Transferencia' and not referencia_pago:
            messages.error(request, 'Debes ingresar la referencia/comprobante de la transferencia.')
            return render(request, 'pedidos/checkout.html', {
                'items': items,
                'subtotal': subtotal,
                'iva': iva,
                'total': total,
                'fmt': _clp_fmt,
                'cliente': cliente,
            })

        pedido = Pedido.objects.create(
            cliente=cliente,
            subtotal=subtotal,
            iva=iva,
            total=total,
            metodo_pago=metodo_pago,
            referencia_pago=referencia_pago,
            direccion_entrega=f"{direccion}, {comuna}",
        )
        # Adjuntar comprobante si corresponde
        if metodo_pago == 'Transferencia' and request.FILES.get('comprobante_pago'):
            pedido.comprobante_pago = request.FILES['comprobante_pago']
            pedido.save(update_fields=['comprobante_pago'])
        for p, cantidad, _ in items:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=p,
                cantidad=cantidad,
                precio_unitario=p.precio,
            )
            # Disminuir stock y registrar movimiento
            p.stock = int(p.stock) - int(cantidad)
            p.save(update_fields=['stock'])
            MovimientoInventario.objects.create(
                producto=p,
                tipo=MovimientoInventario.Tipo.SALIDA,
                cantidad=cantidad,
                motivo=f'Pedido #{pedido.id}',
            )

        # Crear notificación pendiente (WhatsApp)
        Notificacion.objects.create(
            pedido=pedido,
            canal='WhatsApp',
            estado='pendiente',
        )

        # Para pagos con Tarjeta/Débito, generar además notificación por Email para enlace de pago
        if metodo_pago in ('Tarjeta', 'Débito'):
            Notificacion.objects.create(
                pedido=pedido,
                canal='Email',
                estado='pendiente',
            )

        # Enviar email informativo al cliente (si tiene email)
        destinatario = getattr(getattr(cliente, 'usuario', None), 'email', '')
        if destinatario:
            try:
                asunto = f"Confirmación pedido #{pedido.id} - {metodo_pago}"
                if metodo_pago == 'Transferencia':
                    cuerpo = (
                        f"Hola {cliente.nombre},\n\n"
                        f"Hemos recibido tu pedido #{pedido.id} por un total de {_clp_fmt(int(total))}.\n"
                        "Seleccionaste Transferencia bancaria. Realiza la transferencia a:\n"
                        "Banco Ejemplo, CTA 12-345678-9, RUT 12.345.678-9, Email pagos@floreser.cl.\n"
                        f"Referencia proporcionada: {referencia_pago or '-'}\n\n"
                        "Una vez verificado el pago, prepararemos tu pedido.\n\n"
                        "Gracias por tu compra."
                    )
                elif metodo_pago in ('Tarjeta', 'Débito'):
                    cuerpo = (
                        f"Hola {cliente.nombre},\n\n"
                        f"Hemos recibido tu pedido #{pedido.id} por un total de {_clp_fmt(int(total))}.\n"
                        "Te enviaremos un enlace de pago seguro o podrás pagar al momento de la entrega.\n\n"
                        "Gracias por tu compra."
                    )
                else:  # Efectivo
                    cuerpo = (
                        f"Hola {cliente.nombre},\n\n"
                        f"Hemos recibido tu pedido #{pedido.id} por un total de {_clp_fmt(int(total))}.\n"
                        "Pagarás en efectivo al momento de la entrega.\n\n"
                        "Gracias por tu compra."
                    )
                send_mail(asunto, cuerpo, settings.DEFAULT_FROM_EMAIL, [destinatario], fail_silently=True)
            except Exception:
                # No interrumpir el flujo por error de email en desarrollo
                pass

        # Limpiar carrito
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, 'Pedido confirmado correctamente.')
        return redirect('pedidos:comprobante_pdf', pedido_id=pedido.id)

    return render(request, 'pedidos/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'fmt': _clp_fmt,
        'cliente': cliente,
    })


@login_required
def confirmar_pedido(request):
    # Endpoint placeholder si se requiere separación del POST de checkout
    return redirect('pedidos:checkout')


@login_required
def comprobante_pdf(request, pedido_id: int):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="comprobante_pedido_{pedido_id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 20 * mm
    p.setFont("Helvetica-Bold", 14)
    p.drawString(20 * mm, y, "Florería FloreSer.cl - Comprobante")
    y -= 10 * mm
    p.setFont("Helvetica", 10)
    p.drawString(20 * mm, y, f"Pedido #{pedido.id} - Fecha: {pedido.fecha_pedido.strftime('%d-%m-%Y %H:%M')}")
    y -= 6 * mm
    p.drawString(20 * mm, y, f"Cliente: {pedido.cliente.nombre} | RUT: {pedido.cliente.rut}")
    y -= 10 * mm

    p.setFont("Helvetica-Bold", 10)
    p.drawString(20 * mm, y, "Producto")
    p.drawString(120 * mm, y, "Cant.")
    p.drawString(140 * mm, y, "Precio")
    p.drawString(170 * mm, y, "Total")
    y -= 6 * mm
    p.setFont("Helvetica", 10)

    for item in pedido.items.select_related('producto').all():
        p.drawString(20 * mm, y, f"{item.producto.nombre}")
        p.drawRightString(135 * mm, y, f"{item.cantidad}")
        p.drawRightString(165 * mm, y, _clp_fmt(item.precio_unitario))
        p.drawRightString(200 * mm, y, _clp_fmt(int(item.precio_unitario) * int(item.cantidad)))
        y -= 6 * mm
        if y < 30 * mm:
            p.showPage()
            y = height - 20 * mm

    y -= 10 * mm
    p.setFont("Helvetica-Bold", 10)
    p.drawRightString(165 * mm, y, "Subtotal:")
    p.drawRightString(200 * mm, y, _clp_fmt(int(pedido.subtotal)))
    y -= 6 * mm
    p.drawRightString(165 * mm, y, "IVA 19%:")
    p.drawRightString(200 * mm, y, _clp_fmt(int(pedido.iva)))
    y -= 6 * mm
    p.drawRightString(165 * mm, y, "Total:")
    p.drawRightString(200 * mm, y, _clp_fmt(int(pedido.total)))

    p.showPage()
    p.save()
    return response


@role_required('Administrador', 'Empleado')
def gestion_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').order_by('-fecha_pedido')
    estados = [e[0] for e in Pedido.ESTADOS]
    return render(request, 'pedidos/gestion.html', {
        'pedidos': pedidos,
        'estados': estados,
        'fmt': _clp_fmt,
    })


@role_required('Administrador', 'Empleado')
def pedido_cambiar_estado(request, pedido_id: int):
    if request.method != 'POST':
        return redirect('pedidos:gestion')
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    nuevo = request.POST.get('estado')
    estados_validos = [e[0] for e in Pedido.ESTADOS]
    if nuevo not in estados_validos:
        messages.error(request, 'Estado inválido.')
        return redirect('pedidos:gestion')
    pedido.estado = nuevo
    pedido.save(update_fields=['estado'])
    messages.success(request, f'Estado del pedido #{pedido.id} actualizado a {nuevo}.')
    return redirect('pedidos:gestion')


@role_required('Administrador', 'Empleado')
def pedido_detalle(request, pedido_id: int):
    pedido = get_object_or_404(Pedido.objects.select_related('cliente'), pk=pedido_id)
    items = list(pedido.items.select_related('producto').all())
    items_info = [
        {
            'item': it,
            'line_total': int(it.precio_unitario) * int(it.cantidad),
        }
        for it in items
    ]
    return render(request, 'pedidos/detalle.html', {
        'pedido': pedido,
        'items_info': items_info,
        'fmt': _clp_fmt,
    })
