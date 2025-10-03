#!/bin/bash
# Entrypoint script para inicializar el contenedor Django

set -e

echo "🚀 Iniciando contenedor Django..."

# Función para esperar a que PostgreSQL esté listo
wait_for_postgres() {
    echo "⏳ Esperando a que PostgreSQL esté listo..."

    until PGPASSWORD=$DATABASE_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -d "$DATABASE_NAME" -c '\q' 2>/dev/null; do
        echo "PostgreSQL no está listo - esperando..."
        sleep 2
    done

    echo "✅ PostgreSQL está listo!"
}

# Esperar a PostgreSQL si DATABASE_HOST está definido
if [ ! -z "$DATABASE_HOST" ]; then
    wait_for_postgres
fi

# Ejecutar migraciones
echo "🔄 Aplicando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Crear datos de prueba y superusuario si la variable está habilitada
if [ "$AUTO_POPULATE_DB" = "True" ] || [ "$AUTO_POPULATE_DB" = "true" ]; then
    echo "🌱 Poblando la base de datos con datos de prueba..."
    python create_test_data.py
fi

echo "✅ Inicialización completa!"
echo "🌐 Iniciando servidor..."

# Ejecutar el comando pasado al contenedor
exec "$@"
