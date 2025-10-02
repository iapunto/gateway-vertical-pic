#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core del Gateway Local - Orquestador principal
"""

import logging
import threading
import time
from typing import Dict, Any, List, Optional
from gateway.src.config.config_manager import ConfigManager
from gateway.src.utils.logger import setup_logger
from gateway.src.plc.plc_factory import PLCFactory
from gateway.src.interfaces.plc_interface import PLCInterface


class GatewayCore:
    """Clase principal del Gateway Local"""

    def __init__(self, config_file: str = "gateway_config.json"):
        """Inicializa el Gateway Local"""
        self.config_manager = ConfigManager(config_file)
        self.logger = setup_logger(self.config_manager.get("logging", {}))
        self.plcs: Dict[str, PLCInterface] = {}
        self.running = False
        self.threads: List[threading.Thread] = []

        # Configuración
        heartbeat_interval = self.config_manager.get(
            "wms.heartbeat_interval", 60)
        # Manejar diferentes tipos de retorno de configuración
        if isinstance(heartbeat_interval, (int, float, str)):
            self.heartbeat_interval = int(heartbeat_interval)
        else:
            self.heartbeat_interval = 60

        self.logger.info("Gateway Local inicializado")

    def initialize_plcs(self) -> bool:
        """Inicializa todos los PLCs configurados"""
        try:
            plc_configs = self.config_manager.get_plc_list()
            self.logger.info(f"Inicializando {len(plc_configs)} PLCs")

            for plc_config in plc_configs:
                plc_id = plc_config.get("id")
                plc_type = plc_config.get("type", "delta")
                ip = plc_config.get("ip")
                port = plc_config.get("port", 3200)

                if not all([plc_id, ip]):
                    self.logger.warning(
                        f"Configuración incompleta para PLC: {plc_config}")
                    continue

                try:
                    plc = PLCFactory.create_plc(plc_type, ip, port)
                    self.plcs[plc_id] = plc
                    self.logger.info(
                        f"PLC {plc_id} ({plc_type}) inicializado: {ip}:{port}")
                except Exception as e:
                    self.logger.error(f"Error inicializando PLC {plc_id}: {e}")
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error inicializando PLCs: {e}")
            return False

    def connect_plcs(self) -> bool:
        """Conecta todos los PLCs inicializados"""
        success_count = 0
        for plc_id, plc in self.plcs.items():
            try:
                if plc.connect():
                    self.logger.info(f"PLC {plc_id} conectado exitosamente")
                    success_count += 1
                else:
                    self.logger.error(f"Error conectando PLC {plc_id}")
            except Exception as e:
                self.logger.error(f"Excepción conectando PLC {plc_id}: {e}")

        return success_count == len(self.plcs)

    def start(self) -> bool:
        """Inicia el Gateway Local"""
        self.logger.info("Iniciando Gateway Local...")

        # Inicializar PLCs
        if not self.initialize_plcs():
            self.logger.error("Error inicializando PLCs")
            return False

        # Conectar PLCs
        if not self.connect_plcs():
            self.logger.error("Error conectando PLCs")
            return False

        self.running = True

        # Iniciar hilos de trabajo
        self._start_heartbeat_thread()
        self._start_monitoring_thread()

        self.logger.info("Gateway Local iniciado exitosamente")
        return True

    def stop(self) -> None:
        """Detiene el Gateway Local"""
        self.logger.info("Deteniendo Gateway Local...")
        self.running = False

        # Desconectar todos los PLCs
        for plc_id, plc in self.plcs.items():
            try:
                plc.disconnect()
                self.logger.info(f"PLC {plc_id} desconectado")
            except Exception as e:
                self.logger.error(f"Error desconectando PLC {plc_id}: {e}")

        # Esperar a que terminen los hilos
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)

        self.logger.info("Gateway Local detenido")

    def _start_heartbeat_thread(self) -> None:
        """Inicia el hilo de heartbeat"""
        heartbeat_thread = threading.Thread(
            target=self._heartbeat_worker, daemon=True)
        heartbeat_thread.start()
        self.threads.append(heartbeat_thread)
        self.logger.info("Hilo de heartbeat iniciado")

    def _start_monitoring_thread(self) -> None:
        """Inicia el hilo de monitoreo"""
        monitoring_thread = threading.Thread(
            target=self._monitoring_worker, daemon=True)
        monitoring_thread.start()
        self.threads.append(monitoring_thread)
        self.logger.info("Hilo de monitoreo iniciado")

    def _heartbeat_worker(self) -> None:
        """Worker para enviar heartbeat"""
        while self.running:
            try:
                # TODO: Implementar envío real de heartbeat al WMS
                self.logger.debug("Enviando heartbeat...")
                time.sleep(float(self.heartbeat_interval))
            except Exception as e:
                self.logger.error(f"Error en worker de heartbeat: {e}")
                time.sleep(5.0)

    def _monitoring_worker(self) -> None:
        """Worker para monitoreo de PLCs"""
        while self.running:
            try:
                # TODO: Implementar monitoreo real de PLCs
                self.logger.debug("Monitoreando PLCs...")
                time.sleep(10.0)
            except Exception as e:
                self.logger.error(f"Error en worker de monitoreo: {e}")
                time.sleep(5.0)

    def get_plc_status(self, plc_id: str) -> Dict[str, Any]:
        """Obtiene el estado de un PLC específico"""
        if plc_id not in self.plcs:
            return {"error": f"PLC {plc_id} no encontrado", "success": False}

        try:
            plc = self.plcs[plc_id]
            status = plc.get_status()
            return {
                "plc_id": plc_id,
                "connected": plc.is_connected(),
                "status": status,
                "success": True
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo estado de PLC {plc_id}: {e}")
            return {"error": str(e), "success": False}

    def send_plc_command(self, plc_id: str, command: int, argument: Optional[int] = None) -> Dict[str, Any]:
        """Envía un comando a un PLC específico"""
        if plc_id not in self.plcs:
            return {"error": f"PLC {plc_id} no encontrado", "success": False}

        try:
            plc = self.plcs[plc_id]
            if not plc.is_connected():
                if not plc.connect():
                    return {"error": "No se pudo conectar al PLC", "success": False}

            result = plc.send_command(command, argument)
            return {
                "plc_id": plc_id,
                "command": command,
                "argument": argument,
                "result": result,
                "success": result.get("success", False)
            }
        except Exception as e:
            self.logger.error(f"Error enviando comando a PLC {plc_id}: {e}")
            return {"error": str(e), "success": False}
