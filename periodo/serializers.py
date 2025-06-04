from rest_framework import serializers
from .models import PeriodoNomina

class PeriodoNominaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoNomina
        fields = [
            'id',
            'empresa',
            'nombre',
            'fecha_inicio',
            'fecha_fin',
            'liquidado',
        ]
        read_only_fields = ['empresa', 'liquidado']
