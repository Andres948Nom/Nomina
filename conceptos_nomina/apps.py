from django.apps import AppConfig


class ConceptosNominaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conceptos_nomina'

    def ready(self):
        import conceptos_nomina.signals
