#!/bin/bash

# Salir inmediatamente si algún comando interno falla
set -e

echo "========================================================="
echo "⚙️  DataForge CLI - Inicializando instalación automatizada"
echo "========================================================="

# 1. Verificar si Python 3 está instalado en el sistema Linux objetivo
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no se encuentra instalado en este entorno Linux."
    exit 1
fi

echo "➔ Creando entorno virtual de Python (.venv)..."
python3 -m venv .venv

echo "➔ Activando el entorno virtual..."
source .venv/bin/activate

echo "➔ Actualizando administrador de paquetes pip..."
pip install --upgrade pip

echo "➔ Instalando dependencias de producción desde requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  Aviso: No se detectó el archivo requirements.txt en la raíz."
fi

echo "========================================================="
echo "✅ ¡Configuración finalizada con éxito!"
echo "Para correr la CLI ejecuta: source .venv/bin/activate && python main.py --debug"
echo "========================================================="
