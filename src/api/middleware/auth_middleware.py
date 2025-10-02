#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Middleware de autenticación para la API REST del Gateway Local
"""

import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify, g
from typing import Dict, Any, Optional


class AuthMiddleware:
    """Middleware de autenticación para la API"""

    def __init__(self, secret_key: str = "default_secret_key"):
        self.secret_key = secret_key
        self.users: Dict[str, str] = {}  # username: hashed_password

    def register_user(self, username: str, password: str) -> bool:
        """Registra un nuevo usuario"""
        try:
            # Hashear la contraseña
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.users[username] = hashed.decode('utf-8')
            return True
        except Exception as e:
            print(f"Error registrando usuario: {e}")
            return False

    def authenticate_user(self, username: str, password: str) -> bool:
        """Autentica un usuario"""
        if username not in self.users:
            return False

        try:
            hashed_password = self.users[username].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        except Exception as e:
            print(f"Error autenticando usuario: {e}")
            return False

    def generate_token(self, username: str) -> str:
        """Genera un token JWT para un usuario"""
        try:
            payload = {
                'username': username,
                # En producción, usar expiración
            }
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            return token
        except Exception as e:
            print(f"Error generando token: {e}")
            return ""

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica un token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def require_auth(self, f):
        """Decorador para requerir autenticación"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Obtener el token del header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'error': 'Token requerido'}), 401

            # Verificar formato del header
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Formato de token inválido'}), 401

            # Extraer el token
            token = auth_header.split(' ')[1]

            # Verificar el token
            payload = self.verify_token(token)
            if not payload:
                return jsonify({'error': 'Token inválido'}), 401

            # Agregar el usuario al contexto global
            g.current_user = payload

            return f(*args, **kwargs)
        return decorated_function
