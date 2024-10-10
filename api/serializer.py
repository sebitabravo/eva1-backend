from rest_framework import serializers
from .models import conductor, camion, tipo_madera, cliente, carga


class conductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = conductor
        fields = '__all__'


class camionSerializer(serializers.ModelSerializer):
    class Meta:
        model = camion
        fields = '__all__'


class tipo_maderaSerializer(serializers.ModelSerializer):
    class Meta:
        model = tipo_madera
        fields = '__all__'


class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = cliente
        fields = '__all__'


class cargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = carga
        fields = '__all__'
