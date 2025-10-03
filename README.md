# 🌲 API Maderas del Sur

[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)

> **Mi primera API REST** - Desarrollada originalmente como evaluación de backend para INACAP. Este proyecto representa mi primera incursión en el desarrollo de APIs profesionales con Django REST Framework.

API RESTful pública para gestión de logística y transporte de madera en la empresa ficticia "Maderas del Sur S.A.". Actualmente optimizada para producción con Docker, rate limiting y despliegue en servidor con recursos limitados.

## 📖 Contexto del Proyecto

Este proyecto fue desarrollado como **evaluación final del módulo de backend** en INACAP, representando mi primera experiencia completa construyendo una API RESTful desde cero.

**Evolución del proyecto:**

- **Versión 1.0** (2024): API básica con SQLite, CRUD completo y admin de Django
- **Versión 2.0** (2025): Refactorización completa con PostgreSQL, Docker, seguridad mejorada y optimización para producción

La API gestiona la logística de transporte de madera, incluyendo flota de camiones, conductores, tipos de madera, cargas y clientes.

## 🗄️ Modelo de Datos

La base de datos está modelada para gestionar la logística completa de transporte:

1. **Conductor**: Nombre, licencia de conducir, teléfono, dirección
2. **Camión**: Placa, modelo, capacidad de carga, conductor asignado
3. **Tipo de Madera**: Nombre, descripción
4. **Cliente**: Nombre de empresa, dirección, teléfono, correo
5. **Carga**: Tipo de madera, cantidad, peso, camión, cliente

Todas las entidades incluyen timestamps automáticos (`created_at`, `updated_at`).

## ✨ Features

- API pública de solo lectura (sin autenticación)
- Protección contra abuso con rate limiting restrictivo
- Cache en endpoints costosos (15 minutos)
- Paginación limitada (máx 100 resultados)
- Escritura solo para administradores
- Optimizada para 512MB RAM / 1 CPU core

## ⚡ Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/sebitabravo/maderaapi.git
cd eva1-backend

# Levantar con Docker
docker-compose up -d --build

# API disponible en http://localhost:3002/api/
```

## 📋 Endpoints

| Recurso | Endpoint | Métodos |
|---------|----------|---------|
| Conductores | `/api/conductores/` | GET, POST*, PUT*, DELETE* |
| Camiones | `/api/camiones/` | GET, POST*, PUT*, DELETE* |
| Tipos Madera | `/api/tipos-madera/` | GET, POST*, PUT*, DELETE* |
| Clientes | `/api/clientes/` | GET, POST*, PUT*, DELETE* |
| Cargas | `/api/cargas/` | GET, POST*, PUT*, DELETE* |
| Estadísticas Camión | `/api/camiones/{id}/estadisticas/` | GET |
| Estadísticas Cliente | `/api/clientes/{id}/estadisticas/` | GET |
| Estadísticas Generales | `/api/cargas/estadisticas_generales/` | GET |
| Autenticación | `/api/auth/token/` | POST |

_*Requiere autenticación y permisos de administrador_

## 🔒 Rate Limiting

| Tipo | Límite | Descripción |
|------|--------|-------------|
| Anónimo | 30/hora | Usuarios sin autenticación |
| Autenticado | 500/hora | Usuarios con token |
| Burst | 10/minuto | Prevención de ráfagas (todas las IPs) |
| Estadísticas | 5/hora | Endpoints de agregaciones |
| Escritura | 10/hora | Operaciones POST/PUT/DELETE |

### Respuesta HTTP 429

```json
{
  "detail": "Request was throttled. Expected available in 45 seconds."
}
```

## 🔑 Autenticación

### Obtener Token

```bash
curl -X POST http://localhost:3002/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```

### Usar Token

```bash
curl -H "Authorization: Token your-token-here" \
  http://localhost:3002/api/conductores/
```

## 🐳 Docker

### Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Monitorear recursos (CPU/RAM/Disco)
./monitor-resources.sh

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Acceder a shell de Django
docker-compose exec web python manage.py shell

# Detener servicios
docker-compose down
```

### Límites de Recursos

```yaml
web:
  deploy:
    resources:
      limits:
        cpus: '0.5'
        memory: 256M
db:
  deploy:
    resources:
      limits:
        cpus: '0.5'
        memory: 256M
```

## 🌍 Variables de Entorno

```bash
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,api-madera.sbravo.app

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=maderas_db
DATABASE_USER=maderas_user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=db
DATABASE_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.com
CSRF_TRUSTED_ORIGINS=https://your-frontend.com

# Puerto
HOST_PORT=3002
```

## 🛠️ Tecnologías

- **Backend:** Django 5.1, Django REST Framework 3.15
- **Base de Datos:** PostgreSQL 16
- **Server:** Gunicorn (2 workers, 2 threads)
- **Containerización:** Docker, Docker Compose
- **Python:** 3.12+

## 📊 Paginación

- Tamaño por defecto: 20 resultados
- Máximo permitido: 100 resultados
- Uso: `?page=2&page_size=50`

## 📝 Logs

Los logs se rotan automáticamente:

- Tamaño máximo: 10MB por archivo
- Archivos máximos: 3 (30MB total por contenedor)
- Ubicación: `/app/logs/throttle.log` (dentro del contenedor)

```bash
# Ver logs de throttling
docker-compose exec web cat /app/logs/throttle.log

# Seguir logs en tiempo real
docker-compose exec web tail -f /app/logs/throttle.log
```

## 🔧 Desarrollo Local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear datos de prueba
python create_test_data.py

# Iniciar servidor de desarrollo
python manage.py runserver

# API disponible en http://localhost:8000/api/
```

## 📈 Monitoreo

```bash
# Ver uso de recursos en tiempo real
docker stats maderas_web maderas_db

# Ver tamaño de volúmenes
docker system df -v

# Ver conexiones activas a la DB
docker-compose exec db psql -U maderas_user -d maderas_db -c "SELECT count(*) FROM pg_stat_activity;"
```

## 🆘 Troubleshooting

### Error de permisos en logs

```bash
docker-compose exec web ls -la /app/logs
docker-compose restart web
```

### Reconstruir contenedores

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Resetear base de datos

```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

---

**Desarrollado por [Sebastián Bravo](https://github.com/sebitabravo)**
