# 🚛 API Maderas del Sur S.A.

[![Django](https://img.shields.io/badge/Django-5.1.1-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

API RESTful profesional desarrollada con Django REST Framework para gestionar la logística de transporte de madera. Sistema completo de gestión de flota de camiones, conductores, tipos de madera, cargas y clientes.

## 🎯 Características Principales

- ✅ **CRUD completo** para todas las entidades
- 🔐 **Autenticación por token** (JWT-ready)
- 🔍 **Búsqueda y filtros** avanzados
- 📊 **Endpoints de estadísticas** personalizados
- 📄 **Paginación** automática
- ✨ **Validaciones robustas** de negocio
- 🎨 **API navegable** (Browsable API)
- 📝 **Documentación completa** de endpoints
- 🌐 **CORS** configurado
- 🛡️ **Seguridad** mejorada para producción

## 🏗️ Arquitectura

```
eva1-backend/
├── api/                    # Aplicación principal
│   ├── models.py          # Modelos con validaciones
│   ├── serializers.py     # Serializers con campos explícitos
│   ├── views.py           # ViewSets con filtros y acciones
│   ├── admin.py           # Admin personalizado
│   └── urls.py            # Rutas de la API
├── drfmaderas/            # Configuración del proyecto
│   ├── settings.py        # Settings con variables de entorno
│   └── urls.py            # URLs principales
├── .env                   # Variables de entorno (no versionado)
├── .env.example           # Ejemplo de configuración
├── requirements.txt       # Dependencias con versiones
├── INSTALLATION.md        # Guía de instalación detallada
├── API_DOCUMENTATION.md   # Documentación de endpoints
└── DEPLOYMENT.md          # Guía de despliegue
```

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/sebitabravo/maderaapi.git
cd eva1-backend
```

### 2. Configurar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tu configuración
```

### 5. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor

```bash
python manage.py runserver
```

🎉 **API disponible en:** `http://localhost:8000/api/`

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| [INSTALLATION.md](INSTALLATION.md) | Guía completa de instalación |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Documentación de todos los endpoints |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Guía de despliegue a producción |

## 🔌 Endpoints Principales

### Base URL: `/api/`

| Recurso | Endpoint | Descripción |
|---------|----------|-------------|
| **Conductores** | `/api/conductores/` | CRUD de conductores |
| **Camiones** | `/api/camiones/` | CRUD de camiones con estadísticas |
| **Tipos de Madera** | `/api/tipos-madera/` | CRUD de tipos de madera |
| **Clientes** | `/api/clientes/` | CRUD de clientes con estadísticas |
| **Cargas** | `/api/cargas/` | CRUD de cargas con validaciones |
| **Auth** | `/api/auth/token/` | Obtener token de autenticación |

### Endpoints Adicionales

- `GET /api/camiones/{id}/estadisticas/` - Estadísticas por camión
- `GET /api/clientes/{id}/estadisticas/` - Estadísticas por cliente
- `GET /api/cargas/estadisticas_generales/` - Estadísticas generales
- `GET /api/conductores/{id}/camiones/` - Camiones por conductor

## 🔐 Autenticación

Obtener token:

```bash
POST /api/auth/token/
Content-Type: application/json

{
  "username": "tu_usuario",
  "password": "tu_password"
}
```

Usar token en requests:

```bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## 📊 Modelos de Datos

### Conductor
- Nombre, licencia de conducir (única), teléfono, dirección
- Validaciones: formato de teléfono, licencia mínima 5 caracteres

### Camión
- Placa (única), modelo, capacidad de carga, conductor
- Validaciones: formato de placa, capacidad > 0
- Relación: `PROTECT` con Conductor

### Tipo de Madera
- Nombre (único), descripción

### Cliente
- Nombre empresa, dirección, teléfono, correo (único)
- Validaciones: formato de teléfono y email

### Carga
- Tipo de madera, cantidad, peso, camión, cliente
- Validación crítica: **peso ≤ capacidad del camión**
- Timestamps: `created_at`, `updated_at`

## 🛠️ Tecnologías

| Categoría | Tecnologías |
|-----------|-------------|
| **Backend** | Django 5.1.1, Django REST Framework 3.15.2 |
| **Base de Datos** | SQLite (dev), PostgreSQL (prod) |
| **Autenticación** | Token Authentication |
| **Seguridad** | CORS, CSRF protection, variables de entorno |
| **Servidor** | Gunicorn, Whitenoise |
| **Testing** | Pytest, Coverage |
| **Code Quality** | Black, Flake8, Isort |

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
coverage run -m pytest
coverage report
```

## 🔒 Mejoras de Seguridad Implementadas

- ✅ `SECRET_KEY` en variables de entorno
- ✅ `DEBUG=False` en producción
- ✅ `ALLOWED_HOSTS` configurado
- ✅ HTTPS ready (HSTS, SSL redirect)
- ✅ CORS configurado apropiadamente
- ✅ Validaciones robustas en modelos y serializers
- ✅ Permisos: `IsAuthenticatedOrReadOnly`
- ✅ Constraints de base de datos (unique, indexes)

## 📈 Mejoras Implementadas vs Versión Original

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Nombres de clases** | minúsculas ❌ | PascalCase ✅ |
| **SECRET_KEY** | Hardcoded ❌ | Variables de entorno ✅ |
| **Validaciones** | Básicas | Validaciones de negocio completas ✅ |
| **Serializers** | `fields = '__all__'` ❌ | Campos explícitos ✅ |
| **Timestamps** | No ❌ | `created_at`, `updated_at` ✅ |
| **Índices DB** | No ❌ | Indexes optimizados ✅ |
| **Related names** | No ❌ | Relaciones inversas ✅ |
| **Filtros** | No ❌ | Búsqueda y filtros avanzados ✅ |
| **Estadísticas** | No ❌ | Endpoints de analytics ✅ |
| **Documentación** | Básica | Completa (3 archivos MD) ✅ |
| **Admin** | Básico | Personalizado con filtros ✅ |
| **Seguridad** | Desarrollo | Production-ready ✅ |

## 🚀 Despliegue

### Docker

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Heroku

```bash
heroku create tu-app
heroku addons:create heroku-postgresql
git push heroku main
```

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para guías completas de despliegue.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Convenciones de Código

- **PEP 8** para Python
- **Black** para formateo
- **Docstrings** en español
- **Commits** descriptivos en español

## 📞 Soporte y Contacto

- **Issues**: [GitHub Issues](https://github.com/sebitabravo/maderaapi/issues)
- **Documentación**: Ver archivos MD en el repositorio
- **Admin Panel**: `http://localhost:8000/admin/`

## 📄 Licencia

Este proyecto fue desarrollado como parte de una evaluación de backend para la Universidad Tecnológica de Chile INACAP.

---

**Desarrollado con ❤️ para Maderas del Sur S.A.**
