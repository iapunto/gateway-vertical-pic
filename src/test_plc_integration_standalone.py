#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de integración standalone para el Gateway Local (sin WMS)
"""

import sys
import os
import json
import time
import threading
from typing import Optional
from unittest.mock import Mock, patch

# Importar usando rutas relativas
from core.gateway_core import GatewayCore
from plc.delta_plc import DeltaPLC
from plc.plc_factory import PLCFactory
from config.config_manager import ConfigManager


class MockDeltaPLC(DeltaPLC):
    """Mock de PLC Delta para pruebas sin hardware real"""

    def __init__(self, ip: str, port: int = 3200):
        super().__init__(ip, port)
        self._connected = False
        self._position = 0
        self._commands_received = []

    def connect(self) -> bool:
        """Simula conexión exitosa"""
        self._connected = True
        return True

    def disconnect(self) -> None:
        """Simula desconexión"""
        self._connected = False

    def is_connected(self) -> bool:
        """Retorna estado de conexión simulado"""
        return self._connected

    def send_command(self, command: int, argument: Optional[int] = None):
        """Simula envío de comando"""
        self._commands_received.append((command, argument))

        # Simular respuestas diferentes según el comando
        if command == 0:  # STATUS
            return {
                'status_code': 0,
                'position': self._position,
                'success': True
            }
        elif command == 1:  # MUEVETE
            if argument is not None:
                self._position = argument
            return {
                'status_code': 0,
                'position': self._position,
                'success': True
            }
        else:
            return {
                'status_code': 0,
                'position': self._position,
                'success': True
            }

    def get_status(self):
        """Simula obtención de estado"""
        return self.send_command(0)

    def get_position(self) -> int:
        """Retorna posición simulada"""
        return self._position


def create_test_config():
    """Crea una configuración de prueba"""
    return {
        "gateway": {
            "id": "TEST-GW-001",
            "name": "Gateway de Prueba",
            "version": "2.7.0"
        },
        "wms": {
            "endpoint": "https://wms.example.com/api/v1/gateways",
            "auth_token": "",
            "reconnect_interval": 30,
            "heartbeat_interval": 60
        },
        "network": {
            "bind_address": "127.0.0.1",
            "bind_port": 8080,
            "plc_port": 3200
        },
        "security": {
            "tls_cert": "",
            "tls_key": "",
            "ca_cert": "",
            "require_tls": False
        },
        "logging": {
            "level": "DEBUG",
            "file": "test_gateway.log",
            "max_size": 10485760,
            "backup_count": 5
        },
        "plcs": [
            {
                "id": "TEST-PLC-001",
                "type": "delta",
                "name": "PLC de Prueba 1",
                "ip": "127.0.0.1",
                "port": 3200,
                "description": "PLC Delta simulado para pruebas"
            }
        ]
    }


def test_gateway_standalone_operation():
    """Test de operación standalone del gateway"""
    print("🧪 Test de operación standalone del Gateway...")

    # Guardar las clases originales
    original_config_manager_init = ConfigManager.__init__
    original_config_manager_get = ConfigManager.get
    original_config_manager_get_plc_list = ConfigManager.get_plc_list
    original_create_plc = PLCFactory.create_plc

    # Crear configuración de prueba
    test_config = create_test_config()

    # Reemplazar métodos con mocks
    def mock_config_manager_init(self, config_file="gateway_config.json"):
        self.config = test_config
        self.logger = Mock()

    def mock_config_manager_get(self, key_path, default=None):
        keys = key_path.split('.')
        value = test_config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def mock_config_manager_get_plc_list(self):
        return test_config["plcs"]

    def mock_create_plc(plc_type, ip, port=3200):
        return MockDeltaPLC(ip, port)

    # Aplicar los mocks
    ConfigManager.__init__ = mock_config_manager_init
    ConfigManager.get = mock_config_manager_get
    ConfigManager.get_plc_list = mock_config_manager_get_plc_list
    PLCFactory.create_plc = mock_create_plc

    try:
        # Crear e iniciar el gateway
        gateway = GatewayCore()

        # Verificar que se haya creado correctamente
        assert gateway.config_manager is not None
        assert gateway.logger is not None

        # Iniciar el gateway
        assert gateway.start(), "El gateway debería iniciar correctamente"
        assert gateway.running, "El gateway debería estar en estado running"

        # Verificar que se hayan inicializado los PLCs
        assert len(gateway.plcs) > 0, "Debería haber PLCs inicializados"

        # Verificar estado de PLC
        plc_status = gateway.get_plc_status("TEST-PLC-001")
        assert plc_status["success"], "Debería obtener estado de PLC correctamente"
        assert plc_status["connected"], "PLC debería estar conectado"

        # Enviar comando al PLC
        command_result = gateway.send_plc_command("TEST-PLC-001", 1, 5)
        assert command_result["success"], "Debería enviar comando correctamente"
        assert command_result["result"]["position"] == 5, "La posición debería ser 5"

        # Detener el gateway
        gateway.stop()
        assert not gateway.running, "El gateway debería estar detenido"

    finally:
        # Restaurar las clases originales
        ConfigManager.__init__ = original_config_manager_init
        ConfigManager.get = original_config_manager_get
        ConfigManager.get_plc_list = original_config_manager_get_plc_list
        PLCFactory.create_plc = original_create_plc

    print("✅ Test de operación standalone del Gateway PASADO")


def test_multiple_plcs():
    """Test con múltiples PLCs"""
    print("\n🧪 Test con múltiples PLCs...")

    # Guardar las clases originales
    original_config_manager_init = ConfigManager.__init__
    original_config_manager_get = ConfigManager.get
    original_config_manager_get_plc_list = ConfigManager.get_plc_list
    original_create_plc = PLCFactory.create_plc

    # Crear configuración con múltiples PLCs
    test_config = create_test_config()
    test_config["plcs"] = [
        {
            "id": "TEST-PLC-001",
            "type": "delta",
            "name": "PLC de Prueba 1",
            "ip": "127.0.0.1",
            "port": 3200,
            "description": "PLC Delta simulado 1"
        },
        {
            "id": "TEST-PLC-002",
            "type": "delta",
            "name": "PLC de Prueba 2",
            "ip": "127.0.0.2",
            "port": 3200,
            "description": "PLC Delta simulado 2"
        }
    ]

    # Reemplazar métodos con mocks
    def mock_config_manager_init(self, config_file="gateway_config.json"):
        self.config = test_config
        self.logger = Mock()

    def mock_config_manager_get(self, key_path, default=None):
        keys = key_path.split('.')
        value = test_config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def mock_config_manager_get_plc_list(self):
        return test_config["plcs"]

    def mock_create_plc(plc_type, ip, port=3200):
        return MockDeltaPLC(ip, port)

    # Aplicar los mocks
    ConfigManager.__init__ = mock_config_manager_init
    ConfigManager.get = mock_config_manager_get
    ConfigManager.get_plc_list = mock_config_manager_get_plc_list
    PLCFactory.create_plc = mock_create_plc

    try:
        # Crear e iniciar el gateway
        gateway = GatewayCore()
        assert gateway.start(), "El gateway debería iniciar correctamente"

        # Verificar que se hayan inicializado todos los PLCs
        assert len(gateway.plcs) == 2, "Debería haber 2 PLCs inicializados"

        # Verificar estado de todos los PLCs
        for plc_id in ["TEST-PLC-001", "TEST-PLC-002"]:
            plc_status = gateway.get_plc_status(plc_id)
            assert plc_status["success"], f"Debería obtener estado de {plc_id} correctamente"
            assert plc_status["connected"], f"{plc_id} debería estar conectado"

        # Enviar comandos a diferentes PLCs
        result1 = gateway.send_plc_command("TEST-PLC-001", 1, 10)
        result2 = gateway.send_plc_command("TEST-PLC-002", 1, 20)

        assert result1["success"], "Debería enviar comando al PLC 1 correctamente"
        assert result2["success"], "Debería enviar comando al PLC 2 correctamente"
        assert result1["result"]["position"] == 10, "PLC 1 debería estar en posición 10"
        assert result2["result"]["position"] == 20, "PLC 2 debería estar en posición 20"

        # Detener el gateway
        gateway.stop()

    finally:
        # Restaurar las clases originales
        ConfigManager.__init__ = original_config_manager_init
        ConfigManager.get = original_config_manager_get
        ConfigManager.get_plc_list = original_config_manager_get_plc_list
        PLCFactory.create_plc = original_create_plc

    print("✅ Test con múltiples PLCs PASADO")


def test_api_adapter_compatibility():
    """Test de compatibilidad con API Adapter"""
    print("\n🧪 Test de compatibilidad con API Adapter...")

    # Guardar las clases originales
    original_config_manager_init = ConfigManager.__init__
    original_config_manager_get = ConfigManager.get
    original_config_manager_get_plc_list = ConfigManager.get_plc_list
    original_create_plc = PLCFactory.create_plc

    # Crear configuración de prueba
    test_config = create_test_config()

    # Reemplazar métodos con mocks
    def mock_config_manager_init(self, config_file="gateway_config.json"):
        self.config = test_config
        self.logger = Mock()

    def mock_config_manager_get(self, key_path, default=None):
        keys = key_path.split('.')
        value = test_config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def mock_config_manager_get_plc_list(self):
        return test_config["plcs"]

    def mock_create_plc(plc_type, ip, port=3200):
        return MockDeltaPLC(ip, port)

    # Aplicar los mocks
    ConfigManager.__init__ = mock_config_manager_init
    ConfigManager.get = mock_config_manager_get
    ConfigManager.get_plc_list = mock_config_manager_get_plc_list
    PLCFactory.create_plc = mock_create_plc

    try:
        # Crear gateway y adapter
        from adapters.api_adapter import APIAdapter

        gateway = GatewayCore()
        assert gateway.start(), "El gateway debería iniciar correctamente"

        adapter = APIAdapter(gateway)

        # Test get_status para un PLC específico
        status = adapter.get_status("TEST-PLC-001")
        assert status["success"], "Debería obtener status correctamente"
        assert status["connected"], "PLC debería estar conectado"

        # Test get_status para todos los PLCs
        all_status = adapter.get_status()
        assert all_status["success"], "Debería obtener status de todos los PLCs"
        assert len(all_status["data"]) > 0, "Debería haber datos de PLCs"

        # Test send_command
        command_result = adapter.send_command(1, 15, "TEST-PLC-001")
        assert command_result["success"], "Debería enviar comando correctamente"
        assert command_result["result"]["position"] == 15, "Debería estar en posición 15"

        # Test move_to_position
        move_result = adapter.move_to_position(25, "TEST-PLC-001")
        assert move_result["success"], "Debería mover a posición correctamente"
        assert move_result["result"]["position"] == 25, "Debería estar en posición 25"

        # Test get_machines
        machines = adapter.get_machines()
        assert machines["success"], "Debería obtener lista de máquinas"
        assert len(machines["data"]) > 0, "Debería haber máquinas disponibles"

        gateway.stop()

    finally:
        # Restaurar las clases originales
        ConfigManager.__init__ = original_config_manager_init
        ConfigManager.get = original_config_manager_get
        ConfigManager.get_plc_list = original_config_manager_get_plc_list
        PLCFactory.create_plc = original_create_plc

    print("✅ Test de compatibilidad con API Adapter PASADO")


def main():
    """Función principal de tests"""
    print("🚀 Iniciando tests de integración standalone para Gateway Local")
    print("=" * 60)

    try:
        test_gateway_standalone_operation()
        test_multiple_plcs()
        test_api_adapter_compatibility()

        print("\n" + "=" * 60)
        print("🎉 Todos los tests PASARON exitosamente!")
        print("✅ El gateway está listo para operación standalone")

    except Exception as e:
        print(f"\n❌ Test FALLIDO: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
