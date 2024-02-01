from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MarcaViewSet, vehiculoViewSet,UserList,UserDetail

# Crear un DefaultRouter y registrar las vistas
router = DefaultRouter()
router.register(r'vehiculo', vehiculoViewSet, basename='vehiculo')
router.register(r'marca', MarcaViewSet, basename='marca')

# Obtener las URL generadas por el router y agregar las personalizadas
urlpatterns = router.urls + [
    path('api-auth/', include('rest_framework.urls')),
    path('vehiculo/filtrar-por-marca/', vehiculoViewSet.as_view({'get': 'filtrar_por_marca'}),name='vehiculo-filtrar-por-marca'),
    path('vehiculo/filtrar-por-fecha/', vehiculoViewSet.as_view({'get': 'filtrar_por_fecha'}),name='vehiculo-filtrar-por-fecha'),
    path('vehiculo/filtrar-por-marca-modelo-colores/',vehiculoViewSet.as_view({'get': 'filtrar_por_marca_modelo_colores'}),name='vehiculo-filtrar-por-marca-modelo-colores'),
    path('vehiculo/<int:pk>/', vehiculoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='vehiculo-destroy'),
    path('marca/', MarcaViewSet.as_view({'get': 'list', 'post': 'create'}), name='marca-list'),
    path('marca/<int:pk>/', MarcaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='marca-detail'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
