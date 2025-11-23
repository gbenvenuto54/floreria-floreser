from django.shortcuts import render
from .models import Producto
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from apps.usuarios.decorators import role_required
from .forms import ProductoForm
from apps.home.models import Config


def lista_productos(request):
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    productos = Producto.objects.all()
    if q:
        productos = productos.filter(nombre__icontains=q)
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)

    configuracion = Config.objects.first()

    return render(request, 'productos/lista.html', {
        'productos': productos,
        'q': q,
        'categoria': categoria,
        'configuracion': configuracion,
    })


@role_required('Administrador', 'Empleado')
def gestion_lista(request):
    q = request.GET.get('q', '').strip()
    productos = Producto.objects.all()
    if q:
        productos = productos.filter(nombre__icontains=q)

    configuracion = Config.objects.first()

    return render(request, 'productos/gestion_lista.html', {
        'productos': productos,
        'q': q,
        'configuracion': configuracion,
    })


@role_required('Administrador', 'Empleado')
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('productos:gestion_lista')
    else:
        form = ProductoForm()

    configuracion = Config.objects.first()

    return render(request, 'productos/form.html', {
        'form': form,
        'titulo': 'Nuevo producto',
        'configuracion': configuracion,
    })


@role_required('Administrador', 'Empleado')
def producto_editar(request, pk: int):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado.')
            return redirect('productos:gestion_lista')
    else:
        form = ProductoForm(instance=producto)

    configuracion = Config.objects.first()

    return render(request, 'productos/form.html', {
        'form': form,
        'titulo': 'Editar producto',
        'configuracion': configuracion,
    })


@role_required('Administrador', 'Empleado')
def producto_eliminar(request, pk: int):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.info(request, 'Producto eliminado.')
        return redirect('productos:gestion_lista')

    configuracion = Config.objects.first()

    return render(request, 'productos/confirmar_eliminar.html', {
        'obj': producto,
        'configuracion': configuracion,
    })
