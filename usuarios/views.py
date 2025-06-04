from rest_framework.views import APIView
from rest_framework import generics
from .models import CustomUser
from .serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from empresas.serializers import EmpresaSerializer
from empresas.models import Empresa
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class SeleccionarEmpresaActivaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        empresa_id = request.data.get('empresa_id')

        if user.tipo_usuario != 'MULTIPLE':
            return Response({'detail': 'Solo los usuarios tipo MULTIPLE pueden cambiar de empresa activa.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            empresa = Empresa.objects.get(id=empresa_id, usuario=user)
        except Empresa.DoesNotExist:
            return Response({'detail': 'Empresa no encontrada o no asociada a este usuario.'}, status=status.HTTP_404_NOT_FOUND)

        user.empresa_activa = empresa
        user.save()

        return Response({'detail': f'Empresa activa cambiada a: {empresa.nombre}'}, status=status.HTTP_200_OK)
    

class PerfilUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        usuario = request.user

        # Obtener empresa activa según tipo de usuario
        empresa_activa = None

        if usuario.tipo_usuario == 'UNICA':
            empresa_activa = Empresa.objects.filter(usuario=usuario).first()
        elif usuario.tipo_usuario == 'MULTIPLE' and usuario.empresa_activa:
            empresa_activa = usuario.empresa_activa

        data = {
            "id": usuario.id,
            "username": usuario.username,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario,
            "is_first_login": usuario.is_first_login,
            "empresa_activa": EmpresaSerializer(empresa_activa).data if empresa_activa else None
        }

        return Response(data)

