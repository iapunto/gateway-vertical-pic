#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Middleware de rate limiting para la API REST del Gateway Local
"""

from functools import wraps
from flask import request, jsonify
from collections import defaultdict
import time
from typing import Dict, Tuple


class RateLimitMiddleware:
    """Middleware de rate limiting para la API"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)  # ip: [timestamps]

    def is_rate_limited(self, ip: str) -> bool:
        """Verifica si una IP ha excedido el límite de requests"""
        now = time.time()

        # Limpiar requests antiguos fuera de la ventana
        self.requests[ip] = [
            timestamp for timestamp in self.requests[ip]
            if now - timestamp < self.window_seconds
        ]

        # Verificar si se ha excedido el límite
        return len(self.requests[ip]) >= self.max_requests

    def record_request(self, ip: str) -> None:
        """Registra un request para una IP"""
        now = time.time()
        self.requests[ip].append(now)

    def rate_limit(self, f):
        """Decorador para aplicar rate limiting"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener la IP del cliente
            ip = request.remote_addr or 'unknown'

            # Verificar si está rate limited
            if self.is_rate_limited(ip):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {self.max_requests} requests per {self.window_seconds} seconds'
                }), 429

            # Registrar el request
            self.record_request(ip)

            return f(*args, **kwargs)
        return decorated_function
