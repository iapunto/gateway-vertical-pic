#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana principal de la GUI del Gateway Local
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from typing import Dict, Any, Optional

from src.database.database_manager import DatabaseManager
from src.core.gateway_core import GatewayCore
from src.gui.dialogs import show_plc_dialog, show_scan_progress_dialog
from src.discovery.plc_discovery import PLCDiscoveryService


class GatewayGUI:
    """Interfaz gráfica de escritorio para el Gateway Local"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gateway Local - Panel de Control")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Variables de la aplicación
        self.db_manager = DatabaseManager()
        self.gateway_core = GatewayCore()
        self.is_running = False

        # Variables de la interfaz
        self.plc_vars = {}
        self.config_vars = {}

        # Servicio de descubrimiento
        self.discovery_service = PLCDiscoveryService()

        # Inicializar la interfaz
        self.setup_ui()

        # Cargar datos iniciales
        self.load_initial_data()

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear las pestañas
        self.create_dashboard_tab()
        self.create_plcs_tab()
        self.create_config_tab()
        self.create_logs_tab()

        # Crear barra de estado
        self.create_status_bar()

    def create_dashboard_tab(self):
        """Crear la pestaña de dashboard"""
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")

        # Estadísticas principales
        stats_frame = ttk.LabelFrame(
            self.dashboard_frame, text="Estadísticas", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        # Contadores
        counters_frame = ttk.Frame(stats_frame)
        counters_frame.pack(fill=tk.X)

        ttk.Label(counters_frame, text="PLCs Conectados:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.plc_count_label = ttk.Label(
            counters_frame, text="0", font=("Arial", 12, "bold"))
        self.plc_count_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(counters_frame, text="Comandos Ejecutados:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.commands_count_label = ttk.Label(
            counters_frame, text="0", font=("Arial", 12, "bold"))
        self.commands_count_label.grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(counters_frame, text="Eventos Registrados:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.events_count_label = ttk.Label(
            counters_frame, text="0", font=("Arial", 12, "bold"))
        self.events_count_label.grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Estado del sistema
        status_frame = ttk.LabelFrame(
            self.dashboard_frame, text="Estado del Sistema", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=10)

        self.system_status_label = ttk.Label(
            status_frame, text="Detenido", foreground="red", font=("Arial", 12, "bold"))
        self.system_status_label.pack()

        # Botones de control
        control_frame = ttk.Frame(self.dashboard_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.start_button = ttk.Button(
            control_frame, text="Iniciar Gateway", command=self.start_gateway)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            control_frame, text="Detener Gateway", command=self.stop_gateway, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Actualizar",
                   command=self.refresh_dashboard).pack(side=tk.RIGHT, padx=5)

    def create_plcs_tab(self):
        """Crear la pestaña de PLCs"""
        self.plcs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plcs_frame, text="PLCs")

        # Frame para botones
        buttons_frame = ttk.Frame(self.plcs_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(buttons_frame, text="Agregar PLC",
                   command=self.add_plc).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Editar PLC",
                   command=self.edit_plc).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Eliminar PLC",
                   command=self.delete_plc).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Escanear PLCs",
                   command=self.scan_plcs).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Actualizar",
                   command=self.refresh_plcs).pack(side=tk.RIGHT, padx=5)

        # Tabla de PLCs
        table_frame = ttk.Frame(self.plcs_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear Treeview para mostrar PLCs
        columns = ("ID", "Nombre", "IP", "Puerto", "Tipo", "Estado")
        self.plcs_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15)

        # Configurar encabezados
        for col in columns:
            self.plcs_tree.heading(col, text=col)
            self.plcs_tree.column(col, width=120)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.plcs_tree.yview)
        h_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.plcs_tree.xview)
        self.plcs_tree.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Empaquetar
        self.plcs_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

    def create_config_tab(self):
        """Crear la pestaña de configuración"""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Configuración")

        # Frame principal de configuración
        main_frame = ttk.Frame(self.config_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de red
        network_frame = ttk.LabelFrame(
            main_frame, text="Configuración de Red", padding=10)
        network_frame.pack(fill=tk.X, padx=5, pady=5)

        # Dirección IP de escucha
        ttk.Label(network_frame, text="Dirección IP:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_vars["bind_address"] = tk.StringVar(value="0.0.0.0")
        ttk.Entry(network_frame, textvariable=self.config_vars["bind_address"], width=20).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Puerto de escucha
        ttk.Label(network_frame, text="Puerto:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_vars["bind_port"] = tk.StringVar(value="8080")
        ttk.Entry(network_frame, textvariable=self.config_vars["bind_port"], width=10).grid(
            row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Puerto PLC
        ttk.Label(network_frame, text="Puerto PLC:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_vars["plc_port"] = tk.StringVar(value="3200")
        ttk.Entry(network_frame, textvariable=self.config_vars["plc_port"], width=10).grid(
            row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Configuración de escaneo
        scan_frame = ttk.LabelFrame(
            main_frame, text="Configuración de Escaneo", padding=10)
        scan_frame.pack(fill=tk.X, padx=5, pady=5)

        # Intervalo de escaneo
        ttk.Label(scan_frame, text="Intervalo (segundos):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_vars["scan_interval"] = tk.StringVar(value="30")
        ttk.Entry(scan_frame, textvariable=self.config_vars["scan_interval"], width=10).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Configuración de logging
        log_frame = ttk.LabelFrame(
            main_frame, text="Configuración de Logging", padding=10)
        log_frame.pack(fill=tk.X, padx=5, pady=5)

        # Nivel de log
        ttk.Label(log_frame, text="Nivel de Log:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_vars["log_level"] = tk.StringVar(value="INFO")
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        ttk.Combobox(log_frame, textvariable=self.config_vars["log_level"], values=log_levels, state="readonly", width=15).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Configuración WMS
        wms_frame = ttk.LabelFrame(
            main_frame, text="Configuración WMS", padding=10)
        wms_frame.pack(fill=tk.X, padx=5, pady=5)

        # Endpoint WMS
        ttk.Label(wms_frame, text="Endpoint:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.config_vars["wms_endpoint"] = tk.StringVar(
            value="https://wms.example.com/api/v1/gateways")
        ttk.Entry(wms_frame, textvariable=self.config_vars["wms_endpoint"], width=50).grid(
            row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(buttons_frame, text="Guardar Configuración",
                   command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Restablecer",
                   command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Actualizar",
                   command=self.refresh_config).pack(side=tk.RIGHT, padx=5)

    def create_logs_tab(self):
        """Crear la pestaña de logs"""
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="Logs")

        # Frame para controles
        controls_frame = ttk.Frame(self.logs_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(controls_frame, text="Limpiar Logs",
                   command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Actualizar",
                   command=self.refresh_logs).pack(side=tk.RIGHT, padx=5)

        # Área de texto para logs
        logs_text_frame = ttk.Frame(self.logs_frame)
        logs_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.logs_text = scrolledtext.ScrolledText(
            logs_text_frame, wrap=tk.WORD, height=20)
        self.logs_text.pack(fill=tk.BOTH, expand=True)

        # Agregar algunos logs de ejemplo
        self.logs_text.insert(tk.END, "Sistema iniciado...\n")
        self.logs_text.insert(tk.END, "Cargando configuración...\n")
        self.logs_text.insert(tk.END, "Conectando a base de datos...\n")

    def create_status_bar(self):
        """Crear la barra de estado"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = ttk.Label(
            self.status_bar, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)

    def load_initial_data(self):
        """Cargar datos iniciales al iniciar la aplicación"""
        self.refresh_dashboard()
        self.refresh_plcs()
        self.refresh_config()

    def refresh_dashboard(self):
        """Actualizar los datos del dashboard"""
        try:
            # Obtener estadísticas de la base de datos
            stats = self.db_manager.get_database_stats()

            # Actualizar contadores
            self.plc_count_label.config(text=str(stats.get("plc_count", 0)))
            self.commands_count_label.config(
                text=str(stats.get("command_count", 0)))
            self.events_count_label.config(
                text=str(stats.get("event_count", 0)))

            # Actualizar estado del sistema
            if self.is_running:
                self.system_status_label.config(
                    text="En Ejecución", foreground="green")
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
            else:
                self.system_status_label.config(
                    text="Detenido", foreground="red")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

        except Exception as e:
            self.show_error(f"Error actualizando dashboard: {e}")

    def refresh_plcs(self):
        """Actualizar la lista de PLCs"""
        try:
            # Limpiar tabla
            for item in self.plcs_tree.get_children():
                self.plcs_tree.delete(item)

            # Obtener PLCs de la base de datos
            plcs = self.db_manager.get_all_plcs()

            # Agregar PLCs a la tabla
            for plc in plcs:
                self.plcs_tree.insert("", tk.END, values=(
                    plc.get("plc_id", ""),
                    plc.get("name", ""),
                    plc.get("ip_address", ""),
                    plc.get("port", ""),
                    plc.get("type", ""),
                    "Desconectado"  # En una implementación real, se verificaría el estado
                ))

        except Exception as e:
            self.show_error(f"Error actualizando PLCs: {e}")

    def refresh_config(self):
        """Actualizar la configuración"""
        try:
            # Obtener configuración de la base de datos
            configs = self.db_manager.get_all_configurations()

            # Actualizar variables de configuración
            config_mapping = {
                "bind_address": "bind_address",
                "bind_port": "bind_port",
                "plc_port": "plc_port",
                "scan_interval": "scan_interval",
                "log_level": "log_level",
                "wms_endpoint": "wms_endpoint"
            }

            for var_name, config_key in config_mapping.items():
                if config_key in configs:
                    self.config_vars[var_name].set(configs[config_key])
                else:
                    # Establecer valores por defecto
                    default_values = {
                        "bind_address": "0.0.0.0",
                        "bind_port": "8080",
                        "plc_port": "3200",
                        "scan_interval": "30",
                        "log_level": "INFO",
                        "wms_endpoint": "https://wms.example.com/api/v1/gateways"
                    }
                    if var_name in default_values:
                        self.config_vars[var_name].set(
                            default_values[var_name])

        except Exception as e:
            self.show_error(f"Error actualizando configuración: {e}")

    def refresh_logs(self):
        """Actualizar los logs"""
        # En una implementación real, se obtendrían los logs de la base de datos
        # Por ahora, solo mostramos un mensaje
        self.logs_text.insert(
            tk.END, f"Actualización de logs: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.logs_text.see(tk.END)

    def start_gateway(self):
        """Iniciar el gateway"""
        try:
            if self.gateway_core.start():
                self.is_running = True
                self.refresh_dashboard()
                self.status_label.config(text="Gateway iniciado")
                self.show_info("Gateway iniciado correctamente")
            else:
                self.show_error("Error al iniciar el gateway")
        except Exception as e:
            self.show_error(f"Error al iniciar el gateway: {e}")

    def stop_gateway(self):
        """Detener el gateway"""
        try:
            self.gateway_core.stop()
            self.is_running = False
            self.refresh_dashboard()
            self.status_label.config(text="Gateway detenido")
            self.show_info("Gateway detenido correctamente")
        except Exception as e:
            self.show_error(f"Error al detener el gateway: {e}")

    def add_plc(self):
        """Agregar un nuevo PLC"""
        result = show_plc_dialog(self.root, "Agregar PLC")
        if result:
            try:
                # Guardar en la base de datos
                success = self.db_manager.add_plc(
                    plc_id=result["plc_id"],
                    name=result["name"],
                    ip_address=result["ip_address"],
                    port=result["port"],
                    plc_type=result["type"],
                    description=result["description"]
                )

                if success:
                    self.refresh_plcs()
                    self.status_label.config(text="PLC agregado correctamente")
                    self.show_info("PLC agregado correctamente")
                else:
                    self.show_error("Error al agregar el PLC")
            except Exception as e:
                self.show_error(f"Error al agregar el PLC: {e}")

    def edit_plc(self):
        """Editar un PLC seleccionado"""
        selected = self.plcs_tree.selection()
        if not selected:
            self.show_warning("Seleccione un PLC para editar")
            return

        # Obtener los datos del PLC seleccionado
        item = self.plcs_tree.item(selected[0])
        values = item["values"]

        if len(values) >= 6:
            plc_id = values[0]
            try:
                # Obtener datos completos del PLC de la base de datos
                plc_data = self.db_manager.get_plc(plc_id)
                if plc_data:
                    result = show_plc_dialog(self.root, "Editar PLC", plc_data)
                    if result:
                        # Actualizar en la base de datos
                        success = self.db_manager.update_plc(
                            plc_id=result["plc_id"],
                            name=result["name"],
                            ip_address=result["ip_address"],
                            port=result["port"],
                            plc_type=result["type"],
                            description=result["description"]
                        )

                        if success:
                            self.refresh_plcs()
                            self.status_label.config(
                                text="PLC actualizado correctamente")
                            self.show_info("PLC actualizado correctamente")
                        else:
                            self.show_error("Error al actualizar el PLC")
                else:
                    self.show_error("No se encontraron datos del PLC")
            except Exception as e:
                self.show_error(f"Error al editar el PLC: {e}")
        else:
            self.show_error("Datos del PLC incompletos")

    def delete_plc(self):
        """Eliminar un PLC seleccionado"""
        selected = self.plcs_tree.selection()
        if not selected:
            self.show_warning("Seleccione un PLC para eliminar")
            return

        # Obtener el ID del PLC seleccionado
        item = self.plcs_tree.item(selected[0])
        values = item["values"]
        if len(values) >= 1:
            plc_id = values[0]

            if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el PLC {plc_id}?"):
                try:
                    # Eliminar de la base de datos
                    success = self.db_manager.remove_plc(plc_id)

                    if success:
                        self.refresh_plcs()
                        self.status_label.config(
                            text="PLC eliminado correctamente")
                        self.show_info("PLC eliminado correctamente")
                    else:
                        self.show_error("Error al eliminar el PLC")
                except Exception as e:
                    self.show_error(f"Error al eliminar el PLC: {e}")
        else:
            self.show_error("No se pudo obtener el ID del PLC")

    def scan_plcs(self):
        """Escanear PLCs en la red"""
        # Crear diálogo de progreso
        progress_dialog = show_scan_progress_dialog(self.root)

        # Ejecutar el escaneo en un hilo separado
        scan_thread = threading.Thread(
            target=self._perform_scan,
            args=(progress_dialog,),
            daemon=True
        )
        scan_thread.start()

    def _perform_scan(self, progress_dialog):
        """Realizar el escaneo de PLCs en un hilo separado"""
        try:
            # Obtener la subred de configuración o usar una por defecto
            config = self.db_manager.get_all_configurations()
            bind_address = config.get("bind_address", "0.0.0.0")

            # Determinar la subred a escanear
            if bind_address == "0.0.0.0" or bind_address == "127.0.0.1":
                # Usar una subred común por defecto
                subnet = "192.168.1.0/24"
            else:
                # Derivar la subred de la dirección de escucha
                parts = bind_address.split(".")
                if len(parts) == 4:
                    subnet = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                else:
                    subnet = "192.168.1.0/24"

            # Callback para actualizar el progreso
            def progress_callback(current, total, device):
                if not progress_dialog.is_cancelled:
                    self.root.after(
                        0, progress_dialog.update_progress, current, total, device)
                else:
                    # Detener el escaneo si se canceló
                    self.discovery_service.stop_discovery()

            # Realizar el escaneo
            devices = self.discovery_service.discover_plcs(
                target=subnet,
                discovery_type="subnet",
                progress_callback=progress_callback
            )

            # Si no se canceló, mostrar resultados
            if not progress_dialog.is_cancelled:
                self.root.after(0, self._handle_scan_results,
                                devices, progress_dialog)

        except Exception as e:
            self.root.after(0, self.show_error,
                            f"Error durante el escaneo: {e}")

    def _handle_scan_results(self, devices, progress_dialog):
        """Manejar los resultados del escaneo"""
        # Cerrar el diálogo de progreso
        progress_dialog.dialog.destroy()

        # Mostrar resultados
        if devices:
            message = f"Se encontraron {len(devices)} PLC(s):\n\n"
            for device in devices:
                message += f"- {device['ip']}:{device['port']} ({device['type']})\n"

            message += "\n¿Desea agregar estos PLCs a la configuración?"

            if messagebox.askyesno("PLCs encontrados", message):
                # Agregar los PLCs encontrados a la base de datos
                self._add_discovered_plcs(devices)
        else:
            self.show_info("No se encontraron PLCs en la red")

    def _add_discovered_plcs(self, devices):
        """Agregar los PLCs descubiertos a la base de datos"""
        try:
            added_count = 0
            for i, device in enumerate(devices):
                # Generar un ID único para el PLC
                plc_id = f"PLC_{device['ip'].replace('.', '_')}_{device['port']}"

                # Verificar si ya existe un PLC con esta IP
                existing_plcs = self.db_manager.get_all_plcs()
                existing_ips = [plc.get("ip_address") for plc in existing_plcs]

                if device['ip'] not in existing_ips:
                    # Generar un nombre descriptivo
                    name = f"PLC_{device['ip']}_{device['port']}"

                    # Agregar a la base de datos
                    success = self.db_manager.add_plc(
                        plc_id=plc_id,
                        name=name,
                        ip_address=device['ip'],
                        port=device['port'],
                        plc_type=device['type'],
                        description=f"PLC descubierto automáticamente en {device['ip']}"
                    )

                    if success:
                        added_count += 1

            # Actualizar la lista de PLCs
            self.refresh_plcs()

            # Mostrar mensaje de éxito
            self.show_info(f"Se agregaron {added_count} PLC(s) nuevos")
            self.status_label.config(
                text=f"Se agregaron {added_count} PLC(s) nuevos")

        except Exception as e:
            self.show_error(f"Error al agregar PLCs descubiertos: {e}")

    def save_config(self):
        """Guardar la configuración"""
        try:
            # Guardar cada configuración en la base de datos
            for key, var in self.config_vars.items():
                db_key = key
                if key == "bind_address":
                    db_key = "bind_address"
                elif key == "bind_port":
                    db_key = "bind_port"
                elif key == "plc_port":
                    db_key = "plc_port"
                elif key == "scan_interval":
                    db_key = "scan_interval"
                elif key == "log_level":
                    db_key = "log_level"
                elif key == "wms_endpoint":
                    db_key = "wms_endpoint"

                value = var.get()
                self.db_manager.set_configuration(db_key, value)

            self.status_label.config(text="Configuración guardada")
            self.show_info("Configuración guardada correctamente")
        except Exception as e:
            self.show_error(f"Error al guardar configuración: {e}")

    def reset_config(self):
        """Restablecer la configuración"""
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea restablecer la configuración?"):
            # Establecer valores por defecto
            default_values = {
                "bind_address": "0.0.0.0",
                "bind_port": "8080",
                "plc_port": "3200",
                "scan_interval": "30",
                "log_level": "INFO",
                "wms_endpoint": "https://wms.example.com/api/v1/gateways"
            }

            for key, value in default_values.items():
                if key in self.config_vars:
                    self.config_vars[key].set(value)

            self.status_label.config(text="Configuración restablecida")
            self.show_info("Configuración restablecida a valores por defecto")

    def clear_logs(self):
        """Limpiar los logs"""
        self.logs_text.delete(1.0, tk.END)
        self.status_label.config(text="Logs limpiados")

    def show_info(self, message):
        """Mostrar mensaje de información"""
        messagebox.showinfo("Información", message)

    def show_warning(self, message):
        """Mostrar mensaje de advertencia"""
        messagebox.showwarning("Advertencia", message)

    def show_error(self, message):
        """Mostrar mensaje de error"""
        messagebox.showerror("Error", message)
        self.status_label.config(text=f"Error: {message}")

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


def main():
    """Función principal para ejecutar la GUI"""
    app = GatewayGUI()
    app.run()


if __name__ == "__main__":
    main()
