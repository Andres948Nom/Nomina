from django.db import models
from empresas.models import Empresa

class PeriodoNomina(models.Model):
    TIPO_CHOICES = (
        ('NOMINA', 'Nómina'),
        ('PRIMA', 'Prima de Servicios'),
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='periodos'
    )
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='NOMINA',
        help_text='Indica si el periodo es de nómina regular o prima.'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    liquidado = models.BooleanField(default=False)

    class Meta:
        db_table = 'nomina_periodo'
        unique_together = ('empresa', 'fecha_inicio', 'fecha_fin')
        ordering = ['-fecha_inicio']
        verbose_name = 'Periodo de Nómina'
        verbose_name_plural = 'Periodos de Nómina'

    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio} – {self.fecha_fin})"
