#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Middleware de seguridad para la API REST del Gateway Local
"""

from functools import wraps
from flask import request, jsonify, g
import re
from typing import Dict, Any


class SecurityMiddleware:
    """Middleware de seguridad para la API"""

    def __init__(self):
        # Patrones de ataques comunes para sanitización
        self.dangerous_patterns = [
            r'<script.*?>.*?</script>',  # XSS
            r'javascript:',  # XSS
            r'on\w+\s*=',  # Event handlers XSS
            r'eval\s*\(',  # Code injection
            r'expression\s*\(',  # CSS injection
            r'data:.*?base64',  # Data URLs
        ]

    def sanitize_input(self, data: Any) -> Any:
        """Sanitiza la entrada de datos"""
        if isinstance(data, str):
            # Remover o escapar caracteres peligrosos
            sanitized = data
            for pattern in self.dangerous_patterns:
                sanitized = re.sub(pattern, '', sanitized,
                                   flags=re.IGNORECASE | re.DOTALL)

            # Limitar la longitud de strings
            if len(sanitized) > 1000:
                sanitized = sanitized[:1000]

            return sanitized
        elif isinstance(data, dict):
            # Sanitizar recursivamente diccionarios
            return {key: self.sanitize_input(value) for key, value in data.items()}
        elif isinstance(data, list):
            # Sanitizar recursivamente listas
            return [self.sanitize_input(item) for item in data]
        else:
            return data

    def validate_input(self, f):
        """Decorador para validar y sanitizar la entrada"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Sanitizar datos JSON si existen
            if request.is_json:
                try:
                    json_data = request.get_json()
                    if json_data:
                        sanitized_data = self.sanitize_input(json_data)
                        # Actualizar el contexto global con datos sanitizados
                        g.sanitized_json = sanitized_data
                except Exception as e:
                    return jsonify({'error': 'Invalid JSON data'}), 400

            # Sanitizar parámetros de query
            sanitized_args = {}
            for key, value in request.args.items():
                sanitized_args[key] = self.sanitize_input(value)
            g.sanitized_args = sanitized_args

            # Sanitizar parámetros de formulario
            sanitized_form = {}
            for key, value in request.form.items():
                sanitized_form[key] = self.sanitize_input(value)
            g.sanitized_form = sanitized_form

            return f(*args, **kwargs)
        return decorated_function

    def add_security_headers(self, response):
        """Añade headers de seguridad a la respuesta"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
