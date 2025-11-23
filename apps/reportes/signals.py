from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import AuditLog
from apps.usuarios.middleware import get_current_user, get_current_ip
from apps.productos.models import Producto, MovimientoInventario
from apps.pedidos.models import Pedido, PedidoItem
from apps.proveedores.models import Proveedor


def _make_detail(instance):
    try:
        data = model_to_dict(instance)
    except Exception:
        data = {}
    # Limitar tamaño del detalle
    return str(data)[:2000]


def _log(action: str, instance, object_id: str):
    user = get_current_user()
    ip = get_current_ip()
    AuditLog.objects.create(
        user=user if getattr(user, 'is_authenticated', False) else None,
        ip=ip,
        action=action,
        model=instance.__class__.__name__,
        object_id=str(object_id),
        detail=_make_detail(instance),
    )


@receiver(post_save, sender=Producto)
def producto_saved(sender, instance: Producto, created, **kwargs):
    _log('create' if created else 'update', instance, instance.pk)


@receiver(post_delete, sender=Producto)
def producto_deleted(sender, instance: Producto, **kwargs):
    _log('delete', instance, instance.pk)


@receiver(post_save, sender=MovimientoInventario)
def movinv_saved(sender, instance: MovimientoInventario, created, **kwargs):
    _log('create' if created else 'update', instance, instance.pk)


@receiver(post_delete, sender=MovimientoInventario)
def movinv_deleted(sender, instance: MovimientoInventario, **kwargs):
    _log('delete', instance, instance.pk)


@receiver(post_save, sender=Pedido)
def pedido_saved(sender, instance: Pedido, created, **kwargs):
    _log('create' if created else 'update', instance, instance.pk)


@receiver(post_delete, sender=Pedido)
def pedido_deleted(sender, instance: Pedido, **kwargs):
    _log('delete', instance, instance.pk)


@receiver(post_save, sender=PedidoItem)
def pedidoitem_saved(sender, instance: PedidoItem, created, **kwargs):
    _log('create' if created else 'update', instance, instance.pk)


@receiver(post_delete, sender=PedidoItem)
def pedidoitem_deleted(sender, instance: PedidoItem, **kwargs):
    _log('delete', instance, instance.pk)


@receiver(post_save, sender=Proveedor)
def proveedor_saved(sender, instance: Proveedor, created, **kwargs):
    _log('create' if created else 'update', instance, instance.pk)


@receiver(post_delete, sender=Proveedor)
def proveedor_deleted(sender, instance: Proveedor, **kwargs):
    _log('delete', instance, instance.pk)
