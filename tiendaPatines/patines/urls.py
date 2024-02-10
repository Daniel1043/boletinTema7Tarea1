from django.urls import path, include
from rest_framework import routers
from .views import PatineteViewSet,usuarioViewSet,AlquilerViewSet


router = routers.DefaultRouter()
router.register(r'usuarios', usuarioViewSet)
router.register(r'patinetes', PatineteViewSet)
router.register(r'alquileres', AlquilerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
