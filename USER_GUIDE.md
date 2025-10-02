# Guía de Usuario del Gateway Local

## Introducción

El Gateway Local es una aplicación que permite la comunicación entre PLCs Delta AS Series y nuestro sistema WMS en la nube. Actúa como un puente entre el hardware local y el software en la nube, permitiendo el control remoto de los carruseles verticales PIC.

## Arquitectura

El Gateway Local se compone de los siguientes componentes:

1. **Core del sistema**: Orquesta todas las operaciones del gateway
2. **Comunicación con PLCs**: Se comunica con los PLCs Delta a través de TCP/IP
3. **Comunicación con WMS**: Se conecta con nuestro sistema en la nube
4. **API REST**: Permite el control remoto del gateway
5. **Sistema de monitoreo**: Registra métricas y estado del sistema
6. **Sistema de eventos**: Maneja notificaciones y callbacks
7. **Túnel reverso**: Permite la comunicación bidireccional con el WMS a través de firewalls
8. **Descubrimiento de PLCs**: Escanea la red para encontrar automáticamente PLCs

## Configuración

### Archivo de configuración

El archivo `gateway_config.json` contiene toda la configuración del gateway:

```json
{
  "gateway": {
    "id": "GW-001",
    "name": "Gateway Local Principal",
    "version": "2.7.0"
  },
  "wms": {
    "endpoint": "https://wms.example.com/api/v1/gateways",
    "auth_token": "TOKEN_DE_AUTENTICACION",
    "reconnect_interval": 30,
    "heartbeat_interval": 60
  },
  "network": {
    "bind_address": "0.0.0.0",
    "bind_port": 8080,
    "plc_port": 3200
  },
  "security": {
    "tls_cert": "",
    "tls_key": "",
    "ca_cert": "",
    "require_tls": false
  },
  "logging": {
    "level": "INFO",
    "file": "logs/gateway.log",
    "max_size": 10485760,
    "backup_count": 5
  },
  "plcs": [
    {
      "id": "PLC-001",
      "type": "delta",
      "name": "Carrusel Principal",
      "ip": "192.168.1.50",
      "port": 3200,
      "description": "PLC Delta AS Series principal"
    }
  ]
}
```

### Parámetros de configuración

#### Gateway

- `id`: Identificador único del gateway
- `name`: Nombre descriptivo del gateway
- `version`: Versión del gateway

#### WMS

- `endpoint`: URL del endpoint del WMS
- `auth_token`: Token de autenticación para el WMS
- `reconnect_interval`: Intervalo de reconexión en segundos
- `heartbeat_interval`: Intervalo de envío de heartbeat en segundos

#### Network

- `bind_address`: Dirección IP para escuchar conexiones
- `bind_port`: Puerto para la API REST
- `plc_port`: Puerto para conexiones con PLCs

#### Security

- `tls_cert`: Ruta al certificado TLS
- `tls_key`: Ruta a la clave privada TLS
- `ca_cert`: Ruta al certificado CA
- `require_tls`: Requerir TLS para todas las conexiones

#### Logging

- `level`: Nivel de log (DEBUG, INFO, WARNING, ERROR)
- `file`: Archivo de log
- `max_size`: Tamaño máximo del archivo de log en bytes
- `backup_count`: Número de archivos de respaldo

#### PLCs

- `id`: Identificador único del PLC
- `type`: Tipo de PLC (actualmente solo "delta")
- `name`: Nombre descriptivo del PLC
- `ip`: Dirección IP del PLC
- `port`: Puerto del PLC
- `description`: Descripción del PLC

## Descubrimiento Automático de PLCs

### Funcionalidad

El Gateway Local incluye una función de descubrimiento automático de PLCs que permite escanear la red en busca de dispositivos PLC Vertical PIC que estén escuchando en el puerto 3200.

### Métodos de escaneo

1. **Escaneo de red local**: Escanea automáticamente todas las redes a las que está conectado el sistema
2. **Escaneo de subred específica**: Permite escanear una subred en particular
3. **Escaneo de rango de IPs**: Permite definir un rango específico de direcciones IP a escanear

### Uso del descubrimiento

#### Desde la línea de comandos

```bash
# Escanear toda la red local
python discover_plcs.py

# Escanear una subred específica
python discover_plcs.py --subnet 192.168.1.0/24

# Escanear un rango de IPs
python discover_plcs.py --start-ip 192.168.1.10 --end-ip 192.168.1.50

# Escanear con más hilos para mayor velocidad
python discover_plcs.py --workers 100 --verbose

# Guardar resultados en archivo JSON
python discover_plcs.py --output plcs_encontrados.json
```

#### Scripts de inicio

También se proporcionan scripts convenientes para iniciar el descubrimiento:

- **Windows**: `start_discovery.bat`
- **Linux/Mac**: `start_discovery.sh`

### Resultados del descubrimiento

El proceso de descubrimiento identifica los siguientes datos de cada PLC encontrado:

- Dirección IP
- Puerto
- Tipo de PLC (Delta AS Series)
- Estado actual
- Posición del carrusel

### Integración con la configuración

Una vez identificados los PLCs, pueden añadirse fácilmente al archivo de configuración `gateway_config.json` para que el gateway los controle.

## Conectividad con el WMS

### Túnel HTTP Reverso

El Gateway Local utiliza un túnel HTTP reverso para comunicarse con el WMS en la nube. Esta técnica permite que el WMS envíe comandos al gateway incluso cuando este está detrás de un firewall o NAT.

El túnel funciona de la siguiente manera:

1. El gateway inicia una conexión saliente con el WMS
2. El WMS puede enviar comandos a través de esta conexión persistente
3. El gateway ejecuta los comandos y devuelve los resultados

Esta arquitectura elimina la necesidad de configurar puertos de entrada en el firewall del cliente.

### Registro con el WMS

Cuando el gateway se inicia, se registra automáticamente con el WMS utilizando el token de autenticación proporcionado en la configuración.

### Heartbeats

El gateway envía heartbeats periódicos al WMS para informar que está en línea y operativo. El intervalo de heartbeats se configura en el archivo `gateway_config.json`.

## Uso del Gateway

### Iniciar el Gateway

Para iniciar el gateway, ejecute uno de los scripts de inicio creados durante la instalación:

**Modo API (recomendado):**

- Windows: `start_gateway.bat`
- Linux/Mac: `./start_gateway.sh`

**Modo Standalone:**

- Windows: `start_gateway_standalone.bat`
- Linux/Mac: `./start_gateway_standalone.sh`

### API REST

Cuando el gateway se inicia en modo API, expone una interfaz REST en el puerto configurado (por defecto 8080).

#### Endpoints disponibles

##### Estado del sistema

- `GET /health`: Verifica el estado del gateway
- `GET /metrics`: Obtiene métricas del sistema

##### Control de PLCs

- `GET /api/v1/status`: Obtiene el estado de todos los PLCs
- `GET /api/v1/status/{machine_id}`: Obtiene el estado de un PLC específico
- `GET /api/v1/machines`: Obtiene la lista de máquinas disponibles
- `POST /api/v1/command`: Envía un comando personalizado
- `POST /api/v1/move/{position}`: Mueve un carrusel a una posición específica

##### Control del Gateway

- `POST /api/v1/start`: Inicia el gateway
- `POST /api/v1/stop`: Detiene el gateway

#### Ejemplos de uso

##### Obtener estado de todos los PLCs

```bash
curl http://localhost:8080/api/v1/status
```

##### Obtener estado de un PLC específico

```bash
curl http://localhost:8080/api/v1/status/PLC-001
```

##### Mover carrusel a posición 5

```bash
curl -X POST http://localhost:8080/api/v1/move/5 \
  -H "Content-Type: application/json" \
  -d '{"machine_id": "PLC-001"}'
```

##### Enviar comando personalizado

```bash
curl -X POST http://localhost:8080/api/v1/command \
  -H "Content-Type: application/json" \
  -d '{"command": 1, "argument": 10, "machine_id": "PLC-001"}'
```

### Comandos del WMS

El WMS puede enviar los siguientes tipos de comandos al gateway a través del túnel reverso:

1. **get_status**: Obtiene el estado de un PLC o de todos los PLCs
2. **send_command**: Envía un comando personalizado a un PLC
3. **move_to_position**: Mueve un carrusel a una posición específica

### Monitoreo

El gateway registra información detallada en archivos de log ubicados en el directorio `logs/`. Los niveles de log configurables son:

- `DEBUG`: Información detallada para diagnóstico
- `INFO`: Información general sobre el funcionamiento
- `WARNING`: Advertencias que no detienen el funcionamiento
- `ERROR`: Errores que pueden afectar el funcionamiento

### Eventos

El sistema de eventos notifica sobre cambios importantes en el estado del gateway y los PLCs. Los eventos se registran en los logs y pueden ser utilizados para integraciones adicionales.

## Mantenimiento

### Actualización

Para actualizar el gateway a una nueva versión:

1. Detenga el gateway si está en ejecución
2. Descargue la nueva versión
3. Ejecute el script de instalación nuevamente
4. Verifique la configuración
5. Inicie el gateway

### Copias de seguridad

Es recomendable hacer copias de seguridad del archivo `gateway_config.json` antes de realizar cambios importantes en la configuración.

### Monitoreo de logs

Revise regularmente los archivos de log en el directorio `logs/` para identificar posibles problemas o patrones de uso.

## Seguridad

### Autenticación

El gateway se autentica con el WMS mediante un token de autenticación configurado en el archivo `gateway_config.json`.

### Comunicaciones

Las comunicaciones con el WMS se realizan a través de HTTPS para garantizar la seguridad de los datos.

### Acceso local

El acceso a la API REST local puede restringirse configurando la dirección IP de escucha en el archivo de configuración.

## Solución de problemas de conectividad

### Problemas de conexión con el WMS

1. **Verifique el token de autenticación**: Asegúrese de que el token en la configuración sea correcto
2. **Verifique la conectividad de red**: Asegúrese de que el gateway pueda acceder a Internet
3. **Verifique el endpoint del WMS**: Confirme que la URL del endpoint sea correcta
4. **Revise los logs**: Los logs pueden contener información detallada sobre errores de conexión

### Problemas con el túnel reverso

1. **Verifique que el gateway esté en línea**: Los heartbeats deben estar llegando al WMS
2. **Revise los logs del túnel**: Busque mensajes de error relacionados con el túnel reverso
3. **Verifique el firewall**: Asegúrese de que las conexiones salientes no estén bloqueadas

### Problemas de descubrimiento de PLCs

1. **Verifique la conectividad de red**: Asegúrese de que el sistema pueda acceder a las redes donde están los PLCs
2. **Verifique el puerto**: Confirme que los PLCs estén escuchando en el puerto 3200
3. **Revise los logs**: Los logs pueden contener información sobre errores de conexión

## Soporte

Para obtener soporte técnico, contacte con nuestro equipo de soporte indicando:

1. Versión del gateway
2. Sistema operativo utilizado
3. Descripción detallada del problema
4. Archivos de log relevantes
