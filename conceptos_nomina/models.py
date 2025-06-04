from django.db import models
from empresas.models import Empresa  # Ajusta según tu proyecto

class ConceptoNomina(models.Model):
    TIPO_CHOICES = [
        ('DEVENGADO', 'Devengado'),
        ('DEDUCCION', 'Deducción'),
        ('PROVISION', 'Provisión'),
        ('INFORMATIVO', 'Informativo'),
        ('PARAFISCALES', 'Parafiscales'),
    ]

    FORMA_CALCULO_CHOICES = [
        ('FIJO', 'Valor fijo'),
        ('FORMULA', 'Fórmula'),
        ('MANUAL', 'Valor manual'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='conceptos')
    codigo = models.CharField(max_length=30, help_text="Código único del concepto", unique=False)
    nombre = models.CharField(max_length=100, help_text="Nombre del concepto")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, help_text="Tipo de concepto")
    forma_calculo = models.CharField(max_length=20, choices=FORMA_CALCULO_CHOICES, help_text="Forma en la que se calcula")
    formula = models.TextField(blank=True, help_text="Fórmula en caso de que aplique")
    es_base_cotizacion = models.BooleanField(default=False, help_text="¿Hace parte de la base de cotización?")
    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conceptos_nomina'
        unique_together = ('empresa', 'codigo')
        verbose_name = 'Concepto de Nómina'
        verbose_name_plural = 'Conceptos de Nómina'
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.empresa.nombre})"

