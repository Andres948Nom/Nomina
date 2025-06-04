from rest_framework import serializers
from .models import Liquidacion, DetalleLiquidacion

class DetalleLiquidacionSerializer(serializers.ModelSerializer):
    concepto_codigo = serializers.CharField(source='concepto.codigo', read_only=True)
    concepto_nombre = serializers.CharField(source='concepto.nombre', read_only=True)

    class Meta:
        model = DetalleLiquidacion
        fields = [
            'id',
            'concepto',
            'concepto_codigo',
            'concepto_nombre',
            'cantidad',
            'valor',
            'tipo',
            'novedad',
        ]
        read_only_fields = ['id', 'concepto_codigo', 'concepto_nombre']

class LiquidacionSerializer(serializers.ModelSerializer):
    detalles = DetalleLiquidacionSerializer(many=True, read_only=True)
    empleado_nombre = serializers.CharField(source='empleado.nombre_empleado', read_only=True)
    periodo_nombre = serializers.CharField(source='periodo.nombre', read_only=True)

    class Meta:
        model = Liquidacion
        fields = [
            'id',
            'empleado',
            'empleado_nombre',
            'periodo',
            'periodo_nombre',
            'empresa',
            'fecha_liquidacion',
            'total_asignaciones',
            'total_deducciones',
            'total_provisiones',
            'total_parafiscales',
            'neto_pagar',
            'detalles',
        ]
        read_only_fields = [
            'id',
            'empresa',
            'fecha_liquidacion',
            'total_asignaciones',
            'total_deducciones',
            'total_provisiones',
            'total_parafiscales',
            'neto_pagar',
            'detalles',
            'empleado_nombre',
            'periodo_nombre',
        ]
