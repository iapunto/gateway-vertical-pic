#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogos personalizados para la GUI del Gateway Local
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any


class PLCDialog:
    """Diálogo para agregar/editar PLCs"""

    def __init__(self, parent, title="PLC", plc_data=None):
        self.parent = parent
        self.plc_data = plc_data or {}
        self.result = None

        # Crear la ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        # Centrar el diálogo
        self.center_window()

        # Hacer que el diálogo sea modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Crear la interfaz
        self.setup_ui()

        # Cargar datos si es edición
        if self.plc_data:
            self.load_plc_data()

        # Esperar a que se cierre el diálogo
        self.dialog.wait_window()

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - \
            (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - \
            (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ID del PLC
        ttk.Label(main_frame, text="ID del PLC:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(
            main_frame, textvariable=self.id_var, width=30)
        self.id_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Nombre del PLC
        ttk.Label(main_frame, text="Nombre:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            main_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Dirección IP
        ttk.Label(main_frame, text="Dirección IP:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(
            main_frame, textvariable=self.ip_var, width=30)
        self.ip_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Puerto
        ttk.Label(main_frame, text="Puerto:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.port_var = tk.StringVar(value="3200")
        self.port_entry = ttk.Entry(
            main_frame, textvariable=self.port_var, width=10)
        self.port_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Tipo de PLC
        ttk.Label(main_frame, text="Tipo:").grid(
            row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.type_var = tk.StringVar(value="delta")
        types = ["delta", "siemens", "allen-bradley"]
        self.type_combo = ttk.Combobox(
            main_frame, textvariable=self.type_var, values=types, state="readonly", width=27)
        self.type_combo.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        # Descripción
        ttk.Label(main_frame, text="Descripción:").grid(
            row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(
            main_frame, textvariable=self.desc_var, width=30)
        self.desc_entry.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        # Botones
        ttk.Button(button_frame, text="Cancelar",
                   command=self.cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Guardar",
                   command=self.save).pack(side=tk.RIGHT, padx=5)

        # Enfocar el primer campo
        self.id_entry.focus()

    def load_plc_data(self):
        """Cargar datos del PLC en el diálogo"""
        self.id_var.set(self.plc_data.get("plc_id", ""))
        self.name_var.set(self.plc_data.get("name", ""))
        self.ip_var.set(self.plc_data.get("ip_address", ""))
        self.port_var.set(str(self.plc_data.get("port", "3200")))
        self.type_var.set(self.plc_data.get("type", "delta"))
        self.desc_var.set(self.plc_data.get("description", ""))

    def save(self):
        """Guardar los datos del PLC"""
        # Validar datos
        if not self.id_var.get().strip():
            messagebox.showwarning(
                "Advertencia", "El ID del PLC es obligatorio")
            return

        if not self.name_var.get().strip():
            messagebox.showwarning(
                "Advertencia", "El nombre del PLC es obligatorio")
            return

        if not self.ip_var.get().strip():
            messagebox.showwarning(
                "Advertencia", "La dirección IP es obligatoria")
            return

        try:
            port = int(self.port_var.get())
            if port < 1 or port > 65535:
                raise ValueError("Puerto fuera de rango")
        except ValueError:
            messagebox.showwarning(
                "Advertencia", "El puerto debe ser un número válido entre 1 y 65535")
            return

        # Crear diccionario con los datos
        self.result = {
            "plc_id": self.id_var.get().strip(),
            "name": self.name_var.get().strip(),
            "ip_address": self.ip_var.get().strip(),
            "port": port,
            "type": self.type_var.get(),
            "description": self.desc_var.get().strip()
        }

        # Cerrar el diálogo
        self.dialog.destroy()

    def cancel(self):
        """Cancelar y cerrar el diálogo"""
        self.dialog.destroy()


class ScanProgressDialog:
    """Diálogo para mostrar el progreso del escaneo de PLCs"""

    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.devices_found = []

        # Crear la ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Escaneando PLCs")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)

        # Centrar el diálogo
        self.center_window()

        # Hacer que el diálogo sea modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Crear la interfaz
        self.setup_ui()

        # Variables para el progreso
        self.is_cancelled = False

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - \
            (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - \
            (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")

    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Etiqueta de estado
        self.status_label = ttk.Label(
            main_frame, text="Iniciando escaneo...", font=("Arial", 10))
        self.status_label.pack(pady=10)

        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)

        # Etiqueta de progreso
        self.progress_label = ttk.Label(main_frame, text="0%")
        self.progress_label.pack(pady=5)

        # Etiqueta de dispositivos encontrados
        self.devices_label = ttk.Label(
            main_frame, text="Dispositivos encontrados: 0")
        self.devices_label.pack(pady=5)

        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # Botón de cancelar
        self.cancel_button = ttk.Button(
            button_frame, text="Cancelar", command=self.cancel)
        self.cancel_button.pack()

    def update_progress(self, current, total, device=None):
        """Actualizar el progreso del escaneo"""
        if self.is_cancelled:
            return

        # Calcular porcentaje
        percentage = (current / total) * 100 if total > 0 else 0
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage:.1f}%")

        # Actualizar estado
        if device:
            self.devices_found.append(device)
            self.status_label.config(
                text=f"Dispositivo encontrado: {device['ip']}")
            self.devices_label.config(
                text=f"Dispositivos encontrados: {len(self.devices_found)}")
        else:
            self.status_label.config(text=f"Escaneando... ({current}/{total})")

        # Actualizar la interfaz
        self.dialog.update_idletasks()

    def cancel(self):
        """Cancelar el escaneo"""
        self.is_cancelled = True
        self.dialog.destroy()

    def show_results(self, devices):
        """Mostrar los resultados del escaneo"""
        self.devices_found = devices
        self.dialog.destroy()


def show_plc_dialog(parent, title="PLC", plc_data=None):
    """Mostrar el diálogo de PLC y devolver los datos"""
    dialog = PLCDialog(parent, title, plc_data)
    return dialog.result


def show_scan_progress_dialog(parent):
    """Mostrar el diálogo de progreso del escaneo"""
    dialog = ScanProgressDialog(parent)
    return dialog


# Ejemplo de uso:
if __name__ == "__main__":
    # Crear una ventana de prueba
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Mostrar el diálogo
    result = show_plc_dialog(root, "Agregar PLC")
    if result:
        print("Datos del PLC:", result)
    else:
        print("Operación cancelada")
