#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de funcionalidad PLC para el Gateway Local

Este test verifica que podemos importar y usar las clases PLC existentes.

Autor: Qoder AI Assistant
Fecha: 2025-10-01
"""

import sys
import os

# Añadir el directorio raíz al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_imports():
    """Test básico de importación de módulos"""
    try:
        # Intentar importar los módulos
        from models.plc import PLC
        from controllers.carousel_controller import CarouselController
        from commons.utils import interpretar_estado_plc

        print("✓ Todas las importaciones fueron exitosas")
        print(f"Clase PLC: {PLC}")
        print(f"Clase CarouselController: {CarouselController}")
        print(f"Función interpretar_estado_plc: {interpretar_estado_plc}")

        return True
    except Exception as e:
        print(f"✗ Error en importaciones: {str(e)}")
        return False


def main():
    """Función principal de test"""
    print("Test Simple de Funcionalidad PLC - Gateway Local")
    print("=" * 50)

    imports_ok = test_imports()

    print("\n=== Resumen de Tests ===")
    print(f"Importaciones: {'✓ OK' if imports_ok else '✗ FALLÓ'}")

    if imports_ok:
        print("\n✓ Test de importaciones pasado correctamente")
        return 0
    else:
        print("\n✗ Test de importaciones falló")
        return 1


if __name__ == "__main__":
    sys.exit(main())
