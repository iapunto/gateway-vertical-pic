#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rutas para la interfaz web del gateway
"""

import os
from flask import send_from_directory


def register_ui_routes(app):
    """Registra las rutas para la interfaz web"""

    @app.route('/', methods=['GET'])
    def index():
        """Sirve la página principal de la interfaz web"""
        return serve_web_ui(app, 'index.html')

    @app.route('/<path:path>', methods=['GET'])
    def serve_static(path):
        """Sirve archivos estáticos de la interfaz web"""
        return serve_web_ui(app, path)


def serve_web_ui(app, path='index.html'):
    """Sirve la interfaz web del gateway"""
    web_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'web')
    if not os.path.exists(web_dir):
        os.makedirs(web_dir)

    # Si se solicita la raíz, servir index.html
    if path == 'index.html' or path == '/':
        return serve_index_html()

    # Servir archivos estáticos
    try:
        return send_from_directory(web_dir, path)
    except FileNotFoundError:
        return serve_index_html()  # Si el archivo no existe, servir index.html


def serve_index_html():
    """Sirve el archivo index.html con el dashboard"""
    html_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gateway Local - Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #4361ee;
            --secondary: #3f37c9;
            --success: #4cc9f0;
            --info: #4895ef;
            --warning: #f72585;
            --danger: #e63946;
            --light: #f8f9fa;
            --dark: #212529;
            --gray: #6c757d;
            --light-gray: #e9ecef;
            --border-radius: 8px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f7fb;
            color: var(--dark);
            line-height: 1.6;
        }

        .container {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar */
        .sidebar {
            width: 250px;
            background: linear-gradient(180deg, var(--primary), var(--secondary));
            color: white;
            padding: 20px 0;
            transition: var(--transition);
            box-shadow: var(--box-shadow);
        }

        .sidebar-header {
            padding: 0 20px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-header h2 {
            font-weight: 500;
            font-size: 1.5rem;
        }

        .sidebar-menu {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .sidebar-menu li {
            padding: 0;
        }

        .sidebar-menu a {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: var(--transition);
            font-size: 1rem;
        }

        .sidebar-menu a:hover, .sidebar-menu a.active {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }

        .sidebar-menu a i {
            margin-right: 10px;
            font-size: 1.2rem;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--light-gray);
        }

        .header h1 {
            font-weight: 500;
            color: var(--dark);
            font-size: 1.8rem;
        }

        .user-info {
            display: flex;
            align-items: center;
        }

        .user-info img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
            background: var(--light-gray);
        }

        /* Dashboard Grid */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            transition: var(--transition);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .card-header h3 {
            font-weight: 500;
            font-size: 1.2rem;
            color: var(--dark);
        }

        .card-header i {
            font-size: 1.5rem;
            color: var(--primary);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            margin: 10px 0;
        }

        .stat-label {
            color: var(--gray);
            font-size: 0.9rem;
        }

        /* PLC Status */
        .plc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
        }

        .plc-card {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            transition: var(--transition);
        }

        .plc-card.connected {
            border-left: 4px solid #4ade80;
        }

        .plc-card.disconnected {
            border-left: 4px solid var(--danger);
        }

        .plc-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .plc-name {
            font-weight: 500;
            font-size: 1.1rem;
        }

        .plc-status {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .plc-status.connected {
            background: rgba(74, 222, 128, 0.1);
            color: #16a34a;
        }

        .plc-status.disconnected {
            background: rgba(239, 68, 68, 0.1);
            color: #dc2626;
        }

        .plc-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .plc-detail {
            font-size: 0.9rem;
        }

        .plc-detail-label {
            color: var(--gray);
        }

        .plc-detail-value {
            font-weight: 500;
        }

        /* Buttons */
        .btn {
            padding: 10px 15px;
            border-radius: var(--border-radius);
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .btn i {
            margin-right: 5px;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background: var(--secondary);
        }

        .btn-success {
            background: #4ade80;
            color: white;
        }

        .btn-danger {
            background: var(--danger);
            color: white;
        }

        .btn-warning {
            background: #f9c74f;
            color: white;
        }

        /* Configuration Section */
        .config-section {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            margin-bottom: 30px;
        }

        .config-section h2 {
            font-weight: 500;
            margin-bottom: 20px;
            color: var(--dark);
            padding-bottom: 10px;
            border-bottom: 1px solid var(--light-gray);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: var(--dark);
        }

        .form-control {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid var(--light-gray);
            border-radius: var(--border-radius);
            font-family: 'Roboto', sans-serif;
            font-size: 1rem;
            transition: var(--transition);
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
        }

        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        /* Monitoring Section */
        .chart-container {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            margin-bottom: 30px;
        }

        .chart-container h2 {
            font-weight: 500;
            margin-bottom: 20px;
            color: var(--dark);
            padding-bottom: 10px;
            border-bottom: 1px solid var(--light-gray);
        }

        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }

        /* PLC Management */
        .plc-management {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            margin-bottom: 30px;
        }

        .plc-management h2 {
            font-weight: 500;
            margin-bottom: 20px;
            color: var(--dark);
            padding-bottom: 10px;
            border-bottom: 1px solid var(--light-gray);
        }

        .plc-table {
            width: 100%;
            border-collapse: collapse;
        }

        .plc-table th, .plc-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--light-gray);
        }

        .plc-table th {
            background-color: var(--light);
            font-weight: 500;
        }

        .plc-table tr:hover {
            background-color: rgba(67, 97, 238, 0.05);
        }

        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-connected {
            background-color: #4ade80;
        }

        .status-disconnected {
            background-color: var(--danger);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }

            .sidebar {
                width: 100%;
                padding: 10px 0;
            }

            .sidebar-menu {
                display: flex;
                overflow-x: auto;
                padding: 0 10px;
            }

            .sidebar-menu li {
                flex-shrink: 0;
            }

            .sidebar-menu a {
                padding: 10px 15px;
                font-size: 0.9rem;
            }

            .sidebar-menu a i {
                margin-right: 5px;
                font-size: 1rem;
            }

            .dashboard-grid {
                grid-template-columns: 1fr;
            }

            .chart-grid {
                grid-template-columns: 1fr;
            }

            .plc-table {
                font-size: 0.8rem;
            }

            .plc-table th, .plc-table td {
                padding: 8px 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h2><i class="fas fa-industry"></i> Gateway Local</h2>
            </div>
            <ul class="sidebar-menu">
                <li><a href="#" class="active" data-section="dashboard"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li><a href="#" data-section="plcs"><i class="fas fa-microchip"></i> PLCs</a></li>
                <li><a href="#" data-section="config"><i class="fas fa-cogs"></i> Configuración</a></li>
                <li><a href="#" data-section="monitoring"><i class="fas fa-chart-line"></i> Monitoreo</a></li>
                <li><a href="#" data-section="events"><i class="fas fa-bell"></i> Eventos</a></li>
                <li><a href="#" data-section="commands"><i class="fas fa-database"></i> Comandos</a></li>
                <li><a href="#" data-section="health"><i class="fas fa-heartbeat"></i> Salud</a></li>
            </ul>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <div class="header">
                <h1>Dashboard</h1>
                <div class="user-info">
                    <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='8' r='4' fill='%234361ee'/%3E%3Cpath d='M20 20c0-4.418-4.03-8-9-8s-9 3.582-9 8' fill='none' stroke='%234361ee' stroke-width='2'/%3E%3C/svg%3E" alt="User">
                    <span>Administrador</span>
                </div>
            </div>

            <!-- Dashboard Section -->
            <div id="dashboard-section">
                <!-- Stats Cards -->
                <div class="dashboard-grid">
                    <div class="card">
                        <div class="card-header">
                            <h3>Estado del Gateway</h3>
                            <i class="fas fa-server"></i>
                        </div>
                        <div class="stat-number">Activo</div>
                        <div class="stat-label">Gateway en funcionamiento</div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <h3>PLCs Conectados</h3>
                            <i class="fas fa-link"></i>
                        </div>
                        <div class="stat-number">3</div>
                        <div class="stat-label">de 5 configurados</div>
                    </div>

                    <div class="card">
                        <div class="card-header">
                            <h3>Eventos Recientes</h3>
                            <i class="fas fa-bell"></i>
                        </div>
                        <div class="stat-number">24</div>
                        <div class="stat-label">en las últimas 24h</div>
                    </div>
                </div>

                <!-- PLC Status -->
                <h2 style="margin-bottom: 20px; font-weight: 500;">Estado de PLCs</h2>
                <div class="plc-grid">
                    <div class="plc-card connected">
                        <div class="plc-header">
                            <div class="plc-name">Carrusel Principal</div>
                            <div class="plc-status connected">Conectado</div>
                        </div>
                        <div class="plc-details">
                            <div class="plc-detail">
                                <div class="plc-detail-label">ID</div>
                                <div class="plc-detail-value">PLC-001</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">IP</div>
                                <div class="plc-detail-value">192.168.1.50</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">Tipo</div>
                                <div class="plc-detail-value">Delta AS</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">Último comando</div>
                                <div class="plc-detail-value">Mover a posición 5</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px; display: flex; gap: 10px;">
                            <button class="btn btn-primary"><i class="fas fa-play"></i> Enviar Comando</button>
                            <button class="btn btn-danger"><i class="fas fa-power-off"></i> Desconectar</button>
                        </div>
                    </div>

                    <div class="plc-card connected">
                        <div class="plc-header">
                            <div class="plc-name">Carrusel Secundario</div>
                            <div class="plc-status connected">Conectado</div>
                        </div>
                        <div class="plc-details">
                            <div class="plc-detail">
                                <div class="plc-detail-label">ID</div>
                                <div class="plc-detail-value">PLC-002</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">IP</div>
                                <div class="plc-detail-value">192.168.1.51</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">Tipo</div>
                                <div class="plc-detail-value">Delta AS</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">Último comando</div>
                                <div class="plc-detail-value">Obtener estado</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px; display: flex; gap: 10px;">
                            <button class="btn btn-primary"><i class="fas fa-play"></i> Enviar Comando</button>
                            <button class="btn btn-danger"><i class="fas fa-power-off"></i> Desconectar</button>
                        </div>
                    </div>

                    <div class="plc-card disconnected">
                        <div class="plc-header">
                            <div class="plc-name">Carrusel Reserva</div>
                            <div class="plc-status disconnected">Desconectado</div>
                        </div>
                        <div class="plc-details">
                            <div class="plc-detail">
                                <div class="plc-detail-label">ID</div>
                                <div class="plc-detail-value">PLC-003</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">IP</div>
                                <div class="plc-detail-value">192.168.1.52</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">Tipo</div>
                                <div class="plc-detail-value">Delta AS</div>
                            </div>
                            <div class="plc-detail">
                                <div class="plc-detail-label">Último intento</div>
                                <div class="plc-detail-value">Hace 5 minutos</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px; display: flex; gap: 10px;">
                            <button class="btn btn-primary"><i class="fas fa-redo"></i> Reconectar</button>
                            <button class="btn btn-danger"><i class="fas fa-trash"></i> Eliminar</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Configuration Section -->
            <div id="config-section" style="display: none;">
                <div class="config-section">
                    <h2><i class="fas fa-cog"></i> Configuración del Gateway</h2>
                    <form id="gateway-config-form">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="gateway-id">ID del Gateway</label>
                                <input type="text" id="gateway-id" class="form-control" value="GW-001">
                            </div>
                            <div class="form-group">
                                <label for="gateway-name">Nombre del Gateway</label>
                                <input type="text" id="gateway-name" class="form-control" value="Gateway Local Principal">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="bind-address">Dirección IP para escuchar</label>
                                <input type="text" id="bind-address" class="form-control" value="0.0.0.0">
                            </div>
                            <div class="form-group">
                                <label for="bind-port">Puerto para la API</label>
                                <input type="number" id="bind-port" class="form-control" value="8080">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="log-level">Nivel de Log</label>
                            <select id="log-level" class="form-control">
                                <option value="DEBUG">DEBUG</option>
                                <option value="INFO" selected>INFO</option>
                                <option value="WARNING">WARNING</option>
                                <option value="ERROR">ERROR</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Guardar Configuración</button>
                    </form>
                </div>

                <div class="config-section">
                    <h2><i class="fas fa-cloud"></i> Configuración del WMS</h2>
                    <form id="wms-config-form">
                        <div class="form-group">
                            <label for="wms-endpoint">Endpoint del WMS</label>
                            <input type="url" id="wms-endpoint" class="form-control" value="https://wms.example.com/api/v1/gateways">
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="auth-token">Token de Autenticación</label>
                                <input type="password" id="auth-token" class="form-control" value="TOKEN_DE_AUTENTICACION_DEL_WMS">
                            </div>
                            <div class="form-group">
                                <label for="reconnect-interval">Intervalo de Reconexión (segundos)</label>
                                <input type="number" id="reconnect-interval" class="form-control" value="30">
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Guardar Configuración</button>
                    </form>
                </div>

                <div class="config-section">
                    <h2><i class="fas fa-microchip"></i> Configuración de PLCs</h2>
                    <div class="form-group">
                        <button class="btn btn-primary" id="add-plc-btn"><i class="fas fa-plus"></i> Añadir Nuevo PLC</button>
                    </div>
                    <div id="plc-list">
                        <!-- PLC items will be added here dynamically -->
                        <div class="plc-config-item card" style="margin-bottom: 15px;">
                            <div class="form-row">
                                <div class="form-group">
                                    <label>ID del PLC</label>
                                    <input type="text" class="form-control" value="PLC-001">
                                </div>
                                <div class="form-group">
                                    <label>Nombre</label>
                                    <input type="text" class="form-control" value="Carrusel Principal">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Dirección IP</label>
                                    <input type="text" class="form-control" value="192.168.1.50">
                                </div>
                                <div class="form-group">
                                    <label>Puerto</label>
                                    <input type="number" class="form-control" value="3200">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Tipo de PLC</label>
                                    <select class="form-control">
                                        <option value="delta" selected>Delta AS Series</option>
                                        <option value="siemens">Siemens S7</option>
                                        <option value="allen-bradley">Allen-Bradley</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Descripción</label>
                                    <input type="text" class="form-control" value="PLC Delta AS Series principal">
                                </div>
                            </div>
                            <div style="display: flex; gap: 10px;">
                                <button class="btn btn-success"><i class="fas fa-save"></i> Guardar</button>
                                <button class="btn btn-danger"><i class="fas fa-trash"></i> Eliminar</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Monitoring Section -->
            <div id="monitoring-section" style="display: none;">
                <div class="chart-container">
                    <h2><i class="fas fa-chart-line"></i> Métricas en Tiempo Real</h2>
                    <div class="chart-grid">
                        <div>
                            <canvas id="cpuChart"></canvas>
                        </div>
                        <div>
                            <canvas id="memoryChart"></canvas>
                        </div>
                    </div>
                </div>

                <div class="chart-container">
                    <h2><i class="fas fa-exchange-alt"></i> Tráfico de Comunicaciones</h2>
                    <div class="chart-grid">
                        <div>
                            <canvas id="networkChart"></canvas>
                        </div>
                        <div>
                            <canvas id="plcResponseChart"></canvas>
                        </div>
                    </div>
                </div>

                <div class="chart-container">
                    <h2><i class="fas fa-microchip"></i> Estado de PLCs</h2>
                    <div>
                        <canvas id="plcStatusChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- PLC Management Section -->
            <div id="plcs-section" style="display: none;">
                <div class="plc-management">
                    <h2><i class="fas fa-microchip"></i> Gestión de PLCs</h2>
                    <div class="form-group">
                        <button class="btn btn-primary" id="discover-plcs-btn"><i class="fas fa-search"></i> Descubrir PLCs en Red</button>
                        <button class="btn btn-success" id="add-plc-manual-btn"><i class="fas fa-plus"></i> Añadir PLC Manualmente</button>
                    </div>
                    <table class="plc-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nombre</th>
                                <th>Dirección IP</th>
                                <th>Tipo</th>
                                <th>Estado</th>
                                <th>Última Conexión</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>PLC-001</td>
                                <td>Carrusel Principal</td>
                                <td>192.168.1.50</td>
                                <td>Delta AS</td>
                                <td><span class="status-indicator status-connected"></span> Conectado</td>
                                <td>Hace 2 minutos</td>
                                <td>
                                    <button class="btn btn-primary btn-sm"><i class="fas fa-play"></i></button>
                                    <button class="btn btn-warning btn-sm"><i class="fas fa-sync"></i></button>
                                    <button class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                                </td>
                            </tr>
                            <tr>
                                <td>PLC-002</td>
                                <td>Carrusel Secundario</td>
                                <td>192.168.1.51</td>
                                <td>Delta AS</td>
                                <td><span class="status-indicator status-connected"></span> Conectado</td>
                                <td>Hace 5 minutos</td>
                                <td>
                                    <button class="btn btn-primary btn-sm"><i class="fas fa-play"></i></button>
                                    <button class="btn btn-warning btn-sm"><i class="fas fa-sync"></i></button>
                                    <button class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                                </td>
                            </tr>
                            <tr>
                                <td>PLC-003</td>
                                <td>Carrusel Reserva</td>
                                <td>192.168.1.52</td>
                                <td>Delta AS</td>
                                <td><span class="status-indicator status-disconnected"></span> Desconectado</td>
                                <td>Hace 15 minutos</td>
                                <td>
                                    <button class="btn btn-primary btn-sm"><i class="fas fa-play"></i></button>
                                    <button class="btn btn-warning btn-sm"><i class="fas fa-sync"></i></button>
                                    <button class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                                </td>
                            </tr>
                            <tr>
                                <td>PLC-004</td>
                                <td>Carrusel Almacén</td>
                                <td>192.168.1.53</td>
                                <td>Delta AS</td>
                                <td><span class="status-indicator status-disconnected"></span> No Configurado</td>
                                <td>-</td>
                                <td>
                                    <button class="btn btn-success btn-sm"><i class="fas fa-plus"></i></button>
                                    <button class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Funcionalidad básica del dashboard
        document.addEventListener('DOMContentLoaded', function() {
            // Manejar clics en el menú
            const menuItems = document.querySelectorAll('.sidebar-menu a');
            const sections = ['dashboard', 'plcs', 'config', 'monitoring', 'events', 'commands', 'health'];
            
            menuItems.forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const section = this.getAttribute('data-section');
                    
                    // Actualizar menú activo
                    menuItems.forEach(i => i.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Mostrar sección correspondiente
                    sections.forEach(sec => {
                        const sectionElement = document.getElementById(`${sec}-section`);
                        if (sectionElement) {
                            sectionElement.style.display = sec === section ? 'block' : 'none';
                        }
                    });
                    
                    // Actualizar título
                    document.querySelector('.header h1').textContent = 
                        this.textContent.trim().replace(/^\s*\S+\s*/, '');
                    
                    // Inicializar gráficos si es la sección de monitoreo
                    if (section === 'monitoring') {
                        initializeCharts();
                    }
                });
            });

            // Manejar formulario de configuración del gateway
            const gatewayConfigForm = document.getElementById('gateway-config-form');
            if (gatewayConfigForm) {
                gatewayConfigForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    alert('Configuración del gateway guardada correctamente');
                });
            }

            // Manejar formulario de configuración del WMS
            const wmsConfigForm = document.getElementById('wms-config-form');
            if (wmsConfigForm) {
                wmsConfigForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    alert('Configuración del WMS guardada correctamente');
                });
            }

            // Manejar botón de añadir PLC
            const addPlcBtn = document.getElementById('add-plc-btn');
            if (addPlcBtn) {
                addPlcBtn.addEventListener('click', function() {
                    alert('Funcionalidad de añadir PLC pendiente de implementar');
                });
            }

            // Manejar botón de descubrir PLCs
            const discoverPlcsBtn = document.getElementById('discover-plcs-btn');
            if (discoverPlcsBtn) {
                discoverPlcsBtn.addEventListener('click', function() {
                    alert('Iniciando descubrimiento de PLCs en red...');
                });
            }

            // Manejar botón de añadir PLC manualmente
            const addPlcManualBtn = document.getElementById('add-plc-manual-btn');
            if (addPlcManualBtn) {
                addPlcManualBtn.addEventListener('click', function() {
                    alert('Mostrando formulario para añadir PLC manualmente...');
                });
            }

            // Función para inicializar gráficos
            function initializeCharts() {
                // Gráfico de CPU
                const cpuCtx = document.getElementById('cpuChart').getContext('2d');
                const cpuChart = new Chart(cpuCtx, {
                    type: 'line',
                    data: {
                        labels: Array.from({length: 10}, (_, i) => `${i*5}s`),
                        datasets: [{
                            label: 'Uso de CPU (%)',
                            data: Array.from({length: 10}, () => Math.floor(Math.random() * 30) + 20),
                            borderColor: '#4361ee',
                            backgroundColor: 'rgba(67, 97, 238, 0.1)',
                            tension: 0.4,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: false
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });

                // Gráfico de Memoria
                const memoryCtx = document.getElementById('memoryChart').getContext('2d');
                const memoryChart = new Chart(memoryCtx, {
                    type: 'line',
                    data: {
                        labels: Array.from({length: 10}, (_, i) => `${i*5}s`),
                        datasets: [{
                            label: 'Uso de Memoria (%)',
                            data: Array.from({length: 10}, () => Math.floor(Math.random() * 40) + 30),
                            borderColor: '#4cc9f0',
                            backgroundColor: 'rgba(76, 201, 240, 0.1)',
                            tension: 0.4,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: false
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });

                // Gráfico de Tráfico de Red
                const networkCtx = document.getElementById('networkChart').getContext('2d');
                const networkChart = new Chart(networkCtx, {
                    type: 'bar',
                    data: {
                        labels: ['Entrada', 'Salida'],
                        datasets: [{
                            label: 'Tráfico (KB/s)',
                            data: [Math.floor(Math.random() * 100) + 50, Math.floor(Math.random() * 100) + 50],
                            backgroundColor: ['#4895ef', '#4cc9f0']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });

                // Gráfico de Tiempo de Respuesta de PLCs
                const plcResponseCtx = document.getElementById('plcResponseChart').getContext('2d');
                const plcResponseChart = new Chart(plcResponseCtx, {
                    type: 'bar',
                    data: {
                        labels: ['PLC-001', 'PLC-002', 'PLC-003'],
                        datasets: [{
                            label: 'Tiempo de Respuesta (ms)',
                            data: [Math.floor(Math.random() * 50) + 10, Math.floor(Math.random() * 50) + 15, Math.floor(Math.random() * 100) + 50],
                            backgroundColor: ['#4ade80', '#4ade80', '#f72585']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });

                // Gráfico de Estado de PLCs
                const plcStatusCtx = document.getElementById('plcStatusChart').getContext('2d');
                const plcStatusChart = new Chart(plcStatusCtx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Conectados', 'Desconectados', 'Errores'],
                        datasets: [{
                            data: [3, 1, 1],
                            backgroundColor: ['#4ade80', '#f72585', '#f9c74f']
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'right'
                            }
                        }
                    }
                });

                // Simular actualización de datos en tiempo real
                setInterval(() => {
                    // Actualizar datos de CPU
                    const cpuData = cpuChart.data.datasets[0].data;
                    cpuData.push(Math.floor(Math.random() * 30) + 20);
                    if (cpuData.length > 10) cpuData.shift();
                    cpuChart.update();

                    // Actualizar datos de Memoria
                    const memoryData = memoryChart.data.datasets[0].data;
                    memoryData.push(Math.floor(Math.random() * 40) + 30);
                    if (memoryData.length > 10) memoryData.shift();
                    memoryChart.update();

                    // Actualizar datos de tráfico de red
                    networkChart.data.datasets[0].data = [
                        Math.floor(Math.random() * 100) + 50,
                        Math.floor(Math.random() * 100) + 50
                    ];
                    networkChart.update();

                    // Actualizar datos de tiempo de respuesta
                    plcResponseChart.data.datasets[0].data = [
                        Math.floor(Math.random() * 50) + 10,
                        Math.floor(Math.random() * 50) + 15,
                        Math.floor(Math.random() * 100) + 50
                    ];
                    plcResponseChart.update();
                }, 5000); // Actualizar cada 5 segundos
            }

            // Simular actualización de datos en tiempo real
            setInterval(() => {
                // Aquí iría la lógica para actualizar los datos desde la API
                console.log('Actualizando datos...');
            }, 30000); // Actualizar cada 30 segundos
        });
    </script>
</body>
</html>
    '''
    return html_content, 200, {'Content-Type': 'text/html'}
