from django.urls import path
from .views import ListCreateEmpleadoView, RetrieveUpdateDestroyEmpleadoView
from .views import ListCreateNovedadView, RetrieveUpdateDestroyNovedadView

urlpatterns = [
    path('', ListCreateEmpleadoView.as_view(), name='listar_crear_empleado'),
    path('<int:id>/', RetrieveUpdateDestroyEmpleadoView.as_view(), name='detalle_empleado'),
    path('novedades/', ListCreateNovedadView.as_view(), name='novedad-list-create'),
    path('novedades/<int:pk>/', RetrieveUpdateDestroyNovedadView.as_view(), name='novedad-detail'),

]
