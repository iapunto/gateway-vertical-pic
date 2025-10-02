#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar la GUI del Gateway Local
"""

import sys
import os

# Añadir el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.gui.main_window import main
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Error al iniciar la aplicación: {e}")
    sys.exit(1)
