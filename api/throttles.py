"""
Throttle classes personalizadas para proteger la API pública.

Este módulo implementa limitaciones de tasa (rate limiting) adicionales
para prevenir abuso de la API en entornos con recursos limitados.
"""

from rest_framework.throttling import SimpleRateThrottle
import logging

logger = logging.getLogger('django.request')


class BurstRateThrottle(SimpleRateThrottle):
    """
    Throttle para limitar ráfagas de requests desde la misma IP.

    Previene ataques de denegación de servicio (DoS) limitando el número
    de requests que una misma IP puede hacer en un período corto de tiempo.

    Para usuarios anónimos: Identifica por IP usando get_ident()
    Para usuarios autenticados: Identifica por user.pk

    Configuración en settings.py:
    'burst': '10/minute'  # Máximo 10 requests por minuto
    """
    scope = 'burst'

    def get_cache_key(self, request, view):
        """
        Genera la clave de cache para identificar al cliente.

        Args:
            request: La request HTTP
            view: La vista que está siendo accedida

        Returns:
            str: Clave única para identificar al cliente (IP o user_id)
        """
        if request.user and request.user.is_authenticated:
            # Para usuarios autenticados, usar su ID
            ident = request.user.pk
        else:
            # Para usuarios anónimos, usar su IP
            ident = self.get_ident(request)

        # Crear la clave de cache
        cache_key = self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

        return cache_key

    def throttle_failure(self):
        """
        Callback ejecutado cuando se excede el límite de throttling.
        Registra el intento de abuso en los logs.
        """
        # Log de warning para alertar sobre posible abuso
        logger.warning(
            f'Burst throttle limit exceeded. '
            f'Scope: {self.scope}, '
            f'Rate: {self.rate}'
        )
        return super().throttle_failure()
