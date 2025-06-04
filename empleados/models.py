from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from empresas.models import Empresa
from periodo.models import PeriodoNomina
from conceptos_nomina.models import ConceptoNomina

class Empleado(models.Model):
    TIPO_CONTRATO_CHOICES = [
        ('TERMINO_FIJO', 'Término fijo'),
        ('TERMINO_INDEFINIDO', 'Término indefinido'),
        ('OBRA_O_LABOR', 'Obra o labor'),
        ('PRACTICANTE', 'Practicante'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='empleados',
        help_text="Empresa a la que pertenece este empleado."
    )
    nit_empleado = models.CharField(
        max_length=50,
        unique=True,
        help_text="Documento de identificación del empleado (p. ej. cédula)."
    )
    nombre_empleado = models.CharField(
        max_length=255,
        help_text="Nombre completo del empleado."
    )
    cargo = models.CharField(
        max_length=100,
        help_text="Puesto o cargo que ocupa en la empresa."
    )
    salario_empleado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Salario del empleado (en pesos colombianos)."
    )
    fecha_ingreso = models.DateField(
        help_text="Fecha en que el empleado comenzó a laborar."
    )
    fecha_retiro = models.DateField(
        null=True, blank=True,
        help_text="Fecha en que el empleado dejó de laborar (si aplica)."
    )
    auxilio_transporte = models.BooleanField(
        default=False,
        help_text="Indica si el empleado recibe auxilio de transporte."
    )
    activo = models.BooleanField(
        default=True,
        help_text="Si el empleado está activo (True) o ya no (False)."
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        help_text="Teléfono de contacto del empleado (opcional)."
    )
    email = models.EmailField(
        blank=True,
        help_text="Correo electrónico del empleado (opcional)."
    )
    tipo_contrato = models.CharField(
        max_length=20,
        choices=TIPO_CONTRATO_CHOICES,
        default='TERMINO_INDEFINIDO',
        help_text="Tipo de contrato del empleado."
    )
    eps = models.CharField(
        max_length=100,
        blank=True,
        help_text="EPS a la que está afiliado el empleado."
    )
    arl = models.CharField(
        max_length=100,
        blank=True,
        help_text="ARL a la que está afiliado el empleado."
    )
    grupo_nomina = models.CharField(
        max_length=100,
        blank=True,
        help_text="Grupo de nómina o área a la que pertenece (opcional)."
    )
    zona_franca = models.BooleanField(
        default=False,
        help_text="Indica si el empleado aplica a zona franca u otro beneficio especial."
    )

    # Nuevos campos de configuración individual
    descuenta_salud = models.BooleanField(
        default=True,
        help_text="Indica si al empleado se le descuenta el aporte a salud."
    )
    descuenta_pension = models.BooleanField(
        default=True,
        help_text="Indica si al empleado se le descuenta el aporte a pensión."
    )
    descuenta_arl = models.BooleanField(
        default=True,
        help_text="Indica si al empleado se le descuenta el aporte a riesgos laborales."
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empleados_empleado'
        ordering = ['-activo', 'nombre_empleado']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.nombre_empleado} ({self.nit_empleado})"

    

class Cargo(models.Model):
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.CASCADE, related_name='cargos')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"


class GrupoNomina(models.Model):
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.CASCADE, related_name='grupos_nomina')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})" 

