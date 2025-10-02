#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada para la interfaz gráfica de escritorio del Gateway Local
"""

from src.gui.main_window import main
import sys
import os

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


if __name__ == "__main__":
    main()
