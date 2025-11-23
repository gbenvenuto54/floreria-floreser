from django.db import models
from django.conf import settings
from apps.clientes.models import Cliente
from apps.empleados.models import Empleado
from apps.productos.models import Producto


class Pedido(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
        ('En preparación', 'En preparación'),
        ('Entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)
    iva = models.DecimalField(max_digits=12, decimal_places=0)
    total = models.DecimalField(max_digits=12, decimal_places=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    metodo_pago = models.CharField(max_length=50, blank=True)
    referencia_pago = models.CharField(max_length=100, blank=True)
    comprobante_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    direccion_entrega = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=0)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
