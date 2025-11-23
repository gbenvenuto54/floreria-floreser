from django.urls import path
from .views import InicioView, enviar_contacto, faq, testimonios_lista, sobre_nosotros
from django.views.generic import RedirectView

app_name = 'home'  # Define el namespace de la aplicación

urlpatterns = [
    path('', InicioView.as_view(), name='index'),
    path('sobre-nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('enviar-contacto/', enviar_contacto, name='enviar_contacto'),
    path('faq/', faq, name='faq'),
    path('testimonios/', testimonios_lista, name='testimonios'),
]