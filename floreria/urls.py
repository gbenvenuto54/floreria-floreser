from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from apps.usuarios.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de autenticación (sin namespace para compatibilidad con Django)
    path('cuenta/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cuenta/logout/', auth_views.LogoutView.as_view(next_page='home:index'), name='logout'),
    path('cuenta/registro/', signup, name='signup'),
    path('cuenta/password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('cuenta/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('cuenta/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('cuenta/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    # Apps principales
    path('', include('apps.home.urls', namespace='home')),

    # Compatibilidad con enlaces antiguos
    path('usuarios/login/', RedirectView.as_view(pattern_name='login', permanent=False)),
    
    # Otras apps
    path('clientes/', include('apps.clientes.urls', namespace='clientes')),
    path('productos/', include('apps.productos.urls', namespace='productos')),
    path('pedidos/', include('apps.pedidos.urls', namespace='pedidos')),
    path('reportes/', include('apps.reportes.urls', namespace='reportes')),
    # path('carrito/', include('apps.carrito.urls', namespace='carrito')),
]

# Servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)