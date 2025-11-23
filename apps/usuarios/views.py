from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario
from apps.clientes.models import Cliente
from apps.clientes.views import _rut_placeholder_for_user


def index(request):
    return render(request, 'index.html')


class RegistroForm(UserCreationForm):
    """Formulario de registro basado en el modelo de usuario personalizado."""

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "email")


def signup(request):
    """Registro de nuevos usuarios clientes desde la web."""
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.rol = Usuario.Roles.CLIENTE
            usuario.activo = True
            usuario.save()

            # Crear perfil de Cliente asociado con un RUT placeholder válido
            Cliente.objects.create(
                usuario=usuario,
                nombre=usuario.get_full_name() or usuario.username or "Cliente",
                rut=_rut_placeholder_for_user(usuario.id),
                direccion="",
                comuna="",
                telefono="",
            )

            login(request, usuario)
            return redirect("home:index")
    else:
        form = RegistroForm()

    return render(request, "registration/signup.html", {"form": form})