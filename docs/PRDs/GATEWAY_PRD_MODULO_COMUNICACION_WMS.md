# 🌐 Gateway Local PRD - Módulo de Comunicación con WMS

## 📋 Resumen Ejecutivo

Este documento detalla los requisitos específicos para el Módulo de Comunicación con WMS del Gateway Local. Este módulo es responsable de establecer y mantener la conexión segura con el WMS en la nube, autenticar el Gateway, y manejar el intercambio bidireccional de comandos y datos.

El módulo se implementará en Python, utilizando las librerías estándar y de terceros apropiadas para comunicación segura HTTP/WebSocket.

## 🎯 Objetivos del Módulo

- Establecer conexión segura y persistente con el WMS Cloud
- Autenticar el Gateway Local utilizando certificados digitales
- Manejar el intercambio eficiente de mensajes con el WMS
- Implementar mecanismos de resiliencia ante fallos de red
- Proporcionar monitoreo y diagnóstico de la comunicación

## 👥 Usuarios y Sistemas Involucrados

- **WMS en la Nube**: Sistema central que envía comandos y recibe datos
- **Gateway Local**: Sistema que actúa como intermediario de comunicación
- **Administrador del Sistema**: Personal de TI que configura y monitorea
- **Sistema de Monitoreo**: Herramientas que supervisan el estado de comunicaciones

## 📋 Requisitos Funcionales

### RF-001: Establecimiento de Conexión

- El sistema debe establecer conexión HTTPS segura con el WMS Cloud
- Debe utilizar certificados TLS 1.3 para encriptación de comunicaciones
- Debe validar certificado del servidor WMS antes de establecer conexión
- Debe manejar diferentes endpoints del WMS para alta disponibilidad

### RF-002: Autenticación y Registro

- El sistema debe autenticarse con el WMS utilizando certificados TLS mutuos
- Debe registrar el Gateway enviando información de identificación única
- Debe renovar tokens de autenticación automáticamente antes de expiración
- Debe manejar procesos de re-registro en caso de reconexión

### RF-003: Envío de Datos al WMS

- El sistema debe enviar datos de sensores de PLCs al WMS en tiempo real
- Debe incluir identificadores de tenant, gateway y PLC en cada mensaje
- Debe manejar compresión de datos para optimizar ancho de banda
- Debe implementar mecanismos de confirmación de recepción

### RF-004: Recepción de Comandos del WMS

- El sistema debe recibir comandos del WMS y enrutarlos a PLCs correspondientes
- Debe validar la integridad y autenticidad de los comandos recibidos
- Debe manejar diferentes tipos de comandos (movimiento, consulta, configuración)
- Debe confirmar recepción de comandos al WMS

### RF-005: Heartbeat y Monitoreo

- El sistema debe enviar heartbeats periódicos al WMS para mantener conexión activa
- Debe incluir métricas de estado en heartbeats (CPU, memoria, conectividad)
- Debe recibir heartbeats del WMS para confirmar disponibilidad
- Debe generar alertas si se detectan problemas de conectividad

### RF-006: Manejo de Reconexión

- El sistema debe reconectarse automáticamente al WMS en caso de pérdida de conexión
- Debe implementar backoff exponencial para reintentos de conexión
- Debe almacenar temporalmente datos pendientes durante desconexión
- Debe sincronizar estado con el WMS tras reconexión exitosa

## ⚙️ Requisitos No Funcionales

### RNF-001: Seguridad

- Toda la comunicación debe estar encriptada con TLS 1.3
- Los certificados deben rotarse automáticamente cada 90 días
- Las claves privadas deben almacenarse de forma segura y encriptada
- Todas las operaciones deben quedar registradas en logs de auditoría

### RNF-002: Rendimiento

- La latencia de envío de mensajes debe ser < 1 segundo
- El sistema debe manejar al menos 1000 mensajes por minuto
- El uso de CPU para comunicación no debe exceder 30%
- El consumo de memoria para buffering no debe exceder 100MB

### RNF-003: Disponibilidad

- El sistema debe tener una disponibilidad del 99.95%
- Debe recuperarse de fallos de red en < 30 segundos
- Debe mantener operación con un WMS de respaldo si es configurado
- Debe notificar al WMS sobre su estado de disponibilidad

### RNF-004: Escalabilidad

- El sistema debe soportar actualización de endpoints del WMS sin reinicio
- Debe permitir configuración de múltiples WMS para failover
- Debe manejar aumento de volumen de mensajes sin degradación
- Debe permitir ajuste de parámetros de comunicación en caliente

## 🔄 Flujos de Trabajo Principales

### Flujo 1: Conexión Inicial con WMS

1. Gateway inicia proceso de conexión con endpoint del WMS
2. Se establece handshake TLS y se validan certificados
3. Gateway envía solicitud de registro con información de identificación
4. WMS valida registro y responde con token de autenticación
5. Se establece sesión activa y comienza intercambio de heartbeats
6. Gateway notifica estado operativo al WMS

### Flujo 2: Envío de Datos de Sensores

1. PLC reporta datos de sensores al Gateway
2. Gateway procesa y estructura datos para envío
3. Se incluyen identificadores de contexto (tenant, gateway, PLC)
4. Datos se envían al WMS a través de conexión segura
5. WMS confirma recepción de datos
6. Gateway registra operación en logs

### Flujo 3: Recepción y Ejecución de Comandos

1. WMS envía comando al Gateway a través de conexión segura
2. Gateway valida autenticidad e integridad del comando
3. Se identifica PLC destino del comando
4. Comando se encola para envío al PLC correspondiente
5. Gateway confirma recepción del comando al WMS
6. Se ejecuta comando en PLC y se reporta resultado

### Flujo 4: Manejo de Desconexión

1. Gateway detecta pérdida de conectividad con WMS
2. Se inicia proceso de reconexión con backoff exponencial
3. Datos se almacenan temporalmente en buffer
4. Se continúa operación local con PLCs
5. Al restablecerse conexión, se sincronizan datos pendientes
6. Se notifica estado operativo al WMS

## 📊 KPIs y Métricas

- **Latencia de Comunicación**: < 1 segundo promedio
- **Tasa de Éxito de Envío**: > 99.9%
- **Tiempo de Reconexión**: < 30 segundos
- **Throughput de Mensajes**: > 1000 mensajes/minuto
- **Uptime de Conexión**: > 99.95%
- **Tiempo Medio de Respuesta**: < 500 milisegundos

## 🔧 Consideraciones Técnicas

### Tecnología de Implementación

- **Lenguaje**: Python 3.9+
- **Librerías Principales**:
  - `requests` o `httpx` para comunicaciones HTTP
  - `websockets` para comunicación WebSocket
  - `ssl` para manejo de certificados TLS
  - `json` para serialización de mensajes
- **Concurrencia**: `asyncio` para operaciones no bloqueantes
- **Gestión de Certificados**: `cryptography` para manejo de certificados

### Protocolos de Comunicación

- **HTTPS**: Para comunicación segura con WMS
- **WebSocket**: Para comunicación bidireccional en tiempo real
- **JSON**: Para estructura de mensajes
- **TLS 1.3**: Para encriptación de todas las comunicaciones

### Gestión de Certificados

- **Almacenamiento Seguro**: Claves privadas en almacenamiento encriptado
- **Rotación Automática**: Renovación de certificados cada 90 días
- **Validación de Cadena**: Verificación completa de cadena de certificados
- **Revocación**: Manejo de certificados revocados

### Buffering y Almacenamiento Temporal

- **Cola de Mensajes**: Almacenamiento temporal de mensajes pendientes
- **Persistencia Local**: Guardado de datos críticos en disco
- **Límites de Almacenamiento**: Configuración de tamaño máximo de buffer
- **Política de Eliminación**: Estrategia para manejo de buffer lleno

### Manejo de Errores

- **Reintentos Inteligentes**: Backoff exponencial para reintentos
- **Logging de Errores**: Registro detallado de errores de comunicación
- **Notificaciones de Alerta**: Envío de alertas por problemas persistentes
- **Modo Degradado**: Operación limitada durante problemas de conectividad
