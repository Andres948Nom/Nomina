from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Empleado
from .models import Novedad
from .serializers import EmpleadoSerializer
from .serializers import NovedadSerializer

class ListCreateEmpleadoView(generics.ListCreateAPIView):
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    # si deseas paginación personalizada, descomenta la línea siguiente:
    # pagination_class = EmpleadoPagination

    def get_queryset(self):
        usuario = self.request.user

        # 1. Obtener queryset inicial según empresa activa
        if usuario.tipo_usuario == 'UNICA':
            empresa = usuario.empresas.first()
            qs = Empleado.objects.filter(empresa=empresa)
        elif usuario.tipo_usuario == 'MULTIPLE' and usuario.empresa_activa:
            qs = Empleado.objects.filter(empresa=usuario.empresa_activa)
        else:
            return Empleado.objects.none()

        # 2. Filtrar por cargo (si se envía ?cargo=Contador)
        cargo = self.request.query_params.get('cargo', None)
        if cargo:
            qs = qs.filter(cargo__icontains=cargo)

        # 3. Filtrar por estado activo/inactivo (?activo=true o ?activo=false)
        activo = self.request.query_params.get('activo', None)
        if activo is not None:
            if activo.lower() in ['true', '1', 'yes']:
                qs = qs.filter(activo=True)
            elif activo.lower() in ['false', '0', 'no']:
                qs = qs.filter(activo=False)

        # 4. Filtrar por rango de fecha_ingreso:
        #    - ?fecha_ingreso_from=2025-01-01
        #    - ?fecha_ingreso_to=2025-12-31
        from_date = self.request.query_params.get('fecha_ingreso_from', None)
        if from_date:
            qs = qs.filter(fecha_ingreso__gte=from_date)
        to_date = self.request.query_params.get('fecha_ingreso_to', None)
        if to_date:
            qs = qs.filter(fecha_ingreso__lte=to_date)

        return qs

    def perform_create(self, serializer):
        usuario = self.request.user
        if usuario.tipo_usuario == 'UNICA':
            empresa = usuario.empresas.first()
        else:  # MULTIPLE
            empresa = usuario.empresa_activa

        if not empresa:
            raise ValidationError("No tienes una empresa activa seleccionada.")

        serializer.save(empresa=empresa)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data_empleado = serializer.data
        return Response(
            {
                "detail": "Empleado creado correctamente.",
                "empleado": data_empleado
            },
            status=status.HTTP_201_CREATED
        )

class RetrieveUpdateDestroyEmpleadoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.tipo_usuario == 'UNICA':
            empresa = usuario.empresas.first()
            return Empleado.objects.filter(empresa=empresa)
        if usuario.tipo_usuario == 'MULTIPLE' and usuario.empresa_activa:
            return Empleado.objects.filter(empresa=usuario.empresa_activa)
        return Empleado.objects.none()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data_empleado = serializer.data
        return Response(
            {
                "detail": "Empleado actualizado correctamente.",
                "empleado": data_empleado
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Empleado eliminado correctamente."},
            status=status.HTTP_200_OK
        )
    

class ListCreateNovedadView(generics.ListCreateAPIView):
    """
    GET: Lista las novedades del empleado autenticado en su empresa activa y período activo.
    POST: Crea una nueva novedad (el valor se calcula en save()).
    """
    serializer_class = NovedadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresa_activa = getattr(user, 'empresa_activa', None)
        if not empresa_activa:
            return Novedad.objects.none()

        # Filtrar por empresa y, opcionalmente, por un periodo pasado como query param
        periodo_id = self.request.query_params.get('periodo', None)
        if periodo_id:
            return Novedad.objects.filter(
                empleado__empresa=empresa_activa,
                periodo__id=periodo_id
            )
        else:
            return Novedad.objects.filter(empleado__empresa=empresa_activa)

    def perform_create(self, serializer):
        # Simplemente delegamos al serializer; las validaciones y cálculo ocurren allí
        return serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Sobre-escribimos create() para devolver el objeto con valor calculado.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        novedad = self.perform_create(serializer)
        data = NovedadSerializer(novedad).data
        return Response(data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyNovedadView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/novedades/<pk>/ : Ver detalle
    PUT /api/novedades/<pk>/ : Actualizar (recalcula si cambia cantidad)
    DELETE /api/novedades/<pk>/ : Eliminar
    """
    serializer_class = NovedadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        empresa_activa = getattr(user, 'empresa_activa', None)
        if not empresa_activa:
            return Novedad.objects.none()
        return Novedad.objects.filter(empleado__empresa=empresa_activa)
