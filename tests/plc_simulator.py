#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador de PLC Delta AS Series para pruebas del Gateway Local

Este simulador emula el comportamiento de un PLC Delta AS Series
para permitir pruebas de la comunicación sin hardware físico.

Autor: Qoder AI Assistant
Fecha: 2025-10-01
"""

import socket
import struct
import threading
import time
import random


class PLCSimulator:
    """
    Simulador de PLC Delta AS Series que escucha en un puerto TCP/IP
    y responde a comandos con estados simulados.
    """

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.current_status = 0x00  # Estado inicial: listo, parado, manual, sin alarmas
        self.current_position = 0   # Posición inicial

        # Configurar estado inicial simulado
        self._setup_initial_state()

    def _setup_initial_state(self):
        """Configura un estado inicial realista para el PLC"""
        # Bit 0: READY (0 = listo)
        # Bit 1: RUN (0 = parado)
        # Bit 2: MODO_OPERACION (0 = manual)
        # Bit 3: ALARMA (0 = sin alarma)
        # Bit 4: PARADA_EMERGENCIA (1 = sin parada)
        # Bit 5: VFD (0 = OK)
        # Bit 6: ERROR_POSICIONAMIENTO (0 = sin error)
        # Bit 7: SENTIDO_GIRO (0 = ascendente)

        self.current_status = 0x10  # 00010000 en binario

    def start(self):
        """Inicia el servidor de simulación del PLC"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.running = True

            print(f"Simulador de PLC iniciado en {self.host}:{self.port}")
            print("Esperando conexiones...")

            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    print(f"Conexión establecida con {address}")

                    # Manejar la conexión en un hilo separado
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket,)
                    )
                    client_thread.daemon = True
                    client_thread.start()

                except socket.error as e:
                    if self.running:
                        print(f"Error aceptando conexión: {e}")

        except Exception as e:
            print(f"Error iniciando el simulador: {e}")
        finally:
            self.stop()

    def _handle_client(self, client_socket):
        """Maneja la comunicación con un cliente conectado"""
        try:
            while self.running:
                # Recibir comando (1 o 2 bytes)
                data = client_socket.recv(2)
                if not data:
                    break

                if len(data) >= 1:
                    command = data[0]
                    argument = data[1] if len(data) > 1 else None

                    print(
                        f"Comando recibido: {command}, Argumento: {argument}")

                    # Procesar comando y generar respuesta
                    response = self._process_command(command, argument)

                    # Enviar respuesta (2 bytes: status y posición)
                    client_socket.sendall(response)

        except Exception as e:
            print(f"Error manejando cliente: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass

    def _process_command(self, command, argument):
        """
        Procesa un comando recibido y genera una respuesta.

        Protocolo:
        - Comando 0: STATUS - Devuelve estado actual
        - Comando 1: MUEVETE - Mueve a posición especificada
        """
        if command == 0:  # STATUS
            # Devolver estado actual y posición
            response = struct.pack(
                'BB', self.current_status, self.current_position)
            print(
                f"Enviando respuesta STATUS: status={self.current_status}, position={self.current_position}")
            return response

        elif command == 1:  # MUEVETE
            if argument is not None and 0 <= argument <= 9:
                # Simular movimiento
                print(f"Moviendo a posición {argument}")

                # Actualizar posición
                self.current_position = argument

                # Simular estado durante movimiento
                # Bit 1: RUN (1 = en movimiento)
                moving_status = self.current_status | (1 << 1)
                response = struct.pack(
                    'BB', moving_status, self.current_position)
                print(
                    f"Enviando respuesta MOVIMIENTO: status={moving_status}, position={self.current_position}")
                return response
            else:
                # Argumento inválido, devolver error
                # Bit 3: ALARMA (1 = alarma activa)
                error_status = self.current_status | (1 << 3)
                response = struct.pack(
                    'BB', error_status, self.current_position)
                print(
                    f"Enviando respuesta ERROR: status={error_status}, position={self.current_position}")
                return response

        else:
            # Comando desconocido, devolver estado actual
            response = struct.pack(
                'BB', self.current_status, self.current_position)
            print(
                f"Comando desconocido, enviando estado actual: status={self.current_status}, position={self.current_position}")
            return response

    def stop(self):
        """Detiene el simulador"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("Simulador de PLC detenido")


def main():
    """Función principal para ejecutar el simulador"""
    simulator = PLCSimulator()

    try:
        simulator.start()
    except KeyboardInterrupt:
        print("\nDeteniendo simulador...")
        simulator.stop()


if __name__ == "__main__":
    main()
