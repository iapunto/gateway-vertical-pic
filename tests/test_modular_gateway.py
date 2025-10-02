#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas para el Gateway Local modular
"""

from gateway.src.plc.delta_plc import DeltaPLC
from gateway.src.plc.plc_factory import PLCFactory
from gateway.src.interfaces.plc_interface import PLCInterface
import sys
import os
import unittest
from unittest.mock import Mock, patch
import abc

# Añadir el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestPLCInterface(unittest.TestCase):
    """Pruebas para la interface PLC"""

    def test_interface_is_abstract(self):
        """Verifica que la interface sea abstracta"""
        # Verificar que la clase sea abstracta
        self.assertTrue(abc.ABC in PLCInterface.__bases__ or hasattr(
            PLCInterface, '__abstractmethods__'))

        # Verificar que tenga métodos abstractos
        self.assertTrue(hasattr(PLCInterface, '__abstractmethods__'))
        abstract_methods = PLCInterface.__abstractmethods__
        self.assertIn('connect', abstract_methods)
        self.assertIn('disconnect', abstract_methods)
        self.assertIn('is_connected', abstract_methods)
        self.assertIn('send_command', abstract_methods)
        self.assertIn('get_status', abstract_methods)
        self.assertIn('get_position', abstract_methods)


class TestDeltaPLC(unittest.TestCase):
    """Pruebas para la implementación Delta PLC"""

    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.plc = DeltaPLC("127.0.0.1", 3200)

    def test_initialization(self):
        """Verifica la inicialización correcta"""
        self.assertEqual(self.plc.ip, "127.0.0.1")
        self.assertEqual(self.plc.port, 3200)
        self.assertIsNone(self.plc.sock)

    def test_is_connected(self):
        """Verifica el método is_connected"""
        self.assertFalse(self.plc.is_connected())
        self.plc.sock = Mock()
        self.assertTrue(self.plc.is_connected())


class TestPLCFactory(unittest.TestCase):
    """Pruebas para la fábrica de PLCs"""

    def test_create_delta_plc(self):
        """Verifica la creación de PLC Delta"""
        plc = PLCFactory.create_plc("delta", "127.0.0.1", 3200)
        self.assertIsInstance(plc, DeltaPLC)

    def test_create_plc_case_insensitive(self):
        """Verifica que la creación sea case insensitive"""
        plc1 = PLCFactory.create_plc("delta", "127.0.0.1", 3200)
        plc2 = PLCFactory.create_plc("Delta", "127.0.0.1", 3200)
        plc3 = PLCFactory.create_plc("DELTA", "127.0.0.1", 3200)

        self.assertIsInstance(plc1, DeltaPLC)
        self.assertIsInstance(plc2, DeltaPLC)
        self.assertIsInstance(plc3, DeltaPLC)

    def test_create_unsupported_plc(self):
        """Verifica el manejo de PLCs no soportados"""
        with self.assertRaises(ValueError):
            PLCFactory.create_plc("siemens", "127.0.0.1", 3200)

    def test_register_new_plc_type(self):
        """Verifica el registro de nuevos tipos de PLC"""
        # Crear una implementación mock
        class MockPLC(PLCInterface):
            def connect(self): return True
            def disconnect(self): pass
            def is_connected(self): return True
            def send_command(self, command, argument=None): return {}
            def get_status(self): return {}
            def get_position(self): return 0

        # Registrar el nuevo tipo
        PLCFactory.register_plc_type("mock", MockPLC)

        # Verificar que se puede crear
        plc = PLCFactory.create_plc("mock", "127.0.0.1", 3200)
        self.assertIsInstance(plc, MockPLC)


if __name__ == "__main__":
    unittest.main()
