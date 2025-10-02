#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente para comunicación con el WMS Cloud
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin


class WMSClient:
    """Cliente para comunicación con el WMS Cloud"""

    def __init__(self, base_url: str, auth_token: str):
        """Inicializa el cliente WMS

        Args:
            base_url: URL base del WMS Cloud
            auth_token: Token de autenticación
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        })

    def register_gateway(self, gateway_info: Dict[str, Any]) -> bool:
        """Registra el Gateway Local con el WMS

        Args:
            gateway_info: Información del Gateway para registro

        Returns:
            bool: True si el registro fue exitoso, False en caso contrario
        """
        try:
            url = urljoin(self.base_url, '/api/v1/gateways/register')
            response = self.session.post(url, json=gateway_info, timeout=30)
            response.raise_for_status()
            self.logger.info("Gateway registrado exitosamente con WMS")
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error registrando Gateway con WMS: {e}")
            return False

    def send_heartbeat(self, heartbeat_data: Dict[str, Any]) -> bool:
        """Envía heartbeat al WMS

        Args:
            heartbeat_data: Datos de estado del Gateway

        Returns:
            bool: True si el heartbeat fue enviado exitosamente
        """
        try:
            url = urljoin(self.base_url, '/api/v1/gateways/heartbeat')
            response = self.session.post(url, json=heartbeat_data, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error enviando heartbeat al WMS: {e}")
            return False

    def send_sensor_data(self, sensor_data: Dict[str, Any]) -> bool:
        """Envía datos de sensores al WMS

        Args:
            sensor_data: Datos de sensores de PLCs

        Returns:
            bool: True si los datos fueron enviados exitosamente
        """
        try:
            url = urljoin(self.base_url, '/api/v1/gateways/sensor-data')
            response = self.session.post(url, json=sensor_data, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error enviando datos de sensores al WMS: {e}")
            return False

    def get_command(self, command_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un comando del WMS

        Args:
            command_id: ID del comando a obtener

        Returns:
            Dict[str, Any]: Datos del comando o None si hay error
        """
        try:
            url = urljoin(
                self.base_url, f'/api/v1/gateways/commands/{command_id}')
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error obteniendo comando del WMS: {e}")
            return None

    def acknowledge_command(self, command_id: str, status: str, result: Dict[str, Any]) -> bool:
        """Acknowledge de un comando al WMS

        Args:
            command_id: ID del comando
            status: Estado del comando (SUCCESS, FAILED, etc.)
            result: Resultado de la ejecución del comando

        Returns:
            bool: True si el acknowledge fue exitoso
        """
        try:
            url = urljoin(
                self.base_url, f'/api/v1/gateways/commands/{command_id}/ack')
            payload = {
                'status': status,
                'result': result
            }
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error enviando acknowledge al WMS: {e}")
            return False
