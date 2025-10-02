#!/bin/bash
# Script para iniciar el gateway con API REST

# Activar el entorno virtual
source venv/Scripts/activate

# Cambiar al directorio src
cd src

# Iniciar el gateway con API REST
python main.py --api --host 0.0.0.0 --port 8080

# Volver al directorio anterior
cd ..