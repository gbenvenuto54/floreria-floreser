from django.apps import AppConfig


class ReportesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reportes'
    verbose_name = 'Reportes'

    def ready(self):
        from . import signals  # noqa: F401
