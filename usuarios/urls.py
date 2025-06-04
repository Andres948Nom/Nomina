from django.urls import path
from .views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView
from .views import SeleccionarEmpresaActivaView
from .views import PerfilUsuarioView

urlpatterns = [
    path('registro/', UserRegisterView.as_view(), name='registro'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('empresa/seleccionar/', SeleccionarEmpresaActivaView.as_view(), name='seleccionar_empresa'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),

]
