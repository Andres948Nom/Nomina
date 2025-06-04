from django.urls import path
from .views import (
    PeriodoListCreateView,
    PeriodoRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Listar todos los períodos y crear uno nuevo
    path('', PeriodoListCreateView.as_view(), name='periodo-list-create'),

    # Ver/actualizar/eliminar un período concreto por su PK
    path('<int:pk>/', PeriodoRetrieveUpdateDestroyView.as_view(), name='periodo-detail'),
]
