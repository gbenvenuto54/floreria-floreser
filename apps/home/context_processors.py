from django.apps import apps
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist

def configuracion_context(request):
    default_config = {
        "nombre_sitio": "Florería FloreSer",
        "logo": None,
        "favicon": None,
        "telefono": "",
        "email": "",
        "direccion": "",
        "horario_atencion": "",
        "facebook_url": "#",
        "instagram_url": "#",
        "whatsapp_numero": ""
    }
    
    try:
        Config = apps.get_model('home', 'Config')
        cfg = Config.objects.first()
        
        if cfg:
            return {
                'config': {
                    'nombre_sitio': cfg.nombre_sitio,
                    'logo': cfg.logo,
                    'favicon': cfg.favicon,
                    'telefono': cfg.telefono,
                    'email': cfg.email,
                    'direccion': cfg.direccion,
                    'horario_atencion': cfg.horario_atencion,
                    'facebook_url': cfg.facebook_url,
                    'instagram_url': cfg.instagram_url,
                    'whatsapp_numero': cfg.whatsapp_numero,
                }
            }
    except (OperationalError, ProgrammingError, LookupError, ObjectDoesNotExist) as e:
        # Si hay algún error, devolvemos la configuración por defecto
        pass
        
    return {'config': default_config}
