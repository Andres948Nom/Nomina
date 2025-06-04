from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

from empleados.models import Empleado
from periodo.models import PeriodoNomina
from conceptos_nomina.models import ConceptoNomina

class Liquidacion(models.Model):
    """
    Representa la liquidación completa de un empleado en un período, siempre
    vinculada a la empresa activa (empleado.empresa == periodo.empresa == empresa_activa).
    """
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='liquidaciones'
    )
    periodo = models.ForeignKey(
        PeriodoNomina,
        on_delete=models.CASCADE,
        related_name='liquidaciones'
    )
    empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='liquidaciones'
    )
    fecha_liquidacion = models.DateTimeField(auto_now_add=True)
    total_asignaciones = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deducciones = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_provisiones = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_parafiscales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    neto_pagar = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'liquidaciones_liquidacion'
        unique_together = ('empleado', 'periodo')
        ordering = ['-fecha_liquidacion']
        verbose_name = 'Liquidación'
        verbose_name_plural = 'Liquidaciones'

    def __str__(self):
        return f"Liquidación {self.empleado.nombre_empleado} - {self.periodo.nombre}"

    def clean(self):
        # Validar que empleado, periodo y empresa coincidan con la empresa activa
        if self.empleado.empresa != self.empresa:
            raise ValidationError("El empleado no pertenece a la empresa indicada.")
        if self.periodo.empresa != self.empresa:
            raise ValidationError("El período no pertenece a la empresa indicada.")

class DetalleLiquidacion(models.Model):
    """
    Cada renglón de la liquidación: un concepto aplicado (devengado, deducción, provisión, o informativo).
    Puede venir de una novedad o generarse automáticamente (por ejemplo, Sueldo Devengado).
    """
    TIPOS = [
        ('DEVENGADO', 'Devengado'),
        ('DEDUCCION', 'Deducción'),
        ('PROVISION', 'Provisión'),
        ('INFORMATIVO', 'Informativo'),
    ]

    liquidacion = models.ForeignKey(
        Liquidacion,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    concepto = models.ForeignKey(
        ConceptoNomina,
        on_delete=models.PROTECT
    )
    cantidad = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )
    valor = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )
    # Opcional: si este renglón proviene de una novedad
    novedad = models.ForeignKey(
        'empleados.Novedad',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="Novedad que originó este detalle (si aplica)."
    )

    class Meta:
        db_table = 'liquidaciones_detalle'
        ordering = ['concepto__codigo']
        verbose_name = 'Detalle de Liquidación'
        verbose_name_plural = 'Detalles de Liquidación'

    def __str__(self):
        return f"{self.concepto.codigo} - {self.valor} ({self.tipo})"
