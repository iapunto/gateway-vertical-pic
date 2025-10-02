// Versión de depuración del frontend con más información de registro

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Función de depuración
function debugLog(message, data = null) {
  console.log(`[DEBUG ${new Date().toISOString()}] ${message}`, data ? data : '');
}

// Función mejorada para cargar datos de configuración
async function loadConfigData() {
  debugLog("Iniciando loadConfigData");
  
  try {
    // Verificar que los elementos del DOM existan
    debugLog("Verificando elementos del DOM");
    const elements = [
      "bind-address",
      "bind-port", 
      "plc-port",
      "scan-interval",
      "log-level",
      "wms-endpoint"
    ];
    
    const foundElements = {};
    elements.forEach(id => {
      const element = document.getElementById(id);
      foundElements[id] = !!element;
      if (element) {
        debugLog(`Elemento encontrado: ${id}`, element.tagName);
      } else {
        debugLog(`Elemento NO encontrado: ${id}`);
      }
    });
    
    // Obtener configuraciones desde la API
    debugLog("Obteniendo configuraciones desde la API", `${API_BASE_URL}/config`);
    const response = await fetch(`${API_BASE_URL}/config`);
    debugLog("Respuesta de la API recibida", {
      status: response.status,
      ok: response.ok
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const configs = await response.json();
    debugLog("Configuraciones obtenidas de la API", configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs && Object.keys(configs).length > 0) {
      debugLog("Configuraciones encontradas, estableciendo valores");
      
      const configMap = {
        "bind-address": "bind_address",
        "bind-port": "bind_port",
        "plc-port": "plc_port",
        "scan-interval": "scan_interval",
        "log-level": "log_level",
        "wms-endpoint": "wms_endpoint"
      };
      
      for (const [elementId, configKey] of Object.entries(configMap)) {
        const element = document.getElementById(elementId);
        if (element) {
          const value = configs[configKey];
          if (value !== undefined) {
            element.value = value;
            debugLog(`Valor establecido para ${elementId}`, value);
          } else {
            debugLog(`Valor no encontrado para ${configKey}`);
          }
        } else {
          debugLog(`Elemento no encontrado: ${elementId}`);
        }
      }
    } else {
      debugLog("No se encontraron configuraciones o están vacías");
    }
  } catch (error) {
    debugLog("Error cargando configuración", error.message);
    console.error("Error cargando configuración:", error);
    showNotification("Error cargando configuración", "error");
  }
}

// Función para probar manualmente la carga de configuración
function testLoadConfig() {
  debugLog("Iniciando prueba manual de loadConfigData");
  loadConfigData();
}

// Exponer la función para pruebas manuales
window.testLoadConfig = testLoadConfig;

// Función para mostrar notificaciones con depuración
function showNotification(message, type = "info") {
  debugLog("Mostrando notificación", { message, type });
  // Implementación original de showNotification
  const container = document.getElementById("notifications-container");
  if (container) {
    const notification = document.createElement("div");
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${
          type === "success"
            ? "check-circle"
            : type === "error"
            ? "exclamation-circle"
            : type === "warning"
            ? "exclamation-triangle"
            : "info-circle"
        }"></i>
        ${message}
    `;

    container.appendChild(notification);

    // Remover después de 3 segundos
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 3000);
  }
}

// Función loadView con depuración
function loadView(viewName) {
  debugLog("Cargando vista", viewName);
  
  // Ocultar todas las vistas
  const views = document.querySelectorAll('[id$="-view"]');
  views.forEach((view) => {
    view.classList.add("hidden");
  });

  // Mostrar la vista solicitada
  const targetView = document.getElementById(viewName + "-view");
  if (targetView) {
    debugLog("Vista encontrada, mostrando", viewName);
    targetView.classList.remove("hidden");

    // Cargar datos específicos de la vista
    switch (viewName) {
      case "config":
        debugLog("Llamando a loadConfigData para la vista de configuración");
        loadConfigData();
        break;
    }
  } else {
    debugLog("Vista no encontrada", viewName);
  }
}

debugLog("Script de depuración cargado completamente");

// Verificar si el DOM está listo
if (document.readyState === 'loading') {
  debugLog("DOM aún cargando, esperando DOMContentLoaded");
  document.addEventListener('DOMContentLoaded', function() {
    debugLog("DOMContentLoaded disparado");
  });
} else {
  debugLog("DOM ya cargado");
}