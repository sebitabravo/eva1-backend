from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'conductores', views.conductorViewSet)
router.register(r'camiones', views.camionViewSet)
router.register(r'tipos_madera', views.tipo_maderaViewSet)
router.register(r'clientes', views.clienteViewSet)
router.register(r'cargas', views.cargaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
