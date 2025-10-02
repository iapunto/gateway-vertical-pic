@echo off
REM Script para iniciar el descubrimiento de PLCs en Windows

REM Directorio base
set BASE_DIR=%~dp0

REM Cambiar al directorio base
cd /d "%BASE_DIR%"

REM Verificar si el entorno virtual existe
if not exist "gateway_venv" (
    echo El entorno virtual no existe. Por favor ejecute install_gateway.py primero.
    pause
    exit /b 1
)

REM Activar el entorno virtual
call gateway_venv\Scripts\activate.bat

REM Iniciar el descubrimiento de PLCs
echo Iniciando descubrimiento de PLCs...
python discover_plcs.py

REM Desactivar el entorno virtual
call gateway_venv\Scripts\deactivate.bat

pause