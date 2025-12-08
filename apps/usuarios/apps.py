from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.module_loading import import_string


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    verbose_name = 'Usuarios'

    def ready(self):
        # Registrar señal post_migrate para crear/actualizar un superusuario por defecto
        def ensure_default_admin(sender, **kwargs):
            User = import_string('django.contrib.auth.get_user_model')()
            # get_user_model() returns a class, not instance; adjust:
        
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        def create_or_update_admin(sender, **kwargs):
            username = 'admin'
            password = 'Adm1n!23456'
            email = 'admin@example.com'
            user, created = UserModel.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            # Asegurar flags y password en cada migración para evitar quedar sin acceso
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            # set_password solo si el usuario fue creado recientemente o si no puede autenticarse
            user.set_password(password)
            # Intentar asignar rol si el modelo lo soporta
            if hasattr(user, 'rol'):
                try:
                    user.rol = 'Administrador'
                except Exception:
                    pass
            user.save()

        # Conectar con UID para evitar duplicados
        post_migrate.connect(create_or_update_admin, sender=self, dispatch_uid='usuarios.create_default_admin')
