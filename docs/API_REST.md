# API REST del Gateway Local

## Descripción

La API REST del Gateway Local permite controlar y monitorear el gateway de forma remota a través de HTTP. Proporciona endpoints para obtener el estado de los PLCs, enviar comandos y gestionar el gateway.

## Endpoints

### Obtener estado de todos los PLCs

```
GET /api/v1/status
```

**Respuesta:**

```json
{
  "success": true,
  "data": {
    "PLC-001": {
      "plc_id": "PLC-001",
      "connected": true,
      "status": {
        "status_code": 0,
        "position": 3,
        "success": true
      },
      "success": true
    }
  }
}
```

### Obtener estado de un PLC específico

```
GET /api/v1/status/{machine_id}
```

**Parámetros:**

- `machine_id`: ID del PLC

**Respuesta:**

```json
{
  "plc_id": "PLC-001",
  "connected": true,
  "status": {
    "status_code": 0,
    "position": 3,
    "success": true
  },
  "success": true
}
```

### Obtener lista de máquinas disponibles

```
GET /api/v1/machines
```

**Respuesta:**

```json
{
  "success": true,
  "data": [
    {
      "id": "PLC-001",
      "type": "PLC",
      "status": "connected"
    }
  ]
}
```

### Enviar comando a un PLC

```
POST /api/v1/command
```

**Cuerpo de la solicitud:**

```json
{
  "command": 1,
  "argument": 5,
  "machine_id": "PLC-001"
}
```

**Respuesta:**

```json
{
  "plc_id": "PLC-001",
  "command": 1,
  "argument": 5,
  "result": {
    "status_code": 0,
    "position": 5,
    "success": true
  },
  "success": true
}
```

### Mover carrusel a una posición

```
POST /api/v1/move/{position}
```

**Parámetros:**

- `position`: Posición a la que mover el carrusel

**Cuerpo de la solicitud (opcional):**

```json
{
  "machine_id": "PLC-001"
}
```

**Respuesta:**

```json
{
  "plc_id": "PLC-001",
  "command": 1,
  "argument": 5,
  "result": {
    "status_code": 0,
    "position": 5,
    "success": true
  },
  "success": true
}
```

### Iniciar el gateway

```
POST /api/v1/start
```

**Respuesta:**

```json
{
  "message": "Gateway iniciado exitosamente",
  "success": true
}
```

### Detener el gateway

```
POST /api/v1/stop
```

**Respuesta:**

```json
{
  "message": "Gateway detenido exitosamente",
  "success": true
}
```

### Verificación de salud del sistema

```
GET /health
```

**Respuesta:**

```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T12:00:00Z",
  "checks": [
    {
      "name": "Gateway Status",
      "status": "healthy",
      "message": "Gateway is running",
      "timestamp": "2023-01-01T12:00:00Z"
    },
    {
      "name": "PLC Connections",
      "status": "healthy",
      "message": "2/2 PLCs connected",
      "details": {
        "connected": 2,
        "total": 2
      },
      "timestamp": "2023-01-01T12:00:00Z"
    }
  ]
}
```

### Métricas del sistema (Prometheus)

```
GET /metrics
```

**Respuesta:**

```
# TYPE gateway_status gauge
gateway_status 1.0
# TYPE plc_connections gauge
plc_connections 2.0
# TYPE commands_sent counter
commands_sent{plc_id="PLC-001",command="1"} 5.0
# TYPE position_changes counter
position_changes{plc_id="PLC-001"} 5.0
# TYPE current_positions gauge
current_positions{plc_id="PLC-001"} 3.0
```

## Códigos de comando

- **0**: STATUS - Obtiene el estado actual del PLC
- **1**: MUEVETE - Mueve el carrusel a una posición específica

## Ejemplos de uso

### Obtener estado de todos los PLCs

```bash
curl http://localhost:8080/api/v1/status
```

### Mover carrusel a posición 3

```bash
curl -X POST http://localhost:8080/api/v1/move/3
```

### Enviar comando personalizado

```bash
curl -X POST http://localhost:8080/api/v1/command \
  -H "Content-Type: application/json" \
  -d '{"command": 1, "argument": 5, "machine_id": "PLC-001"}'
```

### Verificar salud del sistema

```bash
curl http://localhost:8080/health
```

### Obtener métricas

```bash
curl http://localhost:8080/metrics
```
