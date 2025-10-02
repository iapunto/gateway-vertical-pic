# Instalación del Gateway Local

## Requisitos del sistema

- **Sistema operativo**: Windows 7/8/10/11, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python**: Versión 3.7 o superior
- **Memoria RAM**: Mínimo 512 MB
- **Espacio en disco**: Mínimo 100 MB disponibles

## Pasos de instalación

### 1. Verificar requisitos

Antes de instalar, verifique que tiene Python 3.7 o superior instalado:

```bash
python --version
```

o

```bash
python3 --version
```

Si no tiene Python instalado, descárguelo desde [python.org](https://www.python.org/downloads/).

### 2. Descargar el Gateway

Descargue el archivo comprimido del Gateway Local o clone el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

### 3. Ejecutar el instalador

Navegue al directorio del proyecto y ejecute el script de instalación:

**En Windows:**

```cmd
python install_gateway.py
```

**En Linux/Mac:**

```bash
python3 install_gateway.py
```

El instalador realizará automáticamente las siguientes acciones:

- Creará un entorno virtual
- Instalará todas las dependencias necesarias
- Creará scripts de inicio convenientes
- Generará accesos directos en el escritorio (solo Windows)

### 4. Verificar la instalación

Una vez completada la instalación, debería ver los siguientes archivos creados:

- `gateway_venv/` - Entorno virtual con todas las dependencias
- Scripts de inicio específicos para su sistema operativo
- Accesos directos en el escritorio (solo Windows)

## Configuración

### 1. Ejecutar el asistente de configuración

Para configurar el gateway, ejecute el asistente de configuración:

**En Windows:**

```cmd
python config_wizard.py
```

**En Linux/Mac:**

```bash
python3 config_wizard.py
```

El asistente le guiará a través de la configuración de:

- Parámetros del gateway
- Conexión con el WMS
- Configuración de red
- Parámetros de logging
- Configuración de PLCs

### 2. Configuración manual (opcional)

También puede editar directamente el archivo `gateway_config.json` para configurar el gateway.

## Iniciar el Gateway

### Modo API (recomendado)

Para iniciar el gateway en modo API (con interfaz web):

**En Windows:**

- Ejecute el archivo `start_gateway.bat`
- O haga doble clic en el acceso directo del escritorio "Iniciar Gateway Local (API)"

**En Linux/Mac:**

```bash
./start_gateway.sh
```

### Modo Standalone

Para iniciar el gateway en modo standalone (sin interfaz web):

**En Windows:**

- Ejecute el archivo `start_gateway_standalone.bat`
- O haga doble clic en el acceso directo del escritorio "Iniciar Gateway Local (Standalone)"

**En Linux/Mac:**

```bash
./start_gateway_standalone.sh
```

## Verificación

Una vez iniciado el gateway, puede verificar su funcionamiento:

1. **Verifique los logs**: Los logs se encuentran en el directorio `logs/`
2. **Verifique la API**: Si inició en modo API, acceda a `http://localhost:8080/health`
3. **Verifique la conexión con PLCs**: Los logs mostrarán el estado de conexión con los PLCs

## Solución de problemas

Si encuentra problemas durante la instalación o ejecución, consulte el archivo [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para soluciones a problemas comunes.
