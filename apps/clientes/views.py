from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Cliente
from apps.pedidos.models import Pedido
from apps.usuarios.decorators import role_required


def _rut_dv(num):
    seq = [2, 3, 4, 5, 6, 7]
    s = 0
    m = 0
    for d in str(num)[::-1]:
        s += int(d) * seq[m]
        m = (m + 1) % len(seq)
    r = 11 - (s % 11)
    if r == 11:
        return "0"
    if r == 10:
        return "K"
    return str(r)


def _rut_placeholder_for_user(user_id):
    base = 70000000 + int(user_id or 0)
    dv = _rut_dv(base)
    return f"{base}-{dv}"


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "rut", "direccion", "comuna", "telefono"]


@login_required
def perfil(request):
    cliente, created = Cliente.objects.get_or_create(
        usuario=request.user,
        defaults={
            "nombre": request.user.get_full_name() or request.user.username or "Cliente",
            "rut": _rut_placeholder_for_user(request.user.id),
            "direccion": "",
            "comuna": "",
            "telefono": "",
        },
    )
    if created:
        messages.info(request, "Se ha creado tu perfil de cliente. Actualiza tus datos, por favor.")

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("clientes:perfil")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "clientes/perfil.html", {"form": form})


@login_required
def mis_pedidos(request):
    cliente, _ = Cliente.objects.get_or_create(
        usuario=request.user,
        defaults={
            "nombre": request.user.get_full_name() or request.user.username or "Cliente",
            "rut": _rut_placeholder_for_user(request.user.id),
        },
    )

    pedidos = Pedido.objects.filter(cliente=cliente).order_by("-fecha_pedido")
    return render(request, "clientes/mis_pedidos.html", {"pedidos": pedidos})
