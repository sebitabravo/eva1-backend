#!/usr/bin/env python
"""
Script para crear datos de prueba en la base de datos
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfmaderas.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Conductor, Camion, TipoMadera, Cliente, Carga

def crear_superusuario():
    """Crea un superusuario si no existe"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@maderas.cl',
            password='admin123'
        )
        print("✅ Superusuario creado: admin / admin123")
    else:
        print("ℹ️  Superusuario 'admin' ya existe")

def crear_datos_prueba():
    """Crea datos de prueba para la API"""

    # Crear Conductores
    print("\n📝 Creando conductores...")
    conductores_data = [
        {"nombre": "Juan Pérez", "licencia_conducir": "A12345", "telefono": "+56912345678", "direccion": "Av. Principal 123, Santiago"},
        {"nombre": "María González", "licencia_conducir": "B67890", "telefono": "+56987654321", "direccion": "Calle Los Aromos 456, Valparaíso"},
        {"nombre": "Carlos Rodríguez", "licencia_conducir": "C11223", "telefono": "+56911223344", "direccion": "Paseo del Mar 789, Viña del Mar"},
    ]

    conductores = []
    for data in conductores_data:
        conductor, created = Conductor.objects.get_or_create(
            licencia_conducir=data['licencia_conducir'],
            defaults=data
        )
        conductores.append(conductor)
        if created:
            print(f"  ✓ Conductor creado: {conductor.nombre}")

    # Crear Camiones
    print("\n🚛 Creando camiones...")
    camiones_data = [
        {"placa": "ABC1234", "modelo": "Ford F-150", "capacidad_carga": 5.5, "conductor": conductores[0]},
        {"placa": "XYZ5678", "modelo": "Chevrolet Silverado", "capacidad_carga": 6.0, "conductor": conductores[1]},
        {"placa": "DEF9012", "modelo": "Toyota Hilux", "capacidad_carga": 4.5, "conductor": conductores[2]},
    ]

    camiones = []
    for data in camiones_data:
        camion, created = Camion.objects.get_or_create(
            placa=data['placa'],
            defaults=data
        )
        camiones.append(camion)
        if created:
            print(f"  ✓ Camión creado: {camion.placa} - {camion.modelo}")

    # Crear Tipos de Madera
    print("\n🌲 Creando tipos de madera...")
    tipos_data = [
        {"nombre": "Pino Radiata", "descripcion": "Madera de pino de crecimiento rápido, ideal para construcción y carpintería"},
        {"nombre": "Roble", "descripcion": "Madera noble de alta durabilidad, perfecta para muebles de lujo"},
        {"nombre": "Eucalipto", "descripcion": "Madera resistente a la humedad, excelente para exteriores"},
    ]

    tipos_madera = []
    for data in tipos_data:
        tipo, created = TipoMadera.objects.get_or_create(
            nombre=data['nombre'],
            defaults=data
        )
        tipos_madera.append(tipo)
        if created:
            print(f"  ✓ Tipo de madera creado: {tipo.nombre}")

    # Crear Clientes
    print("\n🏢 Creando clientes...")
    clientes_data = [
        {"nombre_empresa": "Constructora Los Andes S.A.", "direccion": "Av. Las Condes 123, Santiago", "telefono": "+56987654321", "correo_electronico": "contacto@losandes.cl"},
        {"nombre_empresa": "Mueblería El Bosque Ltda.", "direccion": "Calle Comercio 456, Concepción", "telefono": "+56912345678", "correo_electronico": "ventas@elbosque.cl"},
        {"nombre_empresa": "Inmobiliaria Costa Sur", "direccion": "Av. Costanera 789, La Serena", "telefono": "+56911223344", "correo_electronico": "info@costasur.cl"},
    ]

    clientes = []
    for data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            correo_electronico=data['correo_electronico'],
            defaults=data
        )
        clientes.append(cliente)
        if created:
            print(f"  ✓ Cliente creado: {cliente.nombre_empresa}")

    # Crear Cargas
    print("\n📦 Creando cargas...")
    cargas_data = [
        {"tipo_madera": tipos_madera[0], "cantidad": 100, "peso": 5.0, "camion": camiones[0], "cliente": clientes[0]},
        {"tipo_madera": tipos_madera[1], "cantidad": 50, "peso": 4.0, "camion": camiones[1], "cliente": clientes[1]},
        {"tipo_madera": tipos_madera[2], "cantidad": 75, "peso": 3.5, "camion": camiones[2], "cliente": clientes[2]},
        {"tipo_madera": tipos_madera[0], "cantidad": 120, "peso": 5.5, "camion": camiones[0], "cliente": clientes[1]},
        {"tipo_madera": tipos_madera[1], "cantidad": 60, "peso": 4.5, "camion": camiones[1], "cliente": clientes[0]},
    ]

    for data in cargas_data:
        carga, created = Carga.objects.get_or_create(
            tipo_madera=data['tipo_madera'],
            camion=data['camion'],
            cliente=data['cliente'],
            peso=data['peso'],
            defaults=data
        )
        if created:
            print(f"  ✓ Carga creada: {carga.cantidad} {carga.tipo_madera.nombre} para {carga.cliente.nombre_empresa}")

    print("\n" + "="*60)
    print("✅ Datos de prueba creados exitosamente!")
    print("="*60)
    print("\n📊 Resumen:")
    print(f"  - Conductores: {Conductor.objects.count()}")
    print(f"  - Camiones: {Camion.objects.count()}")
    print(f"  - Tipos de Madera: {TipoMadera.objects.count()}")
    print(f"  - Clientes: {Cliente.objects.count()}")
    print(f"  - Cargas: {Carga.objects.count()}")
    print("\n🔐 Credenciales de acceso:")
    print("  Usuario: admin")
    print("  Password: admin123")
    print("\n🌐 URLs importantes:")
    print("  - API: http://localhost:8000/api/")
    print("  - Admin: http://localhost:8000/admin/")
    print("  - Auth Token: http://localhost:8000/api/auth/token/")

if __name__ == '__main__':
    print("🚀 Iniciando creación de datos de prueba...")
    print("="*60)
    crear_superusuario()
    crear_datos_prueba()
