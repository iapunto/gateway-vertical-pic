# Guía de Solución de Problemas del Gateway Local

## Problemas comunes y soluciones

### 1. El gateway no se inicia

#### Síntomas

- Mensaje de error al iniciar el gateway
- El proceso se cierra inmediatamente
- No se puede acceder a la API

#### Posibles causas y soluciones

**Falta de dependencias**

- _Síntoma_: Errores de importación de módulos
- _Solución_: Ejecute el script de instalación nuevamente:
  ```bash
  python install_gateway.py
  ```

**Problemas de configuración**

- _Síntoma_: Errores relacionados con la configuración
- _Solución_: Verifique que el archivo `gateway_config.json` exista y tenga el formato correcto. Puede usar el asistente de configuración:
  ```bash
  python config_wizard.py
  ```

**Puerto ocupado**

- _Síntoma_: Error "Address already in use"
- _Solución_: Cambie el puerto en la configuración o detenga el proceso que está usando el puerto:

  ```bash
  # En Linux/Mac, para encontrar el proceso:
  lsof -i :8080

  # En Windows, para encontrar el proceso:
  netstat -ano | findstr :8080
  ```

### 2. Problemas de conexión con PLCs

#### Síntomas

- Los PLCs aparecen como desconectados
- Errores de comunicación con PLCs
- No se pueden enviar comandos a los PLCs

#### Posibles causas y soluciones

**PLC apagado o desconectado**

- _Síntoma_: Mensajes de "Connection refused" o "timeout"
- _Solución_: Verifique que el PLC esté encendido y conectado a la red

**Dirección IP incorrecta**

- _Síntoma_: Mensajes de "Connection refused" o "timeout"
- _Solución_: Verifique la dirección IP del PLC en la configuración

**Firewall bloqueando conexiones**

- _Síntoma_: Mensajes de "timeout"
- _Solución_: Verifique que el firewall permita conexiones salientes en el puerto del PLC (por defecto 3200)

**Problemas de red**

- _Síntoma_: Errores intermitentes de conexión
- _Solución_: Verifique la conectividad de red entre el gateway y los PLCs

### 3. Problemas de conexión con el WMS

#### Síntomas

- Errores de registro con el WMS
- Heartbeats no llegan al WMS
- Comandos del WMS no se reciben

#### Posibles causas y soluciones

**Token de autenticación incorrecto**

- _Síntoma_: Errores de autenticación
- _Solución_: Verifique que el token en la configuración sea correcto

**Problemas de conectividad**

- _Síntoma_: Timeouts o errores de conexión
- _Solución_: Verifique que tenga acceso a Internet y que el endpoint del WMS sea accesible

**Endpoint del WMS incorrecto**

- _Síntoma_: Errores de conexión
- _Solución_: Verifique que la URL del endpoint sea correcta

### 4. Problemas con la API REST

#### Síntomas

- Respuestas de error al acceder a la API
- La API no responde
- Respuestas lentas

#### Posibles causas y soluciones

**Gateway no iniciado en modo API**

- _Síntoma_: Conexión rechutada
- _Solución_: Inicie el gateway en modo API usando `start_gateway.bat` o `./start_gateway.sh`

**Puerto incorrecto**

- _Síntoma_: Conexión rechutada
- _Solución_: Verifique que esté usando el puerto correcto (por defecto 8080)

### 5. Problemas de rendimiento

#### Síntomas

- El gateway responde lentamente
- Altos uso de CPU o memoria
- Problemas intermitentes

#### Posibles causas y soluciones

**Demasiados PLCs configurados**

- _Síntoma_: Alto uso de CPU
- _Solución_: Verifique que solo tenga configurados los PLCs que realmente necesita

**Problemas de red**

- _Síntoma_: Tiempos de respuesta altos
- _Solución_: Verifique la calidad de la conexión de red

**Logs muy grandes**

- _Síntoma_: Alto uso de disco
- _Solución_: Configure correctamente el tamaño máximo de los archivos de log

## Verificación del sistema

### Comandos útiles

**Verificar versión de Python:**

```bash
python --version
```

**Verificar procesos en ejecución:**

```bash
# En Linux/Mac:
ps aux | grep gateway

# En Windows:
tasklist | findstr python
```

**Verificar puertos en uso:**

```bash
# En Linux/Mac:
netstat -tulpn | grep :8080

# En Windows:
netstat -ano | findstr :8080
```

**Verificar conectividad con PLC:**

```bash
# En Linux/Mac:
telnet IP_DEL_PLC 3200

# En Windows:
telnet IP_DEL_PLC 3200
```

**Verificar conectividad con WMS:**

```bash
curl -v https://wms.example.com/api/v1/gateways
```

## Logs y diagnóstico

### Niveles de log

Los logs se encuentran en el directorio `logs/` y contienen información valiosa para diagnosticar problemas:

- `gateway.log`: Log principal del gateway
- `gateway.log.1`, `gateway.log.2`, etc.: Archivos de respaldo

### Interpretación de mensajes de log

**INFO**: Información general sobre el funcionamiento del sistema
**WARNING**: Advertencias que no detienen el funcionamiento pero requieren atención
**ERROR**: Errores que pueden afectar el funcionamiento del sistema
**DEBUG**: Información detallada para diagnóstico (solo disponible si el nivel de log es DEBUG)

### Recopilación de información para soporte

Si necesita contactar con soporte, recopile la siguiente información:

1. Versión del gateway
2. Sistema operativo
3. Archivo de configuración (sin tokens de autenticación)
4. Últimos 100 líneas de los archivos de log
5. Descripción detallada del problema

## Contacto con soporte

Si después de seguir esta guía aún experimenta problemas, contacte con nuestro equipo de soporte técnico proporcionando:

1. Descripción detallada del problema
2. Pasos realizados para reproducir el problema
3. Información del sistema (SO, versión de Python, etc.)
4. Archivos de log relevantes
5. Archivo de configuración (sin datos sensibles)

Nuestro equipo de soporte está disponible en horario laboral y hará todo lo posible para ayudarle a resolver el problema.
