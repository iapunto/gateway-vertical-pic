#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de verificación de salud para el Gateway Local
"""

import time
from typing import Dict, Any, List
from datetime import datetime


class HealthChecker:
    """Verificador de salud del sistema"""

    def __init__(self, gateway_core):
        self.gateway_core = gateway_core
        self.checks = {
            'gateway_status': self._check_gateway_status,
            'plc_connections': self._check_plc_connections,
            'system_resources': self._check_system_resources,
            'network_connectivity': self._check_network_connectivity
        }

    def _check_gateway_status(self) -> Dict[str, Any]:
        """Verifica el estado del gateway"""
        return {
            'name': 'Gateway Status',
            'status': 'healthy' if self.gateway_core.running else 'unhealthy',
            'message': 'Gateway is running' if self.gateway_core.running else 'Gateway is stopped',
            'timestamp': datetime.now().isoformat()
        }

    def _check_plc_connections(self) -> Dict[str, Any]:
        """Verifica las conexiones a PLCs"""
        connected_plcs = 0
        total_plcs = len(self.gateway_core.plcs)

        for plc in self.gateway_core.plcs.values():
            if plc.is_connected():
                connected_plcs += 1

        status = 'healthy' if connected_plcs == total_plcs else 'degraded'
        message = f'{connected_plcs}/{total_plcs} PLCs connected'

        return {
            'name': 'PLC Connections',
            'status': status,
            'message': message,
            'details': {
                'connected': connected_plcs,
                'total': total_plcs
            },
            'timestamp': datetime.now().isoformat()
        }

    def _check_system_resources(self) -> Dict[str, Any]:
        """Verifica los recursos del sistema"""
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Determinar estado basado en uso de recursos
            cpu_status = 'healthy' if cpu_percent < 80 else 'warning'
            memory_status = 'healthy' if memory.percent < 80 else 'warning'
            disk_status = 'healthy' if disk.percent < 80 else 'warning'

            # Estado general (el peor de todos)
            overall_status = 'healthy'
            if 'warning' in [cpu_status, memory_status, disk_status]:
                overall_status = 'warning'
            if 'unhealthy' in [cpu_status, memory_status, disk_status]:
                overall_status = 'unhealthy'

            return {
                'name': 'System Resources',
                'status': overall_status,
                'message': 'System resources check completed',
                'details': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'cpu_status': cpu_status,
                    'memory_status': memory_status,
                    'disk_status': disk_status
                },
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'name': 'System Resources',
                'status': 'unknown',
                'message': f'Error checking system resources: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }

    def _check_network_connectivity(self) -> Dict[str, Any]:
        """Verifica la conectividad de red"""
        try:
            import socket

            # Verificar conectividad con algunos PLCs configurados
            plc_configs = self.gateway_core.config_manager.get_plc_list()
            reachable_count = 0
            total_count = len(plc_configs)

            for plc_config in plc_configs:
                ip = plc_config.get('ip')
                port = plc_config.get('port', 3200)

                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex((ip, port))
                    sock.close()

                    if result == 0:
                        reachable_count += 1
                except:
                    pass

            status = 'healthy' if reachable_count == total_count else 'degraded'
            message = f'{reachable_count}/{total_count} PLCs reachable'

            return {
                'name': 'Network Connectivity',
                'status': status,
                'message': message,
                'details': {
                    'reachable': reachable_count,
                    'total': total_count
                },
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'name': 'Network Connectivity',
                'status': 'unknown',
                'message': f'Error checking network connectivity: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }

    def get_health_status(self) -> Dict[str, Any]:
        """Obtiene el estado de salud completo del sistema"""
        check_results = []
        overall_status = 'healthy'

        for check_name, check_function in self.checks.items():
            try:
                result = check_function()
                check_results.append(result)

                # Actualizar estado general
                if result['status'] == 'unhealthy':
                    overall_status = 'unhealthy'
                elif result['status'] == 'degraded' and overall_status == 'healthy':
                    overall_status = 'degraded'
                elif result['status'] == 'warning' and overall_status == 'healthy':
                    overall_status = 'warning'

            except Exception as e:
                error_result = {
                    'name': check_name,
                    'status': 'error',
                    'message': f'Error executing health check: {str(e)}',
                    'timestamp': datetime.now().isoformat()
                }
                check_results.append(error_result)
                overall_status = 'unhealthy'

        return {
            'status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'checks': check_results
        }

    def get_simple_status(self) -> str:
        """Obtiene un estado simple del sistema"""
        health = self.get_health_status()
        return health['status']
