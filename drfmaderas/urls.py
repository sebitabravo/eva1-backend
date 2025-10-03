"""
URL configuration for drfmaderas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from decouple import config

# Importar vistas de seguridad
from .views import root_redirect

# Configuración de URL de admin (puede personalizarse para mayor seguridad)
# Por defecto: 'admin/', pero se puede cambiar vía variable de entorno
ADMIN_URL = config('ADMIN_URL', default='admin/')

urlpatterns = [
    # Redireccionar la raíz a /api/ para evitar exponer rutas en página 404
    path('', root_redirect, name='root'),

    # Panel de administración con URL configurable
    path(ADMIN_URL, admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')),
]

# Servir archivos estáticos y media en desarrollo
# WhiteNoise servirá los archivos estáticos en producción automáticamente
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handlers personalizados para errores (solo se usan cuando DEBUG=False)
handler404 = 'drfmaderas.views.custom_404'
handler500 = 'drfmaderas.views.custom_500'
