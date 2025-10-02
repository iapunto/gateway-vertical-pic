#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador de PLC para pruebas locales del Gateway
"""

import socket
import struct
import threading
import time
import logging
from typing import Dict, Any, Optional


class PLCSimulator:
    """Simulador de PLC Delta AS Series para pruebas locales"""

    def __init__(self, host: str = "127.0.0.1", port: int = 3200):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.position = 0
        self.logger = logging.getLogger(__name__)
        self.clients = []
        self.server_thread = None

    def start(self) -> bool:
        """Inicia el servidor del simulador de PLC"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True

            self.server_thread = threading.Thread(
                target=self._server_worker, daemon=True)
            self.server_thread.start()

            self.logger.info(
                f"Simulador de PLC iniciado en {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Error iniciando simulador de PLC: {e}")
            return False

    def stop(self) -> None:
        """Detiene el servidor del simulador de PLC"""
        self.running = False

        # Cerrar conexiones de clientes
        for client_socket in self.clients:
            try:
                client_socket.close()
            except:
                pass
        self.clients.clear()

        # Cerrar socket del servidor
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        self.logger.info("Simulador de PLC detenido")

    def _server_worker(self) -> None:
        """Worker del servidor que acepta conexiones"""
        if not self.socket:
            return

        while self.running:
            try:
                client_socket, address = self.socket.accept()
                self.logger.info(f"Nueva conexión desde {address}")

                # Crear hilo para manejar al cliente
                client_thread = threading.Thread(
                    target=self._client_handler,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()

            except socket.error:
                if self.running:
                    self.logger.error("Error aceptando conexión")
                break
            except Exception as e:
                if self.running:
                    self.logger.error(f"Error inesperado: {e}")
                break

    def _client_handler(self, client_socket: socket.socket, address: tuple) -> None:
        """Maneja las comunicaciones con un cliente"""
        self.clients.append(client_socket)

        try:
            while self.running:
                # Recibir comando
                data = client_socket.recv(2)
                if not data:
                    break

                if len(data) < 1:
                    continue

                command = struct.unpack('B', data[0:1])[0]
                argument = None
                if len(data) > 1:
                    argument = struct.unpack('B', data[1:2])[0]

                self.logger.info(
                    f"Comando recibido: {command}, Argumento: {argument}")

                # Procesar comando y enviar respuesta
                response = self._process_command(command, argument)
                client_socket.sendall(response)

        except Exception as e:
            self.logger.error(f"Error manejando cliente {address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            try:
                client_socket.close()
            except:
                pass

    def _process_command(self, command: int, argument: Optional[int] = None) -> bytes:
        """Procesa un comando y retorna la respuesta"""
        try:
            if command == 0:  # STATUS
                # Retornar estado: código de estado (0) y posición actual
                return struct.pack('BB', 0, self.position)
            elif command == 1:  # MUEVETE
                # Mover a posición especificada
                if argument is not None:
                    self.position = argument
                    self.logger.info(f"Moviendo a posición {self.position}")
                # Retornar estado: código de estado (0) y nueva posición
                return struct.pack('BB', 0, self.position)
            else:
                # Comando desconocido, retornar error
                self.logger.warning(f"Comando desconocido: {command}")
                return struct.pack('BB', 1, self.position)  # Código de error 1
        except Exception as e:
            self.logger.error(f"Error procesando comando {command}: {e}")
            return struct.pack('BB', 255, self.position)  # Código de error 255


def main():
    """Función principal para ejecutar el simulador"""
    import argparse
    import sys

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description="Simulador de PLC Delta")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Dirección IP para escuchar")
    parser.add_argument("--port", type=int, default=3200,
                        help="Puerto para escuchar")

    args = parser.parse_args()

    print(f"Iniciando simulador de PLC en {args.host}:{args.port}")
    print("Presione Ctrl+C para detener")

    simulator = PLCSimulator(args.host, args.port)

    try:
        if not simulator.start():
            print("Error iniciando el simulador")
            sys.exit(1)

        # Mantener el proceso vivo
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDeteniendo simulador...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        simulator.stop()


if __name__ == "__main__":
    main()
