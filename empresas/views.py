from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Empresa
from .serializers import EmpresaSerializer
from rest_framework.generics import DestroyAPIView

class CrearEmpresaView(generics.CreateAPIView):
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        usuario = request.user

        # Usuario UNICA ya tiene empresa → no permite crear
        if usuario.tipo_usuario == 'UNICA' and Empresa.objects.filter(usuario=usuario).exists():
            return Response(
                {'detail': 'Solo puedes crear una empresa.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crea la empresa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        empresa = serializer.save(usuario=usuario)

        # Marca is_first_login = False después de la primera creación
        if usuario.is_first_login:
            usuario.is_first_login = False
            usuario.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListarEmpresasUsuarioView(generics.ListAPIView):
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Empresa.objects.filter(usuario=self.request.user)
    
    
class ListarEmpresasView(generics.ListAPIView):
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Empresa.objects.filter(usuario=self.request.user)
    

class ActualizarEmpresaView(RetrieveUpdateAPIView):
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user

        if usuario.tipo_usuario == 'UNICA':
            return Empresa.objects.filter(usuario=usuario)

        elif usuario.tipo_usuario == 'MULTIPLE':
            if usuario.empresa_activa:
                return Empresa.objects.filter(id=usuario.empresa_activa.id, usuario=usuario)
            else:
                return Empresa.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()

class EliminarEmpresaView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmpresaSerializer

    def get_queryset(self):
        usuario = self.request.user

        if usuario.tipo_usuario == 'UNICA':
            return Empresa.objects.filter(usuario=usuario)

        elif usuario.tipo_usuario == 'MULTIPLE':
            if usuario.empresa_activa:
                return Empresa.objects.filter(id=usuario.empresa_activa.id, usuario=usuario)
            else:
                return Empresa.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response({"detail": "Empresa no encontrada o no permitida para eliminar."}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(instance)

        # Si la empresa eliminada era la activa, limpiamos empresa_activa
        if request.user.tipo_usuario == 'MULTIPLE' and request.user.empresa_activa == instance:
            request.user.empresa_activa = None
            request.user.save()

        return Response({"detail": "Empresa eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)