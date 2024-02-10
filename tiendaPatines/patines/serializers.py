from rest_framework import serializers

from .models import Usuario, Alquiler, Patinete


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class PatineteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patinete
        fields = '__all__'


class AlquilerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alquiler
        fields = '__all__'

