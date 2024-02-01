from rest_framework import viewsets, generics
from .models import Marca, Vehiculo
from .serializers import MarcaSerializer, VehiculoSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsEditorUser


class MarcaViewSet(viewsets.ModelViewSet):
    """
    Este ViewSet proporciona acciones de `list`, `create`, `retrieve`,
    `update`, `destroy` y una acción personalizada `highlight` para el modelo Marca.
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsEditorUser]


class vehiculoViewSet(viewsets.ModelViewSet):
    """
    Este ViewSet proporciona acciones de `list`, `create`, `retrieve`,
    `update`, `destroy` y una acción personalizada `highlight` para el modelo Vehiculo.
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [IsEditorUser]

    @action(detail=False, methods=['GET'], url_path='filtrar-por-marca', url_name='filtrar_por_marca')
    def filtrar_por_marca(self, request, *args, **kwargs):
        marca = request.query_params.get('marca', None)

        if marca is None:
            return Response({"error": "Debes proporcionar la marca como parámetro"}, status=status.HTTP_400_BAD_REQUEST)

        vehiculos_filtrados = Vehiculo.objects.filter(marca=marca)
        serializer = VehiculoSerializer(vehiculos_filtrados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='filtrar_por_fecha', url_name='filtrar_por_fecha')
    def filtrar_por_fecha(self, *args, **kwargs):
        vehiculos_filtrados_fechas = Vehiculo.objects.all().order_by('-fecha_fabricacion')
        serializer = VehiculoSerializer(vehiculos_filtrados_fechas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='filtrar_por_marca_modelo_colores', url_name='filtrar_por_marca_modelo_colores')
    def filtrar_por_marca_modelo_colores(self,request, *args, **kwargs):
        marca = request.query_params.get('marca', None)
        modelo = request.query_params.get('modelo', None)
        color = request.query_params.get('color', None)

        if marca is None:
            return Response({"error": "Debes proporcionar la marca como parámetro"}, status=status.HTTP_400_BAD_REQUEST)

        vehiculos_filtrados_tres = Vehiculo.objects.filter(marca=marca, color=color,modelo=modelo)
        serializer = VehiculoSerializer(vehiculos_filtrados_tres, many=True)
        return Response(serializer.data)



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer