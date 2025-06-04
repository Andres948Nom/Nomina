from rest_framework import serializers
from .models import Empleado
from .models import Novedad

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = [
            'id',
            'nit_empleado',
            'nombre_empleado',
            'cargo',
            'salario_empleado',
            'fecha_ingreso',
            'fecha_retiro',
            'auxilio_transporte',
            'activo',
            'telefono',
            'email',
            'tipo_contrato',
            'eps',
            'arl',
            'grupo_nomina',
            'zona_franca',
            'descuenta_salud',
            'descuenta_pension',
            'descuenta_arl'

        ]

        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def validate_salario_empleado(self, value):
        """
        Asegura que salario_empleado sea positivo.
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError("El salario debe ser un valor positivo.")
        return value

    def validate(self, data):
        """
        Verifica que, si fecha_retiro está presente, sea posterior a fecha_ingreso.
        """
        fecha_ingreso = data.get('fecha_ingreso', None)
        fecha_retiro = data.get('fecha_retiro', None)

        if fecha_retiro and fecha_ingreso and fecha_retiro < fecha_ingreso:
            raise serializers.ValidationError({
                "fecha_retiro": "La fecha de retiro debe ser posterior o igual a la fecha de ingreso."
            })
        return data
    
class NovedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novedad
        fields = [
            'id',
            'empleado',
            'periodo',
            'concepto',
            'cantidad',
            'valor',
            'creado_en',
            'actualizado_en',
        ]
        read_only_fields = ['valor', 'creado_en', 'actualizado_en']

    def validate(self, data):
        """
        Asegura que:
        - Empleado y Periodo pertenecen a la misma empresa.
        - El Periodo está abierto (no liquidado).
        """
        empleado = data.get('empleado')
        periodo = data.get('periodo')
        concepto = data.get('concepto')

        # Verificar que empleado y periodo compartan empresa
        if empleado.empresa != periodo.empresa:
            raise serializers.ValidationError("El período y el empleado deben pertenecer a la misma empresa.")

        # Verificar que el período no esté liquidado
        if periodo.liquidado:
            raise serializers.ValidationError("No puedes agregar novedades a un período ya liquidado.")

        # Verificar que el concepto pertenezca a la misma empresa
        if concepto.empresa != empleado.empresa:
            raise serializers.ValidationError("El concepto seleccionado no pertenece a la empresa del empleado.")

        return data

    def create(self, validated_data):
        """
        Al crear la novedad, el valor se calculará automáticamente en el método save() del modelo.
        """
        novedad = Novedad.objects.create(**validated_data)
        return novedad

    