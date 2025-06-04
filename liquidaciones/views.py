from rest_framework import generics, permissions, status
from rest_framework.response import Response
from decimal import Decimal
from .models import Liquidacion, DetalleLiquidacion
from .serializers import LiquidacionSerializer
from periodo.models import PeriodoNomina
from empleados.models import Empleado, Novedad
from conceptos_nomina.models import ConceptoNomina
import numexpr as ne
from asteval import Interpreter

class LiquidacionEjecutarView(generics.GenericAPIView):
    """
    POST /api/liquidaciones/ejecutar/
    Body JSON:
      {
        "periodo": <periodo_id>,
        "empleado": <empleado_id>  # opcional; si no se provee, se liquidan todos los empleados activos
      }
    """
    serializer_class = LiquidacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        empresa_activa = request.user.empresa_activa
        periodo_id = request.data.get('periodo')
        empleado_id = request.data.get('empleado', None)

        # 1. Validar PeriodoNomina
        try:
            periodo = PeriodoNomina.objects.get(id=periodo_id, empresa=empresa_activa)
        except PeriodoNomina.DoesNotExist:
            return Response(
                {"detail": "Período no encontrado o no pertenece a la empresa activa."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Obtener lista de empleados a liquidar
        if empleado_id:
            try:
                empleado = Empleado.objects.get(id=empleado_id, empresa=empresa_activa, activo=True)
                empleados = [empleado]
            except Empleado.DoesNotExist:
                return Response(
                    {"detail": "Empleado no encontrado o no pertenece a la empresa activa."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            empleados = Empleado.objects.filter(empresa=empresa_activa, activo=True)

        respuesta = []

        for empleado in empleados:
            # 3. Si ya existe una liquidación para este empleado+periodo, la borramos
            Liquidacion.objects.filter(empleado=empleado, periodo=periodo).delete()

            # 4. Calcular días del período
            dias_periodo = (periodo.fecha_fin - periodo.fecha_inicio).days + 1

            # 5. Buscar novedad DIAS_TRABAJADOS
            try:
                nov_dias = Novedad.objects.get(
                    empleado=empleado,
                    periodo=periodo,
                    concepto__codigo='DIAS_TRABAJADOS'
                )
                dias_trabajados = float(nov_dias.cantidad)
            except Novedad.DoesNotExist:
                dias_trabajados = float(dias_periodo)

            # 6. Construir lista temporal de renglones (detalles_tmp)
            detalles_tmp = []
            config = empresa_activa.configuracion

            # --- 6.1. Sueldo Devengado ("000", tipo DEVENGADO) ---
            valor_sueldo = (empleado.salario_empleado / Decimal(dias_periodo)) * Decimal(dias_trabajados)
            detalles_tmp.append({
                'concepto': ConceptoNomina.objects.get(codigo='000', empresa=empleado.empresa),
                'cantidad': dias_trabajados,
                'valor': round(float(valor_sueldo), 2),
                'tipo': 'DEVENGADO',
                'novedad': nov_dias if 'nov_dias' in locals() else None
            })

            # --- 6.2. Auxilio de Transporte ("002", tipo DEVENGADO) ---
            if empleado.salario_empleado <= (config.asignacion_basica_anual * 2):
                valor_aux = (config.auxilio_transporte / Decimal(dias_periodo)) * Decimal(dias_trabajados)
            else:
                valor_aux = Decimal('0')
            detalles_tmp.append({
                'concepto': ConceptoNomina.objects.get(codigo='002', empresa=empleado.empresa),
                'cantidad': dias_trabajados,
                'valor': round(float(valor_aux), 2),
                'tipo': 'DEVENGADO',
                'novedad': nov_dias if 'nov_dias' in locals() else None
            })

            # --- 6.3. Otras Novedades (FORMULA o FIJO), excepto DIAS_TRABAJADOS ---
            for nov in Novedad.objects.filter(empleado=empleado, periodo=periodo):
                if nov.concepto.codigo == 'DIAS_TRABAJADOS':
                    continue
                detalles_tmp.append({
                    'concepto': nov.concepto,
                    'cantidad': nov.cantidad if nov.concepto.forma_calculo != 'FIJO' else None,
                    'valor': Decimal(nov.valor).quantize(Decimal('0.01')),
                    'tipo': nov.concepto.tipo,   # <-- Aquí usamos "tipo", que es el campo de ConceptoNomina
                    'novedad': nov
                })


            # --- 6.4. Calcular total_base_cotizacion (sum de valores donde es_base_cotizacion=True) ---

            total_base_cotizacion = sum(
                (Decimal(reng['valor'])
                 for reng in detalles_tmp 
                 if reng['concepto'].es_base_cotizacion), Decimal('0.00')
            )

            # --- 6.5. Deducciones Salud ("201") y Pensión ("202") ---
            porc_salud = config.porcentaje_salud / 100
            valor_salud = Decimal(total_base_cotizacion) * Decimal(porc_salud)
            detalles_tmp.append({
                'concepto': ConceptoNomina.objects.get(codigo='201', empresa=empleado.empresa),
                'cantidad': None,
                'valor': round(float(valor_salud), 2),
                'tipo': 'DEDUCCION',
                'novedad': None
            })

            porc_pension = config.porcentaje_pension / 100
            valor_pension = Decimal(total_base_cotizacion) * Decimal(porc_pension)
            detalles_tmp.append({
                'concepto': ConceptoNomina.objects.get(codigo='202', empresa=empleado.empresa),
                'cantidad': None,
                'valor': round(float(valor_pension), 2),
                'tipo': 'DEDUCCION',
                'novedad': None
            })

            # --- 6.6. Provisiones Informativas ---

            codigos_provision = ['101', '102', '103', '104']

            for codigo in codigos_provision:
                concepto = ConceptoNomina.objects.get(codigo=codigo, empresa=empleado.empresa)
                # Montamos el contexto para evaluar la fórmula:
                contexto = {
                    'total_base_cotizacion': float(total_base_cotizacion),
                }
                formula = concepto.formula  # Ejemplo: "total_base_cotizacion * 0.0833"

                # Evaluamos la fórmula de manera segura:
                try:
                    valor_calc = ne.evaluate(formula, local_dict=contexto).item()
                except Exception:
                    # Si no está instalado numexpr, usamos asteval como fallback:
                    ae = Interpreter()
                    ae.symtable['total_base_cotizacion'] = contexto['total_base_cotizacion']
                    valor_calc = ae(formula)

                # Convertimos a Decimal y redondeamos a 2 decimales
                valor_prov = Decimal(valor_calc).quantize(Decimal('0.01'))

                detalles_tmp.append({
                    'concepto': concepto,
                    'cantidad': None,
                    'valor': valor_prov,
                    'tipo': 'PROVISION',
                    'novedad': None
                })
            
            # — Parafiscales Caja (501) —
            concepto_caja = ConceptoNomina.objects.get(codigo='501', empresa=empleado.empresa)
            formula_caja = concepto_caja.formula  # "total_base_cotizacion * porcentaje_caja"
            contexto_pf = {
                'total_base_cotizacion': float(total_base_cotizacion),
                'porcentaje_caja': float(config.porcentaje_caja/100),
            }
            try:
                valor_caja = ne.evaluate(formula_caja, local_dict=contexto_pf).item()
            except Exception:
                ae = Interpreter()
                ae.symtable.update(contexto_pf)
                valor_caja = ae(formula_caja)
            valor_caja = Decimal(valor_caja).quantize(Decimal('0.01'))
            detalles_tmp.append({
                'concepto': concepto_caja,
                'cantidad': None,
                'valor': valor_caja,
                'tipo': 'PARAFISCALES',
                'novedad': None
            })

            # — Parafiscales SENA (502) —
            concepto_sena = ConceptoNomina.objects.get(codigo='502', empresa=empleado.empresa)
            formula_sena = concepto_sena.formula  # "total_base_cotizacion * porcentaje_sena"
            contexto_pf['porcentaje_sena'] = float(config.porcentaje_sena / 100)   
            try:
                valor_sena = ne.evaluate(formula_sena, local_dict=contexto_pf).item()
            except Exception:
                ae = Interpreter()
                ae.symtable.update(contexto_pf)
                valor_sena = ae(formula_sena)
            valor_sena = Decimal(valor_sena).quantize(Decimal('0.01'))
            detalles_tmp.append({
                'concepto': concepto_sena,
                'cantidad': None,
                'valor': valor_sena,
                'tipo': 'PARAFISCALES',
                'novedad': None
            })

            # — Parafiscales ICBF (503) —
            concepto_icbf = ConceptoNomina.objects.get(codigo='503', empresa=empleado.empresa)
            formula_icbf = concepto_icbf.formula  # "total_base_cotizacion * porcentaje_icbf"
            contexto_pf['porcentaje_icbf'] = float(config.porcentaje_icbf/100)
            try:
                valor_icbf = ne.evaluate(formula_icbf, local_dict=contexto_pf).item()
            except Exception:
                ae = Interpreter()
                ae.symtable.update(contexto_pf)
                valor_icbf = ae(formula_icbf)
            valor_icbf = Decimal(valor_icbf).quantize(Decimal('0.01'))
            detalles_tmp.append({
                'concepto': concepto_icbf,
                'cantidad': None,
                'valor': valor_icbf,
                'tipo': 'PARAFISCALES',
                'novedad': None
            })

            # --- 6.7. Sumar totales, asegurándonos de usar Decimal para el acumulador ---
            total_asignaciones  =  sum((Decimal(r['valor']) for r in detalles_tmp if r['tipo'] == 'DEVENGADO'),Decimal('0.00'))
            total_deducciones   =  sum((Decimal(r['valor']) for r in detalles_tmp if r['tipo'] == 'DEDUCCION'),Decimal('0.00'))
            total_provisiones   =  sum((Decimal(r['valor']) for r in detalles_tmp if r['tipo'] == 'PROVISION'),Decimal('0.00'))
            total_parafiscales  =  sum((Decimal(r['valor']) for r in detalles_tmp if r['tipo'] == 'PARAFISCALES'),Decimal('0.00'))
            neto_pagar = (total_asignaciones - total_deducciones).quantize(Decimal('0.01'))



            # --- 6.8. Crear Liquidación en BD ---
            liq = Liquidacion.objects.create(
                empleado=empleado,
                periodo=periodo,
                empresa=empresa_activa,
                total_asignaciones=round(float(total_asignaciones), 2),
                total_deducciones=round(float(total_deducciones), 2),
                total_provisiones=round(float(total_provisiones), 2),
                total_parafiscales=round(float(total_parafiscales), 2),
                neto_pagar=round(float(neto_pagar), 2),
            )

            # --- 6.9. Crear DetalleLiquidacion en BD ---
            for r in detalles_tmp:
                DetalleLiquidacion.objects.create(
                    liquidacion=liq,
                    concepto=r['concepto'],
                    cantidad=r['cantidad'],
                    valor=r['valor'],
                    tipo=r['tipo'],
                    novedad=r['novedad']
                )

            respuesta.append(LiquidacionSerializer(liq).data)

        return Response(respuesta, status=status.HTTP_201_CREATED)


class LiquidacionListView(generics.ListAPIView):
    """
    GET /api/liquidaciones/?periodo=<id>
    Lista todas las liquidaciones de la empresa activa.
    Opcionalmente filtra por periodo.
    """
    serializer_class = LiquidacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        empresa_activa = self.request.user.empresa_activa
        periodo_id = self.request.query_params.get('periodo', None)
        qs = Liquidacion.objects.filter(empresa=empresa_activa)
        if periodo_id:
            qs = qs.filter(periodo__id=periodo_id)
        return qs


class LiquidacionDetailView(generics.RetrieveAPIView):
    """
    GET /api/liquidaciones/<pk>/
    Devuelve detalle de una liquidación de la empresa activa.
    """
    serializer_class = LiquidacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        empresa_activa = self.request.user.empresa_activa
        return Liquidacion.objects.filter(empresa=empresa_activa)
