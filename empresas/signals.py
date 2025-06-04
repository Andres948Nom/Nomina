from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Empresa, ConfiguracionEmpresa
from empleados.models import Cargo, GrupoNomina

@receiver(post_save, sender=Empresa)
def crear_configuracion_y_valores_por_defecto(sender, instance, created, **kwargs):
    if created:
        # Configuración por defecto
        ConfiguracionEmpresa.objects.create(empresa=instance)

        # Cargos por defecto
        cargos_por_defecto = ['Administrador', 'Contador', 'Asistente', 'Auxiliar', 'Operario']
        for nombre in cargos_por_defecto:
            Cargo.objects.create(empresa=instance, nombre=nombre)

        # Grupos de nómina por defecto
        grupos_por_defecto = ['Administrativo', 'Operativo', 'Temporal']
        for nombre in grupos_por_defecto:
            GrupoNomina.objects.create(empresa=instance, nombre=nombre)
