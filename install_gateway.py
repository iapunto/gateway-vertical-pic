#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación simplificada para el Gateway Local
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


def check_python():
    """Verifica si Python está instalado y es compatible"""
    print("🔍 Verificando instalación de Python...")

    try:
        # Verificar versión de Python
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("❌ Python 3.7 o superior es requerido")
            print(
                f"Versión actual: {version.major}.{version.minor}.{version.micro}")
            return False

        print(
            f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado")
        return True
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return False


def create_virtual_environment():
    """Crea un entorno virtual para el gateway"""
    print("\n🔧 Creando entorno virtual...")

    try:
        # Crear entorno virtual
        subprocess.run([sys.executable, "-m", "venv", "gateway_venv"],
                       check=True, capture_output=True)
        print("✅ Entorno virtual creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def install_dependencies():
    """Instala las dependencias del gateway"""
    print("\n📥 Instalando dependencias...")

    try:
        # Determinar el comando pip según el sistema operativo
        if platform.system() == "Windows":
            pip_cmd = os.path.join("gateway_venv", "Scripts", "pip")
        else:
            pip_cmd = os.path.join("gateway_venv", "bin", "pip")

        # Actualizar pip
        print("  Actualizando pip...")
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"],
                       check=True, capture_output=True)

        # Instalar dependencias
        print("  Instalando dependencias...")
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"],
                       check=True, capture_output=True)

        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def create_startup_scripts():
    """Crea scripts de inicio convenientes"""
    print("\n🚀 Creando scripts de inicio...")

    try:
        # Script para Windows
        if platform.system() == "Windows":
            # Crear batch script para iniciar el gateway en modo API
            with open("start_gateway.bat", "w") as f:
                f.write("""@echo off
REM Script para iniciar el Gateway Local
cd /d "%~dp0"
echo Iniciando Gateway Local...
gateway_venv\\Scripts\\python src\\main.py --api
pause
""")

            # Crear batch script para iniciar el gateway en modo standalone
            with open("start_gateway_standalone.bat", "w") as f:
                f.write("""@echo off
REM Script para iniciar el Gateway Local en modo standalone
cd /d "%~dp0"
echo Iniciando Gateway Local en modo standalone...
gateway_venv\\Scripts\\python src\\main.py
pause
""")

            # Crear batch script para iniciar el simulador de PLC
            with open("start_plc_simulator.bat", "w") as f:
                f.write("""@echo off
REM Script para iniciar el simulador de PLC
cd /d "%~dp0"
echo Iniciando simulador de PLC...
gateway_venv\\Scripts\\python src\\plc\\plc_simulator.py
pause
""")

        # Script para Linux/Mac
        else:
            # Crear shell script para iniciar el gateway en modo API
            with open("start_gateway.sh", "w") as f:
                f.write("""#!/bin/bash
# Script para iniciar el Gateway Local
cd "$(dirname "$0")"
echo "Iniciando Gateway Local..."
./gateway_venv/bin/python src/main.py --api
""")

            # Crear shell script para iniciar el gateway en modo standalone
            with open("start_gateway_standalone.sh", "w") as f:
                f.write("""#!/bin/bash
# Script para iniciar el Gateway Local en modo standalone
cd "$(dirname "$0")"
echo "Iniciando Gateway Local en modo standalone..."
./gateway_venv/bin/python src/main.py
""")

            # Crear shell script para iniciar el simulador de PLC
            with open("start_plc_simulator.sh", "w") as f:
                f.write("""#!/bin/bash
# Script para iniciar el simulador de PLC
cd "$(dirname "$0")"
echo "Iniciando simulador de PLC..."
./gateway_venv/bin/python src/plc/plc_simulator.py
""")

            # Hacer los scripts ejecutables
            os.chmod("start_gateway.sh", 0o755)
            os.chmod("start_gateway_standalone.sh", 0o755)
            os.chmod("start_plc_simulator.sh", 0o755)

        print("✅ Scripts de inicio creados exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error creando scripts de inicio: {e}")
        return False


def create_desktop_shortcuts():
    """Crea accesos directos en el escritorio (solo Windows)"""
    if platform.system() != "Windows":
        return True

    print("\n📌 Creando accesos directos en el escritorio...")

    try:
        # Obtener ruta del escritorio
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")

        # Crear acceso directo para iniciar el gateway en modo API
        shortcut_content = f"""@echo off
cd /d "{os.getcwd()}"
gateway_venv\\Scripts\\python src\\main.py --api
pause
"""
        shortcut_path = os.path.join(
            desktop, "Iniciar Gateway Local (API).bat")
        with open(shortcut_path, "w") as f:
            f.write(shortcut_content)

        # Crear acceso directo para iniciar el gateway en modo standalone
        shortcut_content = f"""@echo off
cd /d "{os.getcwd()}"
gateway_venv\\Scripts\\python src\\main.py
pause
"""
        shortcut_path = os.path.join(
            desktop, "Iniciar Gateway Local (Standalone).bat")
        with open(shortcut_path, "w") as f:
            f.write(shortcut_content)

        print("✅ Accesos directos creados en el escritorio")
        return True
    except Exception as e:
        print(f"⚠️  No se pudieron crear los accesos directos: {e}")
        return True  # No es crítico


def main():
    """Función principal del instalador"""
    print("🔧 Instalador del Gateway Local")
    print("=" * 40)

    # Verificar que estamos en el directorio correcto
    if not os.path.exists("src") or not os.path.exists("requirements.txt"):
        print("❌ Por favor ejecute este script desde el directorio raíz del proyecto")
        print("   El directorio debe contener 'src/' y 'requirements.txt'")
        return False

    # Verificar Python
    if not check_python():
        return False

    # Crear entorno virtual
    if not create_virtual_environment():
        return False

    # Instalar dependencias
    if not install_dependencies():
        return False

    # Crear scripts de inicio
    if not create_startup_scripts():
        return False

    # Crear accesos directos
    create_desktop_shortcuts()

    print("\n🎉 ¡Instalación completada exitosamente!")
    print("\n📁 Archivos creados:")
    print("  - gateway_venv/        (Entorno virtual)")

    if platform.system() == "Windows":
        print("  - start_gateway.bat    (Iniciar gateway con API)")
        print("  - start_gateway_standalone.bat (Iniciar gateway standalone)")
        print("  - start_plc_simulator.bat (Iniciar simulador de PLC)")
        print("  - Accesos directos en el escritorio")
    else:
        print("  - start_gateway.sh     (Iniciar gateway con API)")
        print("  - start_gateway_standalone.sh (Iniciar gateway standalone)")
        print("  - start_plc_simulator.sh (Iniciar simulador de PLC)")

    print("\n🚀 Para iniciar el gateway:")
    if platform.system() == "Windows":
        print("  - Ejecute 'start_gateway.bat' para modo API")
        print("  - Ejecute 'start_gateway_standalone.bat' para modo standalone")
    else:
        print("  - Ejecute './start_gateway.sh' para modo API")
        print("  - Ejecute './start_gateway_standalone.sh' para modo standalone")

    print("\n📝 Siguiente paso: Configure el archivo 'gateway_config.json' según sus necesidades")

    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)
