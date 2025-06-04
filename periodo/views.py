from rest_framework import generics, permissions
from .models import PeriodoNomina
from .serializers import PeriodoNominaSerializer

class PeriodoListCreateView(generics.ListCreateAPIView):
    """
    GET    /api/periodos/        → Lista todos los períodos de la empresa activa del usuario.
    POST   /api/periodos/        → Crea un nuevo período para la empresa activa.
    """
    serializer_class = PeriodoNominaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Suponemos que existe user.empresa_activa
        empresa_activa = getattr(user, 'empresa_activa', None)
        if not empresa_activa:
            return PeriodoNomina.objects.none()
        return PeriodoNomina.objects.filter(empresa=empresa_activa)

    def perform_create(self, serializer):
        # Forzamos que el nuevo Período pertenezca a la empresa activa
        empresa_activa = self.request.user.empresa_activa
        serializer.save(empresa=empresa_activa)


class PeriodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/periodos/<pk>/   → Obtiene detalle de un período (si pertenece a la empresa activa).
    PUT    /api/periodos/<pk>/   → Actualiza un período existente.
    DELETE /api/periodos/<pk>/   → Elimina un período (solo si no está marcado como `liquidado=True`).
    """
    serializer_class = PeriodoNominaSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        empresa_activa = getattr(user, 'empresa_activa', None)
        if not empresa_activa:
            return PeriodoNomina.objects.none()
        return PeriodoNomina.objects.filter(empresa=empresa_activa)

    def perform_update(self, serializer):
        # Evitar modificar un período ya liquidado (opcional)
        periodo = self.get_object()
        if periodo.liquidado:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("No puedes modificar un período ya liquidado.")
        serializer.save()

    def perform_destroy(self, instance):
        # Evitar eliminar un período ya liquidado (opcional)
        if instance.liquidado:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("No puedes eliminar un período ya liquidado.")
        instance.delete()
