#!/bin/bash
# Script para monitorear recursos de los contenedores Docker
# Uso: ./monitor-resources.sh

echo "🔍 Monitoreo de Recursos - API Maderas del Sur"
echo "=============================================="
echo ""

# Verificar que Docker Compose esté corriendo
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Los contenedores no están corriendo"
    echo "Ejecuta: docker-compose up -d"
    exit 1
fi

echo "📊 USO DE CPU Y MEMORIA:"
echo "------------------------"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" maderas_web maderas_db

echo ""
echo "💾 USO DE DISCO (VOLÚMENES):"
echo "----------------------------"

# Obtener tamaño de volúmenes
WEB_VOLUME=$(docker system df -v | grep maderas_static | awk '{print $3}')
DB_VOLUME=$(docker system df -v | grep maderas_postgres_data | awk '{print $3}')
MEDIA_VOLUME=$(docker system df -v | grep maderas_media | awk '{print $3}')

echo "Static files:    ${WEB_VOLUME:-0B}"
echo "Database:        ${DB_VOLUME:-0B}"
echo "Media files:     ${MEDIA_VOLUME:-0B}"

echo ""
echo "🚨 LÍMITES CONFIGURADOS:"
echo "------------------------"
echo "CPU por contenedor:     0.5 cores (50%)"
echo "RAM por contenedor:     256MB"
echo "RAM total objetivo:     512MB"
echo "Disco total objetivo:   10GB"

echo ""
echo "📈 CONEXIONES A LA BASE DE DATOS:"
echo "-----------------------------------"
docker exec maderas_db psql -U maderas_user -d maderas_db -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';" 2>/dev/null || echo "No se pudo consultar la base de datos"

echo ""
echo "⚡ RATE LIMITING (Throttling):"
echo "-------------------------------"
echo "Usuarios anónimos:    100 requests/hora"
echo "Usuarios autenticados: 1000 requests/hora"
echo "Tamaño máximo request: 5MB"

echo ""
echo "💡 COMANDOS ÚTILES:"
echo "-------------------"
echo "Ver logs en vivo:          docker-compose logs -f"
echo "Ver uso de recursos:       docker stats"
echo "Limpiar espacio en disco:  docker system prune -a"
echo "Reiniciar servicios:       docker-compose restart"
echo ""
