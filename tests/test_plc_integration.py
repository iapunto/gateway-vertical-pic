#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de integración con PLC para el Gateway Local

Este test demuestra la funcionalidad básica de comunicación con el PLC
basado en el código existente que ya está implementado en las máquinas.

Autor: Qoder AI Assistant
Fecha: 2025-10-01
"""

import sys
import os
import time

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_plc_connection(use_simulator=False):
    """Test básico de conexión con PLC"""
    print("=== Test de Conexión con PLC ===")

    from plc.plc_factory import PLCFactory
    from plc.delta_plc import DeltaPLC

    # Configurar IP y puerto según si usamos simulador o PLC real
    if use_simulator:
        plc_ip = "127.0.0.1"
        plc_port = 5000
        print("Usando simulador de PLC")
    else:
        # Usar una IP y puerto de ejemplo para PLC real
        plc_ip = "192.168.1.100"
        plc_port = 3200
        print("Usando PLC físico (configuración de ejemplo)")

    print(f"Intentando conectar con PLC en {plc_ip}:{plc_port}")

    try:
        # Crear instancia de PLC usando la fábrica
        plc = PLCFactory.create_plc("delta", plc_ip, plc_port)

        # Intentar conectar
        if plc.connect():
            print("✓ Conexión establecida correctamente")

            # Obtener estado actual
            print("Obteniendo estado actual del PLC...")
            status = plc.get_status()
            print(f"Estado: {status}")

            # Cerrar conexión
            plc.disconnect()
            print("✓ Conexión cerrada correctamente")
            return True
        else:
            print("✗ No se pudo establecer conexión con el PLC")
            return False

    except Exception as e:
        print(f"✗ Error durante el test: {str(e)}")
        return False


def test_plc_commands(use_simulator=False):
    """Test de envío de comandos al PLC"""
    print("\n=== Test de Comandos con PLC ===")

    from plc.plc_factory import PLCFactory
    from plc.delta_plc import DeltaPLC

    # Configurar IP y puerto según si usamos simulador o PLC real
    if use_simulator:
        plc_ip = "127.0.0.1"
        plc_port = 5000
        print("Usando simulador de PLC")
    else:
        # Usar una IP y puerto de ejemplo para PLC real
        plc_ip = "192.168.1.100"
        plc_port = 3200
        print("Usando PLC físico (configuración de ejemplo)")

    print(f"Intentando conectar con PLC en {plc_ip}:{plc_port}")

    try:
        # Crear instancia de PLC usando la fábrica
        plc = PLCFactory.create_plc("delta", plc_ip, plc_port)

        # Conectar al PLC
        if not plc.connect():
            print("✗ No se pudo establecer conexión con el PLC")
            return False

        # Obtener estado inicial
        print("Estado inicial:")
        initial_status = plc.get_status()
        print(f"  {initial_status}")

        # Enviar comando de movimiento a posición 1 (si no estamos usando simulador)
        if not use_simulator:
            print("Enviando comando de movimiento a posición 1...")
            move_result = plc.move_to_position(1)
            print(f"Resultado del movimiento: {move_result}")
        else:
            print("En modo simulador, omitiendo comando de movimiento físico")

        # Obtener estado final
        print("Estado final:")
        final_status = plc.get_status()
        print(f"  {final_status}")

        # Cerrar conexión
        plc.disconnect()
        print("✓ Test de comandos completado")
        return True

    except Exception as e:
        print(f"✗ Error durante el test de comandos: {str(e)}")
        return False


def main():
    """Función principal de test"""
    print("Test de Integración con PLC - Gateway Local")
    print("=" * 50)

    # Determinar si usar simulador o PLC real
    use_simulator = len(sys.argv) > 1 and sys.argv[1] == "--simulator"

    # Ejecutar tests
    connection_ok = test_plc_connection(use_simulator)
    commands_ok = test_plc_commands(use_simulator)

    print("\n=== Resumen de Tests ===")
    print(f"Conexión con PLC: {'✓ OK' if connection_ok else '✗ FALLÓ'}")
    print(f"Comandos PLC: {'✓ OK' if commands_ok else '✗ FALLÓ'}")

    if connection_ok and commands_ok:
        print("\n✓ Todos los tests pasaron correctamente")
        return 0
    else:
        print("\n✗ Algunos tests fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
