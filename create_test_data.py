#!/usr/bin/env python
"""
Script para crear una gran cantidad de datos de prueba en la base de datos.
"""
import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drfmaderas.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Conductor, Camion, TipoMadera, Cliente, Carga

# Inicializar Faker para generar datos falsos realistas
fake = Faker('es_ES') # Usar localización en español

def crear_superusuario():
    """Crea un superusuario si no existe usando variables de entorno"""
    username = os.getenv('DJANGO_SUPERUSER_USERNAME')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if not all([username, email, password]):
        print("⚠️  Variables de entorno de superusuario no configuradas. Saltando creación.")
        return

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superusuario creado: {username}")
    else:
        print(f"ℹ️  Superusuario '{username}' ya existe")

def limpiar_base_de_datos():
    """Elimina todos los datos de los modelos para evitar duplicados en ejecuciones repetidas"""
    print("\n🧹 Limpiando la base de datos antigua...")
    Carga.objects.all().delete()
    Camion.objects.all().delete()
    Conductor.objects.all().delete()
    Cliente.objects.all().delete()
    TipoMadera.objects.all().delete()
    print("✅ Base de datos limpiada.")

def crear_datos_prueba(
    num_conductores=50, 
    num_camiones=80, 
    num_clientes=100, 
    num_cargas=1000
):
    """Crea una gran cantidad de datos de prueba para la API"""

    # 1. Crear Tipos de Madera
    print("\n🌲 Creando tipos de madera...")
    tipos_data = [
        {"nombre": "Pino Radiata", "descripcion": "Madera de pino de crecimiento rápido, ideal para construcción y carpintería."},
        {"nombre": "Roble Pellín", "descripcion": "Madera nativa de alta durabilidad, perfecta para estructuras y muebles de lujo."},
        {"nombre": "Eucalipto", "descripcion": "Madera resistente a la humedad, excelente para postes y uso exterior."},
        {"nombre": "Lenga", "descripcion": "Madera nativa de la Patagonia, apreciada por su veta y color para ebanistería."},
        {"nombre": "Raulí", "descripcion": "Madera nativa noble de color rojizo, usada en puertas, ventanas y muebles finos."},
        {"nombre": "Mañío", "descripcion": "Madera de color claro y grano fino, fácil de trabajar, usada en chapas y molduras."},
        {"nombre": "Coihue", "descripcion": "Madera versátil y resistente, común en la construcción y leña."},
        {"nombre": "Alerce", "descripcion": "Madera nativa protegida, muy valorada por su resistencia a la putrefacción."},
        {"nombre": "Ciprés de las Guaitecas", "descripcion": "Madera aromática y duradera, usada en construcción y artesanía."},
        {"nombre": "Tepa", "descripcion": "Madera de color pálido, usada principalmente para cajas y embalajes."},
        {"nombre": "Lingue", "descripcion": "Madera de excelente calidad para muebles y chapas decorativas."},
        {"nombre": "Pino Oregón", "descripcion": "Madera importada, muy apreciada para vigas y estructuras a la vista."},
        {"nombre": "Nogal", "descripcion": "Madera oscura y veteada, de alto valor para muebles de lujo y chapas."},
        {"nombre": "Castaño", "descripcion": "Madera resistente y flexible, usada en tonelería y muebles."},
        {"nombre": "Fresno", "descripcion": "Madera dura y elástica, ideal para artículos deportivos y mangos de herramientas."},
    ]

    tipos_madera = []
    for data in tipos_data:
        tipo, created = TipoMadera.objects.get_or_create(nombre=data['nombre'], defaults=data)
        tipos_madera.append(tipo)
        if created:
            print(f"  ✓ Tipo de madera creado: {tipo.nombre}")
    
    if not tipos_madera:
        raise Exception("No se pudieron crear los tipos de madera. Abortando.")

    # 2. Crear Conductores
    print(f"\n📝 Creando {num_conductores} conductores...")
    conductores = []
    for _ in range(num_conductores):
        nombre = fake.first_name() + " " + fake.last_name()
        licencia = fake.unique.bothify(text='??######').upper()
        conductor, created = Conductor.objects.get_or_create(
            licencia_conducir=licencia,
            defaults={
                "nombre": nombre,
                "telefono": fake.phone_number(),
                "direccion": fake.address()
            }
        )
        conductores.append(conductor)
    print(f"  ✓ {len(conductores)} conductores creados.")
    
    if not conductores:
        raise Exception("No se pudieron crear conductores. Abortando.")

    # 3. Crear Camiones
    print(f"\n🚛 Creando {num_camiones} camiones...")
    camiones = []
    for _ in range(num_camiones):
        placa = fake.unique.bothify(text='????##').upper()
        camion, created = Camion.objects.get_or_create(
            placa=placa,
            defaults={
                "modelo": random.choice(["Ford Cargo", "Mercedes-Benz Actros", "Scania R-Series", "Volvo FH", "MAN TGX", "Iveco Stralis"]),
                "capacidad_carga": round(random.uniform(10.0, 30.0), 1),
                "conductor": random.choice(conductores)
            }
        )
        camiones.append(camion)
    print(f"  ✓ {len(camiones)} camiones creados.")

    if not camiones:
        raise Exception("No se pudieron crear camiones. Abortando.")

    # 4. Crear Clientes
    print(f"\n🏢 Creando {num_clientes} clientes...")
    clientes = []
    for _ in range(num_clientes):
        cliente, created = Cliente.objects.get_or_create(
            correo_electronico=fake.unique.email(),
            defaults={
                "nombre_empresa": fake.company() + " " + fake.company_suffix(),
                "direccion": fake.address(),
                "telefono": fake.phone_number()
            }
        )
        clientes.append(cliente)
    print(f"  ✓ {len(clientes)} clientes creados.")

    if not clientes:
        raise Exception("No se pudieron crear clientes. Abortando.")

    # 5. Crear Cargas
    print(f"\n📦 Creando {num_cargas} cargas...")
    cargas = []
    for i in range(num_cargas):
        camion_seleccionado = random.choice(camiones)
        peso_carga = round(random.uniform(5.0, camion_seleccionado.capacidad_carga), 1)
        
        carga = Carga.objects.create(
            tipo_madera=random.choice(tipos_madera),
            cantidad=random.randint(50, 200),
            peso=peso_carga,
            camion=camion_seleccionado,
            cliente=random.choice(clientes)
        )
        cargas.append(carga)
        # Imprimir progreso para que no parezca colgado
        if (i + 1) % 100 == 0:
            print(f"  ... {i + 1}/{num_cargas} cargas creadas")

    print(f"  ✓ {len(cargas)} cargas creadas.")

    print("\n" + "="*60)
    print("✅ Datos de prueba creados exitosamente!")
    print("="*60)
    print("\n📊 Resumen:")
    print(f"  - Conductores: {Conductor.objects.count()}")
    print(f"  - Camiones: {Camion.objects.count()}")
    print(f"  - Tipos de Madera: {TipoMadera.objects.count()}")
    print(f"  - Clientes: {Cliente.objects.count()}")
    print(f"  - Cargas: {Carga.objects.count()}")

    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    print(f"\n🔐 Superusuario: {username}")
    print("\n🌐 URLs importantes:")
    print("  - API: http://localhost:8000/api/")
    print("  - Admin: http://localhost:8000/admin/")
    print("  - Auth Token: http://localhost:8000/api/auth/token/")

if __name__ == '__main__':
    # Instalar Faker si no está presente
    try:
        import faker
    except ImportError:
        print("🐍 Instalando librería 'Faker' para generar datos de prueba...")
        os.system('pip install Faker')
        from faker import Faker

    print("🚀 Iniciando creación de datos de prueba...")
    print("="*60)
    
    # Limpiar datos antiguos para no crear duplicados
    limpiar_base_de_datos()
    
    # Crear superusuario y datos de prueba
    crear_superusuario()
    crear_datos_prueba()