"""
Paginación personalizada para la API.
Protege contra queries muy grandes que pueden consumir mucha RAM.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Paginación estándar con límite máximo.
    
    - page_size: 20 resultados por defecto
    - max_page_size: 100 resultados máximo (protección contra abuso)
    - page_size_query_param: permite al cliente ajustar con ?page_size=X
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100  # IMPORTANTE: Limita queries grandes
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class SmallResultsSetPagination(PageNumberPagination):
    """
    Paginación para endpoints costosos (estadísticas, agregaciones).
    Límite más pequeño para proteger recursos.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50  # Límite más restrictivo
