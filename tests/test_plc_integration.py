#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de integración con PLC para el Gateway Local

Este test demuestra la funcionalidad básica de comunicación con el PLC
basado en el código existente que ya está implementado en las máquinas.

Autor: Qoder AI Assistant
Fecha: 2025-10-01
"""

from controllers.carousel_controller import CarouselController
from models.plc import PLC
import sys
import os
import time

# Añadir el directorio raíz al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def test_plc_connection(use_simulator=False):
    """Test básico de conexión con PLC"""
    print("=== Test de Conexión con PLC ===")

    # Configurar IP y puerto según si usamos simulador o PLC real
    if use_simulator:
        plc_ip = "127.0.0.1"
        plc_port = 5000
        print("Usando simulador de PLC")
    else:
        # Usar una IP y puerto de ejemplo para PLC real
        plc_ip = "192.168.1.100"
        plc_port = 5000
        print("Usando PLC físico (configuración de ejemplo)")

    print(f"Intentando conectar con PLC en {plc_ip}:{plc_port}")

    try:
        # Crear instancia de PLC
        plc = PLC(plc_ip, plc_port)

        # Intentar conectar
        if plc.connect():
            print("✓ Conexión establecida correctamente")

            # Crear controlador
            controller = CarouselController(plc)

            # Obtener estado actual
            print("Obteniendo estado actual del PLC...")
            status = controller.get_current_status()
            print(f"Estado: {status}")

            # Cerrar conexión
            plc.close()
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

    # Configurar IP y puerto según si usamos simulador o PLC real
    if use_simulator:
        plc_ip = "127.0.0.1"
        plc_port = 5000
        print("Usando simulador de PLC")
    else:
        # Usar una IP y puerto de ejemplo para PLC real
        plc_ip = "192.168.1.100"
        plc_port = 5000
        print("Usando PLC físico (configuración de ejemplo)")

    print(f"Intentando conectar con PLC en {plc_ip}:{plc_port}")

    try:
        # Crear instancia de PLC
        plc = PLC(plc_ip, plc_port)

        # Crear controlador
        controller = CarouselController(plc)

        # Obtener estado inicial
        print("Estado inicial:")
        initial_status = controller.get_current_status()
        print(f"  {initial_status}")

        # Enviar comando de movimiento a posición 1 (si no estamos usando simulador)
        if not use_simulator:
            print("Enviando comando de movimiento a posición 1...")
            move_result = controller.move_to_position(1)
            print(f"Resultado del movimiento: {move_result}")
        else:
            print("En modo simulador, omitiendo comando de movimiento físico")

        # Obtener estado final
        print("Estado final:")
        final_status = controller.get_current_status()
        print(f"  {final_status}")

        # Cerrar conexión
        plc.close()
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
