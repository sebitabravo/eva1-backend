FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Hacer ejecutable el entrypoint
RUN chmod +x /app/docker-entrypoint.sh

# Crear directorios necesarios con permisos apropiados
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

EXPOSE 8000

# Script de entrada
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Usar Gunicorn para producción optimizado para 256MB RAM
# 2 workers + 1 thread = ~150-200MB total
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--worker-class", "gthread", "--timeout", "30", "--max-requests", "1000", "--max-requests-jitter", "50", "--access-logfile", "-", "--error-logfile", "-", "drfmaderas.wsgi:application"]
