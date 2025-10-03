"""
Core views for drfmaderas project.

Incluye vistas de seguridad y redirección.
"""
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET


@require_GET
def root_redirect(request):
    """
    Redirecciona la URL raíz (/) a la API (/api/).

    Esta vista previene que se exponga la página 404 de Django
    con todas las rutas configuradas cuando DEBUG=True.

    Returns:
        HttpResponseRedirect: Redirección permanente a /api/
    """
    return redirect('/api/', permanent=True)


@require_GET
def custom_404(request, exception=None):
    """
    Vista personalizada para errores 404.

    Esta vista no revela información sobre la estructura de rutas
    de la aplicación, mejorando la seguridad.

    Args:
        request: HttpRequest object
        exception: Excepción que causó el 404 (opcional)

    Returns:
        JsonResponse: Respuesta JSON con error 404
    """
    return JsonResponse({
        'error': 'Not Found',
        'message': 'El recurso solicitado no existe.',
        'status_code': 404
    }, status=404)


@require_GET
def custom_500(request):
    """
    Vista personalizada para errores 500.

    Esta vista no revela información sobre errores internos
    del servidor en producción.

    Args:
        request: HttpRequest object

    Returns:
        JsonResponse: Respuesta JSON con error 500
    """
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'Ha ocurrido un error interno. Por favor, intente nuevamente más tarde.',
        'status_code': 500
    }, status=500)
