from django.urls import path
from .views import CrearEmpresaView, ListarEmpresasView, ActualizarEmpresaView
from .views import EliminarEmpresaView

urlpatterns = [
    path('crear/', CrearEmpresaView.as_view(), name='crear-empresa'),
    path('', ListarEmpresasView.as_view(), name='listar-empresas'),
    path('actualizar/', ActualizarEmpresaView.as_view(), name='actualizar-empresa'),
    path('eliminar/', EliminarEmpresaView.as_view(), name='eliminar-empresa'),
]

