# Guía de Instalación - API Maderas del Sur S.A.

## 📋 Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)
- PostgreSQL (para producción, opcional para desarrollo)

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/sebitabravo/maderaapi.git
cd eva1-backend
```

### 2. Crear y Activar el Entorno Virtual

**En Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura tus variables:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generar SECRET_KEY segura:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Realizar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/`

## 🔧 Configuración para Producción

### Base de Datos PostgreSQL

1. Instala PostgreSQL en tu servidor
2. Crea una base de datos:
   ```sql
   CREATE DATABASE maderas_db;
   CREATE USER maderas_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE maderas_db TO maderas_user;
   ```

3. Actualiza tu `.env`:
   ```env
   DEBUG=False
   DATABASE_ENGINE=django.db.backends.postgresql
   DATABASE_NAME=maderas_db
   DATABASE_USER=maderas_user
   DATABASE_PASSWORD=password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

### Archivos Estáticos

```bash
python manage.py collectstatic
```

### Ejecutar con Gunicorn

```bash
gunicorn drfmaderas.wsgi:application --bind 0.0.0.0:8000
```

## 🧪 Ejecutar Tests

```bash
pytest
```

Con cobertura:
```bash
coverage run -m pytest
coverage report
```

## 📚 Documentación de la API

Una vez que el servidor esté corriendo, accede a:

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Auth Token**: http://localhost:8000/api/auth/token/

## 🔐 Autenticación

Para obtener un token de autenticación:

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'
```

Usa el token en tus requests:

```bash
curl -H "Authorization: Token tu_token_aqui" http://localhost:8000/api/camiones/
```

## ⚠️ Solución de Problemas

### Error: ModuleNotFoundError

Asegúrate de que el entorno virtual esté activado y las dependencias instaladas:
```bash
pip install -r requirements.txt
```

### Error: SECRET_KEY not found

Verifica que el archivo `.env` exista y contenga `SECRET_KEY`.

### Error de conexión a la base de datos

Verifica las credenciales en `.env` y que PostgreSQL esté corriendo.

## 📞 Soporte

Para más información, contacta al equipo de desarrollo.
