from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count

from .models import Conductor, Camion, TipoMadera, Cliente, Carga
from .serializer import (
    ConductorSerializer,
    CamionSerializer,
    CamionDetailSerializer,
    TipoMaderaSerializer,
    ClienteSerializer,
    CargaSerializer,
    CargaDetailSerializer,
)


class ConductorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar conductores.
    Proporciona operaciones CRUD completas.
    """
    queryset = Conductor.objects.all().prefetch_related('camiones')
    serializer_class = ConductorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'licencia_conducir', 'telefono']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']

    @action(detail=True, methods=['get'])
    def camiones(self, request, pk=None):
        """Obtiene todos los camiones asignados a un conductor"""
        conductor = self.get_object()
        camiones = conductor.camiones.all()
        serializer = CamionSerializer(camiones, many=True)
        return Response(serializer.data)


class CamionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar camiones.
    Proporciona operaciones CRUD completas y filtros.
    """
    queryset = Camion.objects.all().select_related('conductor').prefetch_related('cargas')
    serializer_class = CamionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conductor', 'placa']
    search_fields = ['placa', 'modelo', 'conductor__nombre']
    ordering_fields = ['placa', 'capacidad_carga', 'created_at']
    ordering = ['placa']

    def get_serializer_class(self):
        """Usa serializer detallado para retrieve"""
        if self.action == 'retrieve':
            return CamionDetailSerializer
        return CamionSerializer

    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """Obtiene todas las cargas transportadas por un camión"""
        camion = self.get_object()
        cargas = camion.cargas.all()
        serializer = CargaSerializer(cargas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtiene estadísticas del camión"""
        camion = self.get_object()
        stats = camion.cargas.aggregate(
            total_cargas=Count('id'),
            peso_total=Sum('peso'),
        )
        return Response({
            'camion': CamionSerializer(camion).data,
            'estadisticas': stats,
        })


class TipoMaderaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tipos de madera.
    Proporciona operaciones CRUD completas.
    """
    queryset = TipoMadera.objects.all()
    serializer_class = TipoMaderaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']

    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """Obtiene todas las cargas de este tipo de madera"""
        tipo_madera = self.get_object()
        cargas = tipo_madera.cargas.all()
        serializer = CargaSerializer(cargas, many=True)
        return Response(serializer.data)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes.
    Proporciona operaciones CRUD completas.
    """
    queryset = Cliente.objects.all().prefetch_related('cargas')
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre_empresa', 'correo_electronico', 'telefono']
    ordering_fields = ['nombre_empresa', 'created_at']
    ordering = ['nombre_empresa']

    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """Obtiene todas las cargas del cliente"""
        cliente = self.get_object()
        cargas = cliente.cargas.all()
        serializer = CargaSerializer(cargas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtiene estadísticas del cliente"""
        cliente = self.get_object()
        stats = cliente.cargas.aggregate(
            total_cargas=Count('id'),
            peso_total=Sum('peso'),
            cantidad_total=Sum('cantidad'),
        )
        return Response({
            'cliente': ClienteSerializer(cliente).data,
            'estadisticas': stats,
        })


class CargaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cargas.
    Proporciona operaciones CRUD completas con filtros avanzados.
    """
    queryset = Carga.objects.all().select_related(
        'tipo_madera', 'camion', 'cliente'
    )
    serializer_class = CargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_madera', 'camion', 'cliente']
    search_fields = ['tipo_madera__nombre', 'camion__placa', 'cliente__nombre_empresa']
    ordering_fields = ['created_at', 'peso', 'cantidad']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Usa serializer detallado para retrieve"""
        if self.action == 'retrieve':
            return CargaDetailSerializer
        return CargaSerializer

    @action(detail=False, methods=['get'])
    def estadisticas_generales(self, request):
        """Obtiene estadísticas generales de todas las cargas"""
        stats = Carga.objects.aggregate(
            total_cargas=Count('id'),
            peso_total=Sum('peso'),
            cantidad_total=Sum('cantidad'),
        )
        return Response(stats)
