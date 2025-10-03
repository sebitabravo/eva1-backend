from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
from .permissions import IsAdminOrReadOnly
from .pagination import StandardResultsSetPagination


@csrf_exempt
def health_check(request):
    """Endpoint de health check para contenedor - no requiere autenticación ni validación de host"""
    return JsonResponse({'status': 'healthy'}, status=200)


class StatsThrottle(UserRateThrottle):
    """Throttle específico para endpoints de estadísticas (costosos)"""
    scope = 'stats'


class WriteThrottle(UserRateThrottle):
    """Throttle específico para operaciones de escritura"""
    scope = 'write'


class ConductorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar conductores.
    Proporciona operaciones CRUD completas.
    
    Protecciones:
    - Solo administradores pueden crear/modificar/eliminar
    - Paginación con límite máximo
    - Throttling para operaciones de escritura
    """
    queryset = Conductor.objects.all().prefetch_related('camiones')
    serializer_class = ConductorSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'licencia_conducir', 'telefono']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    def get_throttles(self):
        """Aplica throttling más restrictivo en operaciones de escritura"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        return super().get_throttles()

    @action(detail=True, methods=['get'])
    def camiones(self, request, pk=None):
        """Obtiene todos los camiones asignados a un conductor"""
        conductor = self.get_object()
        camiones = conductor.camiones.all()
        
        # Aplicar paginación
        page = self.paginate_queryset(camiones)
        if page is not None:
            serializer = CamionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CamionSerializer(camiones, many=True)
        return Response(serializer.data)


class CamionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar camiones.
    Proporciona operaciones CRUD completas y filtros.
    
    Protecciones:
    - Solo administradores pueden crear/modificar/eliminar
    - Paginación con límite máximo
    - Throttling especial para estadísticas (endpoints costosos)
    - Cache en estadísticas (15 minutos)
    """
    queryset = Camion.objects.all().select_related('conductor').prefetch_related('cargas')
    serializer_class = CamionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conductor', 'placa']
    search_fields = ['placa', 'modelo', 'conductor__nombre']
    ordering_fields = ['placa', 'capacidad_carga', 'created_at']
    ordering = ['placa']
    
    def get_throttles(self):
        """Aplica throttling según la acción"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        elif self.action == 'estadisticas':
            return [StatsThrottle()]
        return super().get_throttles()

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
        
        # Aplicar paginación
        page = self.paginate_queryset(cargas)
        if page is not None:
            serializer = CargaSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CargaSerializer(cargas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], throttle_classes=[StatsThrottle])
    @method_decorator(cache_page(60 * 15))  # Cache de 15 minutos
    def estadisticas(self, request, pk=None):
        """
        Obtiene estadísticas del camión.
        Endpoint costoso: throttling restrictivo + cache.
        """
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
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    def get_throttles(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        return super().get_throttles()

    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """Obtiene todas las cargas de este tipo de madera"""
        tipo_madera = self.get_object()
        cargas = tipo_madera.cargas.all()
        
        page = self.paginate_queryset(cargas)
        if page is not None:
            serializer = CargaSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CargaSerializer(cargas, many=True)
        return Response(serializer.data)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar clientes.
    Proporciona operaciones CRUD completas.
    """
    queryset = Cliente.objects.all().prefetch_related('cargas')
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre_empresa', 'correo_electronico', 'telefono']
    ordering_fields = ['nombre_empresa', 'created_at']
    ordering = ['nombre_empresa']
    
    def get_throttles(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        elif self.action == 'estadisticas':
            return [StatsThrottle()]
        return super().get_throttles()

    @action(detail=True, methods=['get'])
    def cargas(self, request, pk=None):
        """Obtiene todas las cargas del cliente"""
        cliente = self.get_object()
        cargas = cliente.cargas.all()
        
        page = self.paginate_queryset(cargas)
        if page is not None:
            serializer = CargaSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CargaSerializer(cargas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], throttle_classes=[StatsThrottle])
    @method_decorator(cache_page(60 * 15))  # Cache de 15 minutos
    def estadisticas(self, request, pk=None):
        """
        Obtiene estadísticas del cliente.
        Endpoint costoso: throttling restrictivo + cache.
        """
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
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_madera', 'camion', 'cliente']
    search_fields = ['tipo_madera__nombre', 'camion__placa', 'cliente__nombre_empresa']
    ordering_fields = ['created_at', 'peso', 'cantidad']
    ordering = ['-created_at']
    
    def get_throttles(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [WriteThrottle()]
        elif self.action == 'estadisticas_generales':
            return [StatsThrottle()]
        return super().get_throttles()

    def get_serializer_class(self):
        """Usa serializer detallado para retrieve"""
        if self.action == 'retrieve':
            return CargaDetailSerializer
        return CargaSerializer

    @action(detail=False, methods=['get'], throttle_classes=[StatsThrottle])
    @method_decorator(cache_page(60 * 15))  # Cache de 15 minutos
    def estadisticas_generales(self, request):
        """
        Obtiene estadísticas generales de todas las cargas.
        Endpoint MUY costoso: throttling restrictivo + cache largo.
        """
        stats = Carga.objects.aggregate(
            total_cargas=Count('id'),
            peso_total=Sum('peso'),
            cantidad_total=Sum('cantidad'),
        )
        return Response(stats)
