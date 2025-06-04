# conceptos_nomina/signals.py

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from empresas.models import Empresa
from .models import ConceptoNomina
from .services.conceptos_por_defecto import CONCEPTOS_POR_DEFECTO

@receiver(post_save, sender=Empresa)
def crear_conceptos_por_defecto(sender, instance, created, **kwargs):
    if created:
        for concepto in CONCEPTOS_POR_DEFECTO:
            ConceptoNomina.objects.create(empresa=instance, **concepto)

@receiver(pre_delete, sender=Empresa)
def eliminar_conceptos_empresa(sender, instance, **kwargs):
    ConceptoNomina.objects.filter(empresa=instance).delete()
