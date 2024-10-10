from rest_framework import viewsets
from .models import conductor, camion, tipo_madera, cliente, carga
from .serializer import conductorSerializer, camionSerializer, tipo_maderaSerializer, clienteSerializer, cargaSerializer

# Create your views here.


class conductorViewSet(viewsets.ModelViewSet):
    queryset = conductor.objects.all()
    serializer_class = conductorSerializer


class camionViewSet(viewsets.ModelViewSet):
    queryset = camion.objects.all()
    serializer_class = camionSerializer


class tipo_maderaViewSet(viewsets.ModelViewSet):
    queryset = tipo_madera.objects.all()
    serializer_class = tipo_maderaSerializer


class clienteViewSet(viewsets.ModelViewSet):
    queryset = cliente.objects.all()
    serializer_class = clienteSerializer


class cargaViewSet(viewsets.ModelViewSet):
    queryset = carga.objects.all()
    serializer_class = cargaSerializer
