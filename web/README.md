# Interfaz Web del Gateway Local

Esta carpeta contiene la interfaz de usuario web para el Gateway Local que conecta los PLCs del Carousel Vertical PIC con los sistemas WMS/ERP.

## Estructura de Archivos

- `index.html` - Página principal de la interfaz web
- `styles.css` - Hoja de estilos CSS
- `script.js` - Funcionalidad JavaScript
- `assets/` - Carpeta para imágenes y otros recursos (se creará cuando se necesite)

## Características

### Dashboard

- Vista general del estado del sistema
- Estadísticas de PLCs conectados
- Gráficos de monitoreo en tiempo real
- Últimos eventos del sistema

### Gestión de PLCs

- Lista de PLCs descubiertos en la red
- Estado en tiempo real de cada PLC
- Escaneo automático de red para encontrar nuevos PLCs
- Envío de comandos a PLCs específicos

### Comandos

- Historial de comandos enviados
- Estado de ejecución de comandos
- Respuestas de los PLCs

### Eventos

- Registro de eventos del sistema
- Filtrado por tipo de evento
- Nivel de severidad de eventos

### Monitoreo

- Gráficos de uso de CPU y memoria
- Tráfico de red en tiempo real
- Uso de disco
- Tiempo de respuesta de comandos

### Configuración

- Configuración de red del gateway
- Parámetros de escaneo
- Nivel de logging
- Configuración de seguridad

## Tecnologías Utilizadas

- HTML5
- CSS3 (con Flexbox y Grid)
- JavaScript (ES6+)
- Chart.js para gráficos
- Font Awesome para íconos
- Google Fonts (Roboto)

## Cómo Usar

1. Iniciar el servidor del gateway:

   ```
   python src/main.py
   ```

2. Abrir un navegador web y acceder a:

   ```
   http://localhost:8080
   ```

3. La interfaz web estará disponible con todas las funcionalidades.

## Personalización

Para personalizar la interfaz:

1. Modificar `styles.css` para cambiar los estilos
2. Editar `script.js` para agregar nueva funcionalidad
3. Actualizar `index.html` para modificar la estructura de la interfaz

## Notas

- Esta interfaz es completamente responsiva y funciona en dispositivos móviles y de escritorio
- Todos los datos se actualizan en tiempo real mediante llamadas AJAX al servidor
- La interfaz utiliza íconos de Font Awesome y fuentes de Google Fonts
- Los gráficos son interactivos y se actualizan automáticamente
