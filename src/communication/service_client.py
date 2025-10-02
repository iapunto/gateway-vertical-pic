#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente para comunicación entre microservicios del Gateway Local
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin
from dataclasses import dataclass
from enum import Enum


class ServiceStatus(Enum):
    """Estados posibles de un servicio"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ServiceInfo:
    """Información básica de un servicio"""
    service_id: str
    name: str
    version: str
    status: ServiceStatus
    host: str
    port: int
    url: str


class ServiceClient:
    """Cliente para comunicación con microservicios"""

    def __init__(self, service_url: str, timeout: int = 30):
        """Inicializa el cliente de servicio"""
        self.service_url = service_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Realiza una solicitud HTTP al servicio"""
        url = urljoin(self.service_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            
            # Intentar parsear JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                # Si no es JSON, devolver el texto
                return {"text": response.text}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error en solicitud a {url}: {e}")
            return None

    def get_health(self) -> Optional[Dict[str, Any]]:
        """Obtiene el estado de salud del servicio"""
        return self._make_request("GET", "/health")

    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """Obtiene las métricas del servicio"""
        return self._make_request("GET", "/metrics")

    def get_service_info(self) -> Optional[ServiceInfo]:
        """Obtiene información básica del servicio"""
        health = self.get_health()
        if health:
            return ServiceInfo(
                service_id=health.get("service_id", "unknown"),
                name=health.get("name", "unknown"),
                version=health.get("version", "unknown"),
                status=ServiceStatus(health.get("status", "unknown")),
                host=self.service_url,
                port=0,  # Puerto no disponible desde la URL
                url=self.service_url
            )
        return None

    def send_command(self, command: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Envía un comando al servicio"""
        return self._make_request(
            "POST", 
            f"/api/v1/commands/{command}",
            json=data,
            headers={"Content-Type": "application/json"}
        )

    def get_resource(self, resource: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Obtiene un recurso del servicio"""
        return self._make_request(
            "GET",
            f"/api/v1/resources/{resource}",
            params=params
        )

    def post_resource(self, resource: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un recurso en el servicio"""
        return self._make_request(
            "POST",
            f"/api/v1/resources/{resource}",
            json=data,
            headers={"Content-Type": "application/json"}
        )

    def put_resource(self, resource: str, resource_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un recurso en el servicio"""
        return self._make_request(
            "PUT",
            f"/api/v1/resources/{resource}/{resource_id}",
            json=data,
            headers={"Content-Type": "application/json"}
        )

    def delete_resource(self, resource: str, resource_id: str) -> Optional[Dict[str, Any]]:
        """Elimina un recurso del servicio"""
        return self._make_request(
            "DELETE",
            f"/api/v1/resources/{resource}/{resource_id}"
        )


class ServiceRegistry:
    """Registro de servicios disponibles"""

    def __init__(self):
        self.services: Dict[str, ServiceClient] = {}
        self.logger = logging.getLogger(__name__)

    def register_service(self, service_id: str, service_url: str, timeout: int = 30) -> None:
        """Registra un servicio en el registro"""
        self.services[service_id] = ServiceClient(service_url, timeout)
        self.logger.info(f"Servicio registrado: {service_id} -> {service_url}")

    def unregister_service(self, service_id: str) -> bool:
        """Elimina un servicio del registro"""
        if service_id in self.services:
            del self.services[service_id]
            self.logger.info(f"Servicio desregistrado: {service_id}")
            return True
        return False

    def get_service(self, service_id: str) -> Optional[ServiceClient]:
        """Obtiene un cliente para un servicio específico"""
        return self.services.get(service_id)

    def get_all_services(self) -> Dict[str, ServiceClient]:
        """Obtiene todos los servicios registrados"""
        return self.services.copy()

    def get_healthy_services(self) -> Dict[str, ServiceClient]:
        """Obtiene solo los servicios que están saludables"""
        healthy_services = {}
        for service_id, client in self.services.items():
            try:
                health = client.get_health()
                if health and health.get("status") == "healthy":
                    healthy_services[service_id] = client
            except Exception as e:
                self.logger.warning(f"Error verificando salud de {service_id}: {e}")
        return healthy_services

    def broadcast_command(self, command: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envía un comando a todos los servicios registrados"""
        results = {}
        for service_id, client in self.services.items():
            try:
                result = client.send_command(command, data)
                results[service_id] = result
            except Exception as e:
                self.logger.error(f"Error enviando comando a {service_id}: {e}")
                results[service_id] = {"error": str(e)}
        return results


# Instancia global del registro de servicios
_service_registry = ServiceRegistry()


def get_service_registry() -> ServiceRegistry:
    """Obtiene la instancia global del registro de servicios"""
    return _service_registry


def register_service(service_id: str, service_url: str, timeout: int = 30) -> None:
    """Registra un servicio globalmente"""
    _service_registry.register_service(service_id, service_url, timeout)


def get_service_client(service_id: str) -> Optional[ServiceClient]:
    """Obtiene un cliente para un servicio específico"""
    return _service_registry.get_service(service_id)