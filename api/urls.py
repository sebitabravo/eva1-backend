from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views

router = routers.DefaultRouter()
router.register(r'conductores', views.ConductorViewSet, basename='conductor')
router.register(r'camiones', views.CamionViewSet, basename='camion')
router.register(r'tipos-madera', views.TipoMaderaViewSet, basename='tipo-madera')
router.register(r'clientes', views.ClienteViewSet, basename='cliente')
router.register(r'cargas', views.CargaViewSet, basename='carga')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('health/', views.health_check, name='health_check'),
]
