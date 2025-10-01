from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que proporciona campos de timestamp
    para registrar creación y modificación.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Conductor(TimeStampedModel):
    """
    Modelo que representa a un conductor de camión.
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre completo",
        help_text="Nombre completo del conductor"
    )
    licencia_conducir = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Licencia de conducir",
        help_text="Número de licencia de conducir"
    )
    telefono = models.CharField(
        validators=[phone_regex],
        max_length=20,
        verbose_name="Teléfono"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección"
    )

    class Meta:
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['licencia_conducir']),
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.licencia_conducir}"


class Camion(TimeStampedModel):
    """
    Modelo que representa un camión de la flota.
    """
    placa_regex = RegexValidator(
        regex=r'^[A-Z]{2,4}\d{2,4}$',
        message="La placa debe tener formato válido (ej: ABC1234)"
    )

    placa = models.CharField(
        max_length=10,
        unique=True,
        validators=[placa_regex],
        verbose_name="Placa",
        help_text="Placa del camión"
    )
    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo"
    )
    capacidad_carga = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name="Capacidad de carga (toneladas)",
        help_text="Capacidad máxima de carga en toneladas"
    )
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT,
        related_name='camiones',
        verbose_name="Conductor"
    )

    class Meta:
        verbose_name = "Camión"
        verbose_name_plural = "Camiones"
        ordering = ['placa']
        indexes = [
            models.Index(fields=['placa']),
        ]

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

    def clean(self):
        """Validación personalizada"""
        super().clean()
        if self.capacidad_carga and self.capacidad_carga < 0:
            raise ValidationError({
                'capacidad_carga': 'La capacidad de carga debe ser positiva.'
            })


class TipoMadera(TimeStampedModel):
    """
    Modelo que representa los tipos de madera disponibles.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del tipo de madera"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del tipo de madera"
    )

    class Meta:
        verbose_name = "Tipo de madera"
        verbose_name_plural = "Tipos de madera"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Cliente(TimeStampedModel):
    """
    Modelo que representa a un cliente de la empresa.
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )

    nombre_empresa = models.CharField(
        max_length=100,
        verbose_name="Nombre de la empresa"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección"
    )
    telefono = models.CharField(
        validators=[phone_regex],
        max_length=20,
        verbose_name="Teléfono"
    )
    correo_electronico = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre_empresa']
        indexes = [
            models.Index(fields=['nombre_empresa']),
            models.Index(fields=['correo_electronico']),
        ]

    def __str__(self):
        return self.nombre_empresa


class Carga(TimeStampedModel):
    """
    Modelo que representa una carga de madera.
    """
    tipo_madera = models.ForeignKey(
        TipoMadera,
        on_delete=models.PROTECT,
        related_name='cargas',
        verbose_name="Tipo de madera"
    )
    cantidad = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name="Cantidad (unidades)",
        help_text="Cantidad de unidades de madera"
    )
    peso = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name="Peso (toneladas)",
        help_text="Peso total de la carga en toneladas"
    )
    camion = models.ForeignKey(
        Camion,
        on_delete=models.PROTECT,
        related_name='cargas',
        verbose_name="Camión"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='cargas',
        verbose_name="Cliente"
    )

    class Meta:
        verbose_name = "Carga"
        verbose_name_plural = "Cargas"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['camion', 'cliente']),
        ]

    def __str__(self):
        return f"Carga de {self.cantidad} {self.tipo_madera.nombre} para {self.cliente.nombre_empresa}"

    def clean(self):
        """Validación de que la carga no exceda la capacidad del camión"""
        super().clean()
        if self.peso and self.camion and self.peso > self.camion.capacidad_carga:
            raise ValidationError({
                'peso': f'El peso de la carga ({self.peso}t) excede la capacidad del camión ({self.camion.capacidad_carga}t).'
            })
