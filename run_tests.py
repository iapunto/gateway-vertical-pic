#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar todas las pruebas del Gateway Local
"""

import sys
import os
import unittest
import argparse


def run_unit_tests():
    """Ejecuta las pruebas unitarias"""
    print("🏃 Ejecutando pruebas unitarias...")

    # Descubrir y ejecutar pruebas
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_integration_tests():
    """Ejecuta las pruebas de integración"""
    print("🏃 Ejecutando pruebas de integración...")

    # Ejecutar el test de integración standalone
    try:
        # Verificar si existe el archivo de pruebas
        test_file = os.path.join(os.path.dirname(
            __file__), 'src', 'test_plc_integration_standalone.py')
        if os.path.exists(test_file):
            import subprocess
            import sys

            result = subprocess.run([
                sys.executable,
                'src/test_plc_integration_standalone.py'
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__))

            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            return result.returncode == 0
        else:
            print("❌ No se encontró el archivo de pruebas de integración")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando pruebas de integración: {e}")
        return False


def run_plc_tests():
    """Ejecuta las pruebas de comunicación con PLC"""
    print("🏃 Ejecutando pruebas de comunicación con PLC...")

    try:
        # Verificar si existe el archivo de pruebas
        test_file = os.path.join(os.path.dirname(
            __file__), 'tests', 'test_plc_communication.py')
        if os.path.exists(test_file):
            import subprocess
            import sys

            result = subprocess.run([
                sys.executable,
                'tests/test_plc_communication.py'
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__))

            print(result.stdout)
            if result.stderr:
                print(result.stderr)

            return result.returncode == 0
        else:
            print("❌ No se encontró el archivo de pruebas de PLC")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando pruebas de PLC: {e}")
        return False


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Ejecutar pruebas del Gateway Local")
    parser.add_argument("--unit", action="store_true",
                        help="Ejecutar solo pruebas unitarias")
    parser.add_argument("--integration", action="store_true",
                        help="Ejecutar solo pruebas de integración")
    parser.add_argument("--plc", action="store_true",
                        help="Ejecutar solo pruebas de PLC")
    parser.add_argument("--all", action="store_true",
                        help="Ejecutar todas las pruebas (por defecto)")

    args = parser.parse_args()

    # Si no se especifica ningún tipo de prueba, ejecutar todas
    if not (args.unit or args.integration or args.plc):
        args.all = True

    success = True

    if args.all or args.unit:
        print("=" * 50)
        print("🧪 PRUEBAS UNITARIAS")
        print("=" * 50)
        if not run_unit_tests():
            success = False
        print()

    if args.all or args.integration:
        print("=" * 50)
        print("🔧 PRUEBAS DE INTEGRACIÓN")
        print("=" * 50)
        if not run_integration_tests():
            success = False
        print()

    if args.all or args.plc:
        print("=" * 50)
        print("🔌 PRUEBAS DE COMUNICACIÓN CON PLC")
        print("=" * 50)
        if not run_plc_tests():
            success = False
        print()

    if success:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("❌ Algunas pruebas fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
