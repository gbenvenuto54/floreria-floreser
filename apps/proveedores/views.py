from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.usuarios.decorators import role_required
from .models import Proveedor
from .forms import ProveedorForm
from apps.productos.models import Producto, MovimientoInventario
from django import forms


class EntregaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(min_value=1)
    motivo = forms.CharField(max_length=255, required=False, initial="Entrega de proveedor")


@role_required('Administrador')
def gestion_lista(request):
    q = request.GET.get('q', '').strip()
    proveedores = Proveedor.objects.select_related('usuario').all()
    if q:
        proveedores = proveedores.filter(empresa__icontains=q)
    return render(request, 'proveedores/gestion_lista.html', {
        'proveedores': proveedores,
        'q': q,
    })


@role_required('Administrador')
def proveedor_crear(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect('proveedores:gestion_lista')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/form.html', {'form': form, 'titulo': 'Nuevo proveedor'})


@role_required('Administrador')
def proveedor_editar(request, pk: int):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado.')
            return redirect('proveedores:gestion_lista')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/form.html', {'form': form, 'titulo': 'Editar proveedor'})


@role_required('Administrador')
def proveedor_eliminar(request, pk: int):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.info(request, 'Proveedor eliminado.')
        return redirect('proveedores:gestion_lista')
    return render(request, 'proveedores/confirmar_eliminar.html', {'obj': proveedor})


@role_required('Administrador')
def registrar_entrega(request, pk: int):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            motivo = form.cleaned_data['motivo']
            # Aumentar stock y registrar movimiento
            producto.stock = int(producto.stock) + int(cantidad)
            producto.save(update_fields=['stock'])
            MovimientoInventario.objects.create(
                producto=producto,
                tipo=MovimientoInventario.Tipo.ENTRADA,
                cantidad=cantidad,
                motivo=f"Entrega de {proveedor.empresa}: {motivo}",
            )
            messages.success(request, 'Entrega registrada y stock actualizado.')
            return redirect('proveedores:gestion_lista')
    else:
        form = EntregaForm()
    return render(request, 'proveedores/entrega_form.html', {'form': form, 'proveedor': proveedor})
