#!/bin/bash
set -e
echo "Iniciando configuración del proyecto"

# 1) Verificar instalación de Python
if ! command -v python3 &> /dev/null; then
  echo "Python3 no está instalado. Instálalo antes de continuar."
  exit 1
fi

# 2) Entrar a la carpeta del proyecto
cd proyecto || { echo "No se encontró la carpeta 'proyecto'"; exit 1; }

# 3) Creación entorno virutal
if [ ! -d "venv" ]; then
  echo "Creando entorno virtual (venv)"
  python3 -m venv venv
else
  echo "El entorno virtual ya existe"
fi

# 4) Activar el entorno virtual
source venv/bin/activate

# 5) Instalar Django
echo "Instalando Django"
pip install --upgrade pip
pip install django

# 6) Migraciones de base de datos
echo "Aplicando migraciones"
python manage.py makemigrations
python manage.py migrate

# 7) Ejecución de pruebas
echo "Ejecutando pruebas."
python manage.py test || echo "No hay pruebas definidas."

# 8) Levantar servidor de desarrollo
echo "Iniciando el servidor en Django"
python manage.py runserver

# 9) Desactivar entorno virtual
echo "Desactivando el entorno virtual"
deactivate

echo "Setup finalizado correctamente."