class Novedad(models.Model):
    """
    Cada novedad se asocia a:
      - Un empleado
      - Un periodo de nómina
      - Un ConceptoNomina existente

    Si el concepto.tipo_calculo == 'FIJO', se lee directamente el campo `valor`.
    Si el concepto.tipo_calculo == 'FORMULA', se evalúa la fórmula usando `cantidad`.
    """

    empleado = models.ForeignKey(
        'empleados.Empleado',
        on_delete=models.CASCADE,
        related_name='novedades'
    )
    periodo = models.ForeignKey(
        PeriodoNomina,
        on_delete=models.CASCADE,
        related_name='novedades'
    )
    concepto = models.ForeignKey(
        ConceptoNomina,
        on_delete=models.PROTECT,
        related_name='novedades',
        help_text="Concepto de nómina asociado (con su tipo_calculo y fórmula)."
    )
    cantidad = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text=(
            "Cantidad según el tipo de fórmula (horas, días, porcentaje, etc.). "
            "Obligatorio si el concepto.tipo_calculo != 'FIJO'."
        )
    )
    valor = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True,
        help_text="Si concepto.tipo_calculo == 'FIJO', aquí se guarda el valor directo."
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empleados_novedad'
        unique_together = ('empleado', 'periodo', 'concepto')
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'

    def __str__(self):
        return f"{self.empleado.nombre_empleado} – {self.concepto.codigo} ({self.periodo.nombre})"

    def clean(self):
        """
        Validaciones:
        - Si el concepto.tipo_calculo == 'FIJO': 'valor' es obligatorio y 'cantidad' no se usa.
        - Si el concepto.tipo_calculo != 'FIJO': 'cantidad' es obligatorio y 'valor' no se usa.
        """
        tipo_calc = self.concepto.forma_calculo.upper()
        if tipo_calc == 'FIJO':
            if self.valor is None:
                raise ValidationError("Para un concepto de tipo FIJO, debes especificar 'valor'.")
            if self.cantidad not in (None, 0):
                raise ValidationError("Para un concepto de tipo FIJO, no debes proveer 'cantidad'.")
        else:
            # Para FORMULA (u otros tipos que requieren magnitud), 'cantidad' es obligatorio
            if self.cantidad is None:
                raise ValidationError("Para un concepto que no es FIJO, debes especificar 'cantidad'.")
            if self.valor not in (None, 0):
                raise ValidationError("Para un concepto de tipo FORMULA, no debes proveer 'valor' directo.")

        # Además, asegura que la novedad pertenezca a la misma empresa que el empleado:
        if self.empleado.empresa != self.periodo.empresa:
            raise ValidationError("El periodo debe corresponder a la misma empresa del empleado.")

    def calcular_valor(self):
        """
        Si el concepto.tipo_calculo == 'FORMULA', evalúa la fórmula.
        Contexto disponible:
          - 'salario': salario_empleado prorrateado si hay novedad DIAS_TRABAJADOS, o salario completo.
          - 'intensidad': empresa.configuracion.intensidad_horaria
          - 'cantidad': self.cantidad (horas, días, porcentaje, etc.)
        """
        tipo_calc = self.concepto.forma_calculo.upper()
        if tipo_calc == 'FORMULA':
            # Obtener datos necesarios para la fórmula
            empleado = self.empleado
            empresa = empleado.empresa
            config = empresa.configuracion  # ConfiguracionEmpresa
            salario_base = empleado.salario_empleado
            intensidad = config.intensidad_horaria
            aux_transporte = config.auxilio_transporte

            # Buscar la novedad de DIAS_TRABAJADOS del mismo empleado y periodo
            dias_trabajados = 30  # Valor por defecto
            novedad_dias = Novedad.objects.filter(
                empleado=empleado,
                periodo=self.periodo,
                concepto__codigo='DIAS_TRABAJADOS'
            ).first()

            if novedad_dias and novedad_dias.cantidad is not None:
                dias_trabajados = float(novedad_dias.cantidad)

            dias_periodo = (self.periodo.fecha_fin - self.periodo.fecha_inicio).days + 1
            

            # Preparar el contexto para la fórmula
            contexto = {
                'salario': float(salario_base),
                'intensidad': float(intensidad),
                'cantidad': float(self.cantidad),
                'dias_trabajados': dias_trabajados,
                'dias_periodo': dias_periodo,
                'aux_transporte': float(aux_transporte), 
            }
            # Evaluar la fórmula de forma segura
            formula = self.concepto.formula  # e.g. "(salario / intensidad) * 1.25 * cantidad"
            # Usaremos un parser sencillo (por ejemplo, ast.literal_eval no sirve para expresiones; se recomienda usar 'numexpr' o 'asteval')
            # Para este ejemplo, vamos a usar 'numexpr' para mayor seguridad:
            try:
                import numexpr as ne
                valor_calculado = ne.evaluate(formula, local_dict=contexto).item()
            except ImportError:
                # Si no tienes numexpr, puedes usar un mini-evaluador de expresiones (con ast)
                from django.conf import settings
                from asteval import Interpreter  # Asteval debe estar instalado
                ae = Interpreter()
                for k, v in contexto.items():
                    ae.symtable[k] = v
                valor_calculado = ae(formula)

            return round(valor_calculado, 2)
        return None

    def save(self, *args, **kwargs):
        # Primero limpia y verifica integridad
        self.clean()

        # Si el concepto es de tipo 'FORMULA', calculamos el valor automático
        if self.concepto.forma_calculo.upper() == 'FORMULA':
            self.valor = self.calcular_valor()
        # Si es FIJO, asumimos que `valor` ya fue asignado por el usuario

        super().save(*args, **kwargs)