@echo off
REM Script para iniciar el gateway con API REST en Windows

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Cambiar al directorio src
cd src

REM Iniciar el gateway con API REST
python main.py --api --host 0.0.0.0 --port 8080

REM Volver al directorio anterior
cd ..