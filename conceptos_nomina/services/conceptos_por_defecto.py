# conceptos_nomina/services/conceptos_por_defecto.py

CONCEPTOS_POR_DEFECTO = [
    # DEVENGADOS BÁSICOS
    {"codigo": "000", "nombre": "Sueldo devengado", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "(salario / 30) * dias_trabajados", "es_base_cotizacion": True},
    {"codigo": "001", "nombre": "Asignación Básica", "tipo": "DEVENGADO", "forma_calculo": "FIJO", "formula": "", "es_base_cotizacion": True},
    {"codigo": "002", "nombre": "Auxilio de Transporte", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((aux_transporte / 30) * dias_trabajados) if salario < 2600000 else 0", "es_base_cotizacion": False},
    
    # HORAS EXTRAS Y RECARGOS
    {"codigo": "003", "nombre": "Hora Extra Diurna", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 1.25) * cantidad", "es_base_cotizacion": True},
    {"codigo": "004", "nombre": "Hora Extra Nocturna", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 1.75) * cantidad", "es_base_cotizacion": True},
    {"codigo": "005", "nombre": "Hora Extra Dominical/Festiva Diurna", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 2) * cantidad", "es_base_cotizacion": True},
    {"codigo": "006", "nombre": "Hora Extra Dominical/Festiva Nocturna", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 2.5) * cantidad", "es_base_cotizacion": True},
    {"codigo": "007", "nombre": "Recargo Nocturno", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 0.35) * cantidad", "es_base_cotizacion": True},
    {"codigo": "008", "nombre": "Recargo Dominical/Festivo", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 1.75) * cantidad", "es_base_cotizacion": True},
    {"codigo": "009", "nombre": "Recargo Nocturno Dominical/Festivo", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((salario / intensidad) * 2.10) * cantidad", "es_base_cotizacion": True},

    # PRESTACIONES PROVISIONADAS
    {"codigo": "101", "nombre": "Cesantías (Provisión)", "tipo": "PROVISION", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * 0.0833", "es_base_cotizacion": False},
    {"codigo": "102", "nombre": "Prima (Provisión)", "tipo": "PROVISION", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * 0.0833", "es_base_cotizacion": False},
    {"codigo": "103", "nombre": "Vacaciones (Provisión)", "tipo": "PROVISION", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * 0.0417", "es_base_cotizacion": False},
    {"codigo": "104", "nombre": "Intereses Cesantías (Provisión)", "tipo": "PROVISION", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * 0.0417", "es_base_cotizacion": False},

    # PRESTACIONES PAGADAS
    {"codigo": "111", "nombre": "Cesantías (Pago)", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "(salario * dias_trabajados) / 360", "es_base_cotizacion": False},
    {"codigo": "112", "nombre": "Prima (Pago)", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "(salario + aux_transporte) * cantidad / 360", "es_base_cotizacion": False},
    {"codigo": "113", "nombre": "Vacaciones (Pago)", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "(salario * dias_trabajados) / 720", "es_base_cotizacion": False},
    {"codigo": "114", "nombre": "Intereses Cesantías (Pago)", "tipo": "DEVENGADO", "forma_calculo": "FORMULA", "formula": "((cesantias * dias_trabajados) * 0.12) / 360", "es_base_cotizacion": False},

    # DEDUCCIONES
    {"codigo": "201", "nombre": "Salud", "tipo": "DEDUCCION", "forma_calculo": "FORMULA", "formula": "salario * 0.04", "es_base_cotizacion": False},
    {"codigo": "202", "nombre": "Pensión", "tipo": "DEDUCCION", "forma_calculo": "FORMULA", "formula": "salario * 0.04", "es_base_cotizacion": False},

    # INFORMATIVOS
    {"codigo": "DIAS_TRABAJADOS", "nombre": "Días Trabajados", "tipo": "INFORMATIVO", "forma_calculo": "MANUAL", "formula": "", "es_base_cotizacion": False},
    {"codigo": "302", "nombre": "Días Prov Vacaciones", "tipo": "INFORMATIVO", "forma_calculo": "MANUAL", "formula": "", "es_base_cotizacion": False},
    {"codigo": "303", "nombre": "Días Prov Prima", "tipo": "INFORMATIVO", "forma_calculo": "MANUAL", "formula": "", "es_base_cotizacion": False},
    {"codigo": "304", "nombre": "Días de Incapacidad", "tipo": "INFORMATIVO", "forma_calculo": "MANUAL", "formula": "", "es_base_cotizacion": False},
    {"codigo": "305", "nombre": "Días Pago Vacaciones", "tipo": "INFORMATIVO", "forma_calculo": "MANUAL", "formula": "", "es_base_cotizacion": False},
    {"codigo": "306", "nombre": "Días Pago Prima", "tipo": "INFORMATIVO", "forma_calculo": "MANUAL", "formula": "", "es_base_cotizacion": False},
    
     # BONIFICACIONES

    {"codigo": "401", "nombre": "Bono No Salarial", "tipo": "DEVENGADO", "forma_calculo": "FIJO", "formula": "", "es_base_cotizacion": False},
    {"codigo": "402", "nombre": "Rodamiento", "tipo": "DEVENGADO", "forma_calculo": "FIJO", "formula": "", "es_base_cotizacion": False},

     # PARAFISCALES

    {"codigo": "501", "nombre": "Caja Compensacion", "tipo": "PARAFISCALES", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * porcentaje_caja", "es_base_cotizacion": False},
    {"codigo": "502", "nombre": "Aporte Sena", "tipo": "PARAFISCALES", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * porcentaje_sena", "es_base_cotizacion": False},
    {"codigo": "503", "nombre": "Aporte ICBF", "tipo": "PARAFISCALES", "forma_calculo": "FORMULA", "formula": "total_base_cotizacion * porcentaje_icbf", "es_base_cotizacion": False},
]
