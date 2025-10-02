#!/bin/bash
# Script para iniciar el descubrimiento de PLCs en Linux/Mac

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cambiar al directorio base
cd "$BASE_DIR"

# Verificar si el entorno virtual existe
if [ ! -d "gateway_venv" ]; then
    echo "El entorno virtual no existe. Por favor ejecute install_gateway.py primero."
    exit 1
fi

# Activar el entorno virtual
source gateway_venv/bin/activate

# Iniciar el descubrimiento de PLCs
echo "Iniciando descubrimiento de PLCs..."
python discover_plcs.py

# Desactivar el entorno virtual
deactivate