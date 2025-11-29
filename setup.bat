@echo off
setlocal
echo Iniciando configuración del proyecto

REM 1) Verificar instalación de Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python no está instalado. Instálalo antes de continuar.
    exit /b 1
)

REM 2) Entrar a la carpeta del proyecto
cd proyecto || (echo No se encontró la carpeta 'proyecto' & exit /b 1)

REM 3) Creación de entorno virtual
if not exist "venv\" (
    echo Creando entorno virtual (venv)
    python -m venv venv
) else (
    echo El entorno virtual ya existe
)

REM 4) Activar entorno virtual
call venv\Scripts\activate.bat

REM 5) Instalar Django
echo Instalando Django
python -m pip install --upgrade pip
pip install django

REM 6) Migraciones de base de datos
echo Aplicando migraciones
python manage.py makemigrations
python manage.py migrate

REM 7) Ejecución de pruebas
echo Ejecutando pruebas
python manage.py test || echo No hay pruebas definidas.

REM 8) Levantar servidor de desarrollo
echo Iniciando el servidor de Django
python manage.py runserver

REM 9) Desactivar entorno virtual
echo Desactivando el entorno virtual
deactivate

echo Setup finalizado correctamente.
pause
