# Guía de Despliegue a Producción

## 🚀 Preparación para Producción

### 1. Configurar Variables de Entorno

Crea un archivo `.env` con la configuración de producción:

```env
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# PostgreSQL
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=maderas_prod
DATABASE_USER=maderas_user
DATABASE_PASSWORD=password_seguro
DATABASE_HOST=localhost
DATABASE_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://tudominio.com,https://www.tudominio.com
CSRF_TRUSTED_ORIGINS=https://tudominio.com,https://www.tudominio.com

# Timezone
TIME_ZONE=America/Santiago
LANGUAGE_CODE=es-cl
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Migraciones y Archivos Estáticos

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Crear Superusuario

```bash
python manage.py createsuperuser
```

---

## 🐳 Despliegue con Docker (Recomendado)

### Dockerfile

Crea un `Dockerfile`:

```dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "drfmaderas.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: maderas_db
      POSTGRES_USER: maderas_user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn drfmaderas.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### Ejecutar con Docker

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## ☁️ Despliegue en Heroku

### 1. Instalar Heroku CLI

```bash
brew install heroku/brew/heroku  # macOS
```

### 2. Configurar Procfile

Crea un archivo `Procfile`:

```
web: gunicorn drfmaderas.wsgi:application --log-file -
release: python manage.py migrate
```

### 3. Crear runtime.txt

```
python-3.12.0
```

### 4. Desplegar

```bash
heroku login
heroku create tu-app-maderas
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY="tu-secret-key"
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py createsuperuser
```

---

## 🖥️ Despliegue en VPS (Ubuntu)

### 1. Preparar el Servidor

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

### 2. Configurar PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE maderas_db;
CREATE USER maderas_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE maderas_db TO maderas_user;
\q
```

### 3. Clonar y Configurar el Proyecto

```bash
cd /var/www
git clone tu-repositorio eva1-backend
cd eva1-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configurar Gunicorn

Crea `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn daemon for Django Maderas API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/eva1-backend
EnvironmentFile=/var/www/eva1-backend/.env
ExecStart=/var/www/eva1-backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/eva1-backend/gunicorn.sock \
          drfmaderas.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 5. Configurar Nginx

Crea `/etc/nginx/sites-available/maderas`:

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/eva1-backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/eva1-backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/eva1-backend/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/maderas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Configurar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

## 🔒 Checklist de Seguridad

- [ ] `DEBUG=False` en producción
- [ ] SECRET_KEY única y segura
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] HTTPS habilitado (SSL/TLS)
- [ ] CORS configurado apropiadamente
- [ ] Permisos de API restrictivos
- [ ] Base de datos con credenciales seguras
- [ ] Firewall configurado (solo puertos 80, 443)
- [ ] Backups automáticos de base de datos
- [ ] Logs de aplicación configurados
- [ ] Variables de entorno en archivo .env (no en código)

---

## 📊 Monitoreo y Mantenimiento

### Ver logs de Gunicorn

```bash
sudo journalctl -u gunicorn -f
```

### Ver logs de Nginx

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Reiniciar servicios

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Backup de base de datos

```bash
pg_dump -U maderas_user maderas_db > backup_$(date +%Y%m%d).sql
```

---

## 🆘 Solución de Problemas

### Error 502 Bad Gateway
- Verificar que Gunicorn esté corriendo: `sudo systemctl status gunicorn`
- Revisar logs: `sudo journalctl -u gunicorn -f`

### Archivos estáticos no se cargan
- Ejecutar `python manage.py collectstatic`
- Verificar permisos: `sudo chown -R www-data:www-data staticfiles/`

### Error de conexión a base de datos
- Verificar credenciales en `.env`
- Verificar que PostgreSQL esté corriendo: `sudo systemctl status postgresql`

---

## 📞 Soporte

Para problemas de despliegue, contacta al equipo DevOps.
