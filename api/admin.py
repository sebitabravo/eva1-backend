from django.contrib import admin
from .models import Conductor, Camion, TipoMadera, Cliente, Carga


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    """Administración personalizada para Conductor"""
    list_display = ['nombre', 'licencia_conducir', 'telefono', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['nombre', 'licencia_conducir', 'telefono']
    ordering = ['nombre']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'licencia_conducir')
        }),
        ('Contacto', {
            'fields': ('telefono', 'direccion')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    """Administración personalizada para Camion"""
    list_display = ['placa', 'modelo', 'capacidad_carga', 'conductor', 'created_at']
    list_filter = ['conductor', 'created_at']
    search_fields = ['placa', 'modelo', 'conductor__nombre']
    ordering = ['placa']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['conductor']
    fieldsets = (
        ('Información del Camión', {
            'fields': ('placa', 'modelo', 'capacidad_carga')
        }),
        ('Conductor Asignado', {
            'fields': ('conductor',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TipoMadera)
class TipoMaderaAdmin(admin.ModelAdmin):
    """Administración personalizada para TipoMadera"""
    list_display = ['nombre', 'created_at']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Administración personalizada para Cliente"""
    list_display = ['nombre_empresa', 'correo_electronico', 'telefono', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['nombre_empresa', 'correo_electronico', 'telefono']
    ordering = ['nombre_empresa']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('nombre_empresa', 'direccion')
        }),
        ('Contacto', {
            'fields': ('telefono', 'correo_electronico')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    """Administración personalizada para Carga"""
    list_display = ['id', 'tipo_madera', 'cantidad', 'peso', 'camion', 'cliente', 'created_at']
    list_filter = ['tipo_madera', 'camion', 'cliente', 'created_at']
    search_fields = ['tipo_madera__nombre', 'camion__placa', 'cliente__nombre_empresa']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['tipo_madera', 'camion', 'cliente']
    fieldsets = (
        ('Información de la Carga', {
            'fields': ('tipo_madera', 'cantidad', 'peso')
        }),
        ('Asignaciones', {
            'fields': ('camion', 'cliente')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('tipo_madera', 'camion', 'cliente')


# Personalización del sitio admin
admin.site.site_header = "Administración - Maderas del Sur S.A."
admin.site.site_title = "Maderas del Sur"
admin.site.index_title = "Panel de Administración"
