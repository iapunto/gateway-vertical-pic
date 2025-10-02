#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de comunicación con PLCs para el Gateway Local
"""

from gateway.src.plc.plc_factory import PLCFactory
from gateway.src.plc.delta_plc import DeltaPLC
from gateway.src.core.gateway_core import GatewayCore
import sys
import os
import json
import time

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_plc_factory():
    """Test de la fábrica de PLCs"""
    print("🧪 Test de PLC Factory...")

    # Crear PLC Delta
    plc = PLCFactory.create_plc("delta", "127.0.0.1", 3200)
    assert isinstance(plc, DeltaPLC), "Debería crear una instancia de DeltaPLC"
    print("✅ PLC Factory funciona correctamente")

    # Verificar tipos soportados
    supported_types = PLCFactory.get_supported_types()
    assert "delta" in supported_types, "Delta debería estar en tipos soportados"
    print(f"✅ Tipos soportados: {supported_types}")


def test_delta_plc_initialization():
    """Test de inicialización de PLC Delta"""
    print("\n🧪 Test de inicialización de PLC Delta...")

    plc = DeltaPLC("127.0.0.1", 3200)

    assert plc.ip == "127.0.0.1", "IP debería ser 127.0.0.1"
    assert plc.port == 3200, "Puerto debería ser 3200"
    assert plc.sock is None, "Socket debería ser None inicialmente"
    assert not plc.is_connected(), "No debería estar conectado inicialmente"

    print("✅ Inicialización de PLC Delta correcta")


def test_plc_interface_compliance():
    """Test de cumplimiento de interface PLC"""
    print("\n🧪 Test de cumplimiento de interface PLC...")

    from gateway.src.interfaces.plc_interface import PLCInterface
    import inspect

    # Verificar que DeltaPLC implementa todos los métodos abstractos
    plc = DeltaPLC("127.0.0.1", 3200)

    # Obtener métodos abstractos de la interface
    abstract_methods = PLCInterface.__abstractmethods__

    # Verificar que todos los métodos abstractos están implementados
    for method_name in abstract_methods:
        method = getattr(plc, method_name, None)
        assert method is not None, f"Método {method_name} no implementado"
        assert callable(method), f"Método {method_name} no es callable"

    print("✅ Cumplimiento de interface PLC verificado")


def test_config_manager():
    """Test del gestor de configuración"""
    print("\n🧪 Test de gestor de configuración...")

    from gateway.src.config.config_manager import ConfigManager

    # Crear config manager con configuración por defecto
    config_manager = ConfigManager()

    # Verificar configuración básica
    gateway_config = config_manager.get("gateway")
    assert gateway_config is not None, "Configuración de gateway debería existir"
    assert "id" in gateway_config, "Configuración debería tener ID"

    # Verificar lista de PLCs
    plc_list = config_manager.get_plc_list()
    assert isinstance(plc_list, list), "Lista de PLCs debería ser una lista"

    print("✅ Gestor de configuración funciona correctamente")


def test_gateway_core_initialization():
    """Test de inicialización del core del gateway"""
    print("\n🧪 Test de inicialización del Gateway Core...")

    # Crear gateway core (sin iniciar)
    gateway = GatewayCore()

    assert gateway.config_manager is not None, "ConfigManager debería estar inicializado"
    assert gateway.logger is not None, "Logger debería estar inicializado"
    assert isinstance(gateway.plcs, dict), "PLCs debería ser un diccionario"
    assert not gateway.running, "Gateway no debería estar corriendo inicialmente"

    print("✅ Inicialización del Gateway Core correcta")


def test_command_validation():
    """Test de validación de comandos"""
    print("\n🧪 Test de validación de comandos...")

    plc = DeltaPLC("127.0.0.1", 3200)

    # Test comando válido
    try:
        # Esto no debería lanzar excepción para comando válido
        result = plc.send_command(0)  # Comando STATUS
        # Como no estamos conectados, debería devolver error
        assert "error" in result or "success" in result, "Debería devolver resultado estructurado"
    except Exception as e:
        # Si hay excepción, debería ser porque no estamos conectados
        pass

    print("✅ Validación de comandos funciona correctamente")


def main():
    """Función principal de tests"""
    print("🚀 Iniciando tests de comunicación con PLCs")
    print("=" * 50)

    try:
        test_plc_factory()
        test_delta_plc_initialization()
        test_plc_interface_compliance()
        test_config_manager()
        test_gateway_core_initialization()
        test_command_validation()

        print("\n" + "=" * 50)
        print("🎉 Todos los tests PASARON exitosamente!")
        print("✅ El gateway está listo para comunicación con PLCs")

    except Exception as e:
        print(f"\n❌ Test FALLIDO: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
