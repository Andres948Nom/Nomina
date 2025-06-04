from django.db import models
from django.conf import settings
from decimal import Decimal

class Empresa(models.Model):
    TIPO_EMPRESA_CHOICES = [
        ('NATURAL', 'Natural'),
        ('JURIDICA', 'Jurídica'),
    ]

    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    tipo_empresa = models.CharField(max_length=10, choices=TIPO_EMPRESA_CHOICES)
    regimen = models.CharField(max_length=100)

    # Relación con el usuario (creador)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='empresas'
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.nit})"


class ConfiguracionEmpresa(models.Model):
    empresa = models.OneToOneField('Empresa', on_delete=models.CASCADE, related_name='configuracion')

    asignacion_basica_anual = models.DecimalField(max_digits=12, decimal_places=2, default=1423500)
    auxilio_transporte = models.DecimalField(max_digits=12, decimal_places=2, default=200000)
    intensidad_horaria = models.PositiveIntegerField(default=230)
    porcentaje_salud = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    porcentaje_pension = models.DecimalField(max_digits=5, decimal_places=2, default=4.0)
    porcentaje_riesgos = models.DecimalField(max_digits=5, decimal_places=2, default=0.52)
    porcentaje_caja = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('4.00'))
    porcentaje_sena = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('2.00'))
    porcentaje_icbf = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('3.00'))                                                                           


    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Configuración {self.empresa.nombre}"