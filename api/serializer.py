from rest_framework import serializers
from .models import Conductor, Camion, TipoMadera, Cliente, Carga


class ConductorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Conductor"""
    camiones_count = serializers.SerializerMethodField()

    class Meta:
        model = Conductor
        fields = [
            'id',
            'nombre',
            'licencia_conducir',
            'telefono',
            'direccion',
            'created_at',
            'updated_at',
            'camiones_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_camiones_count(self, obj):
        """Retorna la cantidad de camiones asignados al conductor"""
        return obj.camiones.count()

    def validate_licencia_conducir(self, value):
        """Validación adicional para la licencia de conducir"""
        if len(value) < 5:
            raise serializers.ValidationError(
                "La licencia de conducir debe tener al menos 5 caracteres."
            )
        return value.upper()


class CamionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Camion"""
    conductor_nombre = serializers.CharField(source='conductor.nombre', read_only=True)
    cargas_count = serializers.SerializerMethodField()

    class Meta:
        model = Camion
        fields = [
            'id',
            'placa',
            'modelo',
            'capacidad_carga',
            'conductor',
            'conductor_nombre',
            'created_at',
            'updated_at',
            'cargas_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cargas_count(self, obj):
        """Retorna la cantidad de cargas asignadas al camión"""
        return obj.cargas.count()

    def validate_placa(self, value):
        """Validación adicional para la placa"""
        return value.upper()


class CamionDetailSerializer(CamionSerializer):
    """Serializer detallado para Camion con información del conductor"""
    conductor = ConductorSerializer(read_only=True)


class TipoMaderaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo TipoMadera"""
    cargas_count = serializers.SerializerMethodField()

    class Meta:
        model = TipoMadera
        fields = [
            'id',
            'nombre',
            'descripcion',
            'created_at',
            'updated_at',
            'cargas_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cargas_count(self, obj):
        """Retorna la cantidad de cargas de este tipo de madera"""
        return obj.cargas.count()


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Cliente"""
    cargas_count = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre_empresa',
            'direccion',
            'telefono',
            'correo_electronico',
            'created_at',
            'updated_at',
            'cargas_count',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cargas_count(self, obj):
        """Retorna la cantidad de cargas del cliente"""
        return obj.cargas.count()

    def validate_correo_electronico(self, value):
        """Validación adicional para el correo electrónico"""
        return value.lower()


class CargaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Carga"""
    tipo_madera_nombre = serializers.CharField(source='tipo_madera.nombre', read_only=True)
    camion_placa = serializers.CharField(source='camion.placa', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre_empresa', read_only=True)

    class Meta:
        model = Carga
        fields = [
            'id',
            'tipo_madera',
            'tipo_madera_nombre',
            'cantidad',
            'peso',
            'camion',
            'camion_placa',
            'cliente',
            'cliente_nombre',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validación a nivel de objeto para verificar que el peso
        no exceda la capacidad del camión.
        """
        peso = data.get('peso')
        camion = data.get('camion')

        if peso and camion:
            if peso > camion.capacidad_carga:
                raise serializers.ValidationError({
                    'peso': f'El peso de la carga ({peso}t) excede la capacidad del camión ({camion.capacidad_carga}t).'
                })

        return data


class CargaDetailSerializer(CargaSerializer):
    """Serializer detallado para Carga con información completa de relaciones"""
    tipo_madera = TipoMaderaSerializer(read_only=True)
    camion = CamionSerializer(read_only=True)
    cliente = ClienteSerializer(read_only=True)
