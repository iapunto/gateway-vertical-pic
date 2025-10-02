#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de configuración para microservicios del Gateway Local
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum


class ServiceType(Enum):
    """Tipos de servicios disponibles"""
    GATEWAY = "gateway"
    PLC_ADAPTER = "plc_adapter"
    MONITORING = "monitoring"
    HEALTH = "health"
    EVENT_MANAGER = "event_manager"


@dataclass
class ServiceConfig:
    """Configuración base para un servicio"""
    service_id: str
    service_type: ServiceType
    name: str
    version: str
    enabled: bool = True
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class NetworkConfig:
    """Configuración de red para servicios"""
    host: str
    port: int
    bind_address: str = "0.0.0.0"
    tls_enabled: bool = False
    tls_cert: str = ""
    tls_key: str = ""


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    host: str
    port: int
    database: str
    username: str
    password: str
    connection_pool_size: int = 10


@dataclass
class MessageQueueConfig:
    """Configuración de cola de mensajes"""
    broker_url: str
    result_backend: str
    exchange_name: str = "gateway_events"
    queue_name: str = "gateway_queue"


class MicroserviceConfigManager:
    """Gestor de configuración para microservicios"""

    def __init__(self, config_file: str = "microservices_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.services: Dict[str, ServiceConfig] = {}
        self._initialize_services()

    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo o valores por defecto"""
        default_config = {
            "gateway": {
                "service_id": "gw-main-001",
                "service_type": "gateway",
                "name": "Gateway Principal",
                "version": "1.0.0",
                "enabled": True,
                "dependencies": ["plc-adapter-001", "monitoring-001"]
            },
            "plc_adapter": {
                "service_id": "plc-adapter-001",
                "service_type": "plc_adapter",
                "name": "Adaptador PLC",
                "version": "1.0.0",
                "enabled": True,
                "dependencies": []
            },
            "monitoring": {
                "service_id": "monitoring-001",
                "service_type": "monitoring",
                "name": "Servicio de Monitoreo",
                "version": "1.0.0",
                "enabled": True,
                "dependencies": []
            },
            "health": {
                "service_id": "health-001",
                "service_type": "health",
                "name": "Servicio de Salud",
                "version": "1.0.0",
                "enabled": True,
                "dependencies": []
            },
            "event_manager": {
                "service_id": "event-manager-001",
                "service_type": "event_manager",
                "name": "Gestor de Eventos",
                "version": "1.0.0",
                "enabled": True,
                "dependencies": []
            },
            "network": {
                "gateway": {
                    "host": "localhost",
                    "port": 8081,
                    "bind_address": "0.0.0.0"
                },
                "plc_adapter": {
                    "host": "localhost",
                    "port": 8082,
                    "bind_address": "0.0.0.0"
                },
                "monitoring": {
                    "host": "localhost",
                    "port": 8083,
                    "bind_address": "0.0.0.0"
                },
                "health": {
                    "host": "localhost",
                    "port": 8084,
                    "bind_address": "0.0.0.0"
                },
                "event_manager": {
                    "host": "localhost",
                    "port": 8085,
                    "bind_address": "0.0.0.0"
                }
            },
            "message_queue": {
                "broker_url": "redis://localhost:6379/0",
                "result_backend": "redis://localhost:6379/0",
                "exchange_name": "gateway_events",
                "queue_name": "gateway_queue"
            }
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                # Merge con configuración por defecto
                self._merge_config(default_config, file_config)
            except Exception as e:
                print(f"Error cargando configuración de microservicios: {e}")

        return default_config

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Merge de configuración base con override"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _initialize_services(self) -> None:
        """Inicializa los servicios desde la configuración"""
        for service_type in ["gateway", "plc_adapter", "monitoring", "health", "event_manager"]:
            if service_type in self.config:
                service_config = self.config[service_type]
                self.services[service_config["service_id"]] = ServiceConfig(
                    service_id=service_config["service_id"],
                    service_type=ServiceType(service_config["service_type"]),
                    name=service_config["name"],
                    version=service_config["version"],
                    enabled=service_config.get("enabled", True),
                    dependencies=service_config.get("dependencies", [])
                )

    def get_service_config(self, service_id: str) -> Optional[ServiceConfig]:
        """Obtiene la configuración de un servicio específico"""
        return self.services.get(service_id)

    def get_service_configs_by_type(self, service_type: ServiceType) -> List[ServiceConfig]:
        """Obtiene las configuraciones de servicios por tipo"""
        return [service for service in self.services.values()
                if service.service_type == service_type]

    def get_network_config(self, service_type: str) -> NetworkConfig:
        """Obtiene la configuración de red para un tipo de servicio"""
        network_config = self.config.get("network", {}).get(service_type, {})
        return NetworkConfig(
            host=network_config.get("host", "localhost"),
            port=network_config.get("port", 8080),
            bind_address=network_config.get("bind_address", "0.0.0.0"),
            tls_enabled=network_config.get("tls_enabled", False),
            tls_cert=network_config.get("tls_cert", ""),
            tls_key=network_config.get("tls_key", "")
        )

    def get_database_config(self) -> Optional[DatabaseConfig]:
        """Obtiene la configuración de base de datos"""
        db_config = self.config.get("database")
        if db_config:
            return DatabaseConfig(
                host=db_config.get("host", "localhost"),
                port=db_config.get("port", 5432),
                database=db_config.get("database", "gateway"),
                username=db_config.get("username", "gateway"),
                password=db_config.get("password", ""),
                connection_pool_size=db_config.get("connection_pool_size", 10)
            )
        return None

    def get_message_queue_config(self) -> MessageQueueConfig:
        """Obtiene la configuración de cola de mensajes"""
        mq_config = self.config.get("message_queue", {})
        return MessageQueueConfig(
            broker_url=mq_config.get("broker_url", "redis://localhost:6379/0"),
            result_backend=mq_config.get(
                "result_backend", "redis://localhost:6379/0"),
            exchange_name=mq_config.get("exchange_name", "gateway_events"),
            queue_name=mq_config.get("queue_name", "gateway_queue")
        )

    def is_service_enabled(self, service_id: str) -> bool:
        """Verifica si un servicio está habilitado"""
        service_config = self.get_service_config(service_id)
        return service_config.enabled if service_config else False

    def get_enabled_services(self) -> List[ServiceConfig]:
        """Obtiene todos los servicios habilitados"""
        return [service for service in self.services.values() if service.enabled]

    def save_config(self, config_file: Optional[str] = None) -> bool:
        """Guarda la configuración en archivo"""
        try:
            save_path = config_file or self.config_file
            # Convertir servicios a diccionario para guardar
            config_to_save = self.config.copy()
            services_dict = {}
            for service_id, service in self.services.items():
                services_dict[service.service_type.value] = asdict(service)
            config_to_save.update(services_dict)

            with open(save_path, 'w') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando configuración de microservicios: {e}")
            return False


# Instancia global del gestor de configuración
_microservice_config_manager = None


def get_microservice_config_manager() -> MicroserviceConfigManager:
    """Obtiene la instancia global del gestor de configuración de microservicios"""
    global _microservice_config_manager
    if _microservice_config_manager is None:
        _microservice_config_manager = MicroserviceConfigManager()
    return _microservice_config_manager
