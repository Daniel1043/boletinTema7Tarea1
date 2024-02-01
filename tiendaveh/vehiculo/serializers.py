from rest_framework import serializers
from .models import Marca, Vehiculo
from django.contrib.auth.models import User

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    vehiculo = serializers.PrimaryKeyRelatedField(many=True, queryset=Marca.objects.all())
    marca = serializers.PrimaryKeyRelatedField(many=True, queryset=Vehiculo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'vehiculo','marca']
