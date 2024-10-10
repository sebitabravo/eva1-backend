from django.contrib import admin
from .models import conductor, camion, tipo_madera, cliente, carga

# Register your models here.
admin.site.register(conductor)
admin.site.register(camion)
admin.site.register(tipo_madera)
admin.site.register(cliente)
admin.site.register(carga)
