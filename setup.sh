#!/bin/bash

# Script de configuración inicial para el proyecto
# Uso: bash setup.sh

echo "🚀 Iniciando configuración del proyecto..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si existe Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 encontrado${NC}"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "${YELLOW}⚠️  El entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Verificar si existe archivo .env
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edita el archivo .env con tu configuración${NC}"
else
    echo -e "${YELLOW}⚠️  El archivo .env ya existe${NC}"
fi

# Eliminar migraciones antiguas y base de datos
echo "🗑️  Limpiando migraciones antiguas..."
rm -f api/migrations/0*.py
rm -f db.sqlite3

# Crear nuevas migraciones
echo "🔄 Creando nuevas migraciones..."
python manage.py makemigrations

# Aplicar migraciones
echo "⚙️  Aplicando migraciones..."
python manage.py migrate

# Preguntar si desea crear superusuario
echo ""
read -p "¿Deseas crear un superusuario? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[SsYy]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo -e "${GREEN}✅ ¡Configuración completada!${NC}"
echo ""
echo "📋 Próximos pasos:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Edita el archivo .env si es necesario"
echo "  3. Ejecuta el servidor: python manage.py runserver"
echo ""
echo "🌐 La API estará disponible en: http://localhost:8000/api/"
echo "🔐 Panel admin en: http://localhost:8000/admin/"
echo ""
echo -e "${GREEN}¡Listo para desarrollar! 🎉${NC}"
