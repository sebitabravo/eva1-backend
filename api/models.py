from django.db import models

# Create your models here.


class conductor(models.Model):
    nombre = models.CharField(max_length=100)
    licencia_conducir = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class camion(models.Model):
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=50)
    capacidad_carga = models.FloatField()
    conductor = models.ForeignKey(conductor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"


class tipo_madera(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class cliente(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correo_electronico = models.EmailField()

    def __str__(self):
        return self.nombre_empresa


class carga(models.Model):
    tipo_madera = models.ForeignKey(tipo_madera, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    peso = models.FloatField()
    camion = models.ForeignKey(camion, on_delete=models.CASCADE)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carga de {self.cantidad} {self.tipo_madera.nombre} para {self.cliente.nombre_empresa}"
