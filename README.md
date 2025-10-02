# Gateway Local

## Descripción

Implementación modular del Gateway Local para comunicación con PLCs de racks verticales, evolución del Carousel API existente.

## Arquitectura Modular

La nueva arquitectura sigue principios de diseño limpio y separación de responsabilidades:

```
gateway/
├── src/                    # Código fuente del Gateway
│   ├── api/               # API REST para control remoto
│   ├── core/              # Core del sistema y orquestación
│   ├── plc/               # Implementaciones específicas de PLCs
│   ├── interfaces/        # Interfaces comunes
│   ├── config/            # Gestión de configuración
│   ├── wms/               # Comunicación con WMS cloud
│   ├── utils/             # Utilidades y herramientas
│   ├── adapters/          # Adaptadores para compatibilidad
│   └── main.py            # Punto de entrada
├── tests/                 # Pruebas unitarias e integración
├── docs/                  # Documentación técnica
├── requirements.txt       # Dependencias de Python
├── gateway_config.json    # Configuración principal
└── README.md              # Este archivo
```

## Componentes Principales

### Core (`src/core/`)

- **gateway_core.py**: Orquestador principal del sistema
- Gestiona el ciclo de vida del gateway
- Coordina la comunicación entre componentes

### PLC (`src/plc/`)

- **delta_plc.py**: Implementación específica para PLC Delta AS Series
- **plc_factory.py**: Fábrica para crear instancias de PLCs
- **plc_simulator.py**: Simulador de PLC para pruebas locales
- Diseñado para fácil extensión a otras marcas de PLC

### Interfaces (`src/interfaces/`)

- **plc_interface.py**: Interface común para todos los PLCs
- Permite polimorfismo y fácil sustitución de implementaciones

### Configuración (`src/config/`)

- **config_manager.py**: Gestor centralizado de configuración
- Soporta configuración por archivos JSON

### WMS (`src/wms/`)

- **wms_client.py**: Cliente para comunicación con WMS cloud
- Implementa registro, heartbeat y sincronización

### Utilidades (`src/utils/`)

- **logger.py**: Sistema de logging centralizado

### Adaptadores (`src/adapters/`)

- **api_adapter.py**: Mantiene compatibilidad con API existente

### API REST (`src/api/`)

- **gateway_api.py**: API REST para control remoto del gateway
- Permite controlar el gateway sin necesidad del WMS

## Extensibilidad

Para añadir soporte para un nuevo tipo de PLC:

1. Crear una nueva implementación en `src/plc/`
2. Implementar la interface `PLCInterface`
3. Registrar el nuevo tipo en `PLCFactory`
4. Añadir configuración en `gateway_config.json`

## Desarrollo

### Configuración del entorno

1. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Windows
   source venv/bin/activate      # En Linux/Mac
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

#### Modo standalone (sin API):
```bash
cd src
python main.py
```

#### Modo con API REST:
```bash
cd src
python main.py --api --host 0.0.0.0 --port 8080
```

O usando los scripts proporcionados:
```bash
# En Windows
start_api.bat

# En Linux/Mac
./start_api.sh
```

### Pruebas

Ejecutar todas las pruebas:
```bash
python run_tests.py
```

Ejecutar pruebas específicas:
```bash
python run_tests.py --unit
python run_tests.py --integration
python run_tests.py --plc
```

### API REST

La API REST permite controlar el gateway de forma remota. Consulta [docs/API_REST.md](docs/API_REST.md) para más detalles.

#### Endpoints principales:
- `GET /api/v1/status` - Obtener estado de todos los PLCs
- `GET /api/v1/status/{machine_id}` - Obtener estado de un PLC específico
- `POST /api/v1/move/{position}` - Mover carrusel a una posición
- `POST /api/v1/command` - Enviar comando personalizado

### Simulador de PLC

Para pruebas locales sin hardware real, se incluye un simulador de PLC:

```bash
cd src/plc
python plc_simulator.py
```

## Comandos PLC

- **Comando 0 (STATUS)**: Obtiene el estado actual del PLC
- **Comando 1 (MUEVETE)**: Mueve el carrusel a una posición específica

## Compatibilidad

Este componente mantiene compatibilidad con la versión actual del Carousel API v2.6.1

## Flujo de trabajo GIT

Siga el flujo de trabajo GIT definido en [docs/GIT_WORKFLOW_GATEWAY.md](docs/GIT_WORKFLOW_GATEWAY.md)