"""
Permisos personalizados para la API de Maderas.
Estos permisos protegen contra abuso de recursos en servidor compartido.
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado que permite:
    - Lectura (GET, HEAD, OPTIONS) a todos los usuarios
    - Escritura (POST, PUT, PATCH, DELETE) solo a administradores
    
    Útil para APIs públicas donde quieres proteger datos contra modificaciones no autorizadas.
    """
    
    def has_permission(self, request, view):
        # Permitir métodos de lectura a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permitir escritura solo a administradores
        return request.user and request.user.is_staff


class IsAuthenticatedAndStaffOrReadOnly(permissions.BasePermission):
    """
    Permiso más restrictivo:
    - Lectura a todos
    - Escritura solo a usuarios autenticados Y que sean staff
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )
