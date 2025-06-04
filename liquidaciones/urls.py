from django.urls import path
from .views import (
    LiquidacionEjecutarView,
    LiquidacionListView,
    LiquidacionDetailView,
)

urlpatterns = [
    # Ejecutar liquidación (todos o un empleado específico)
    path('ejecutar/', LiquidacionEjecutarView.as_view(), name='liquidacion-ejecutar'),
    # Listar liquidaciones (filtro opcional por periodo: ?periodo=ID)
    path('', LiquidacionListView.as_view(), name='liquidacion-list'),
    # Ver detalle de una liquidación
    path('<int:pk>/', LiquidacionDetailView.as_view(), name='liquidacion-detail'),
]
