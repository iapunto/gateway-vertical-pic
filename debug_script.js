// Versión de depuración de script.js con más información de registro

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Función de depuración mejorada
function debugLog(message, data = null) {
  console.log(`[DEBUG] ${message}`, data ? data : "");
}

// Cargar datos de configuración con depuración
async function loadConfigData() {
  debugLog("Iniciando loadConfigData");
  try {
    // Obtener configuraciones desde la API
    debugLog(
      "Obteniendo configuraciones desde la API",
      `${API_BASE_URL}/config`
    );
    const response = await fetch(`${API_BASE_URL}/config`);
    debugLog("Respuesta de la API recibida", response.status);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const configs = await response.json();
    debugLog("Configuraciones obtenidas", configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs) {
      debugLog("Configuraciones encontradas, estableciendo valores");

      // Verificar que los elementos existan
      const bindAddressElement = document.getElementById("bind-address");
      const bindPortElement = document.getElementById("bind-port");
      const plcPortElement = document.getElementById("plc-port");
      const scanIntervalElement = document.getElementById("scan-interval");
      const logLevelElement = document.getElementById("log-level");
      const wmsEndpointElement = document.getElementById("wms-endpoint");

      debugLog("Elementos del DOM encontrados", {
        bindAddress: !!bindAddressElement,
        bindPort: !!bindPortElement,
        plcPort: !!plcPortElement,
        scanInterval: !!scanIntervalElement,
        logLevel: !!logLevelElement,
        wmsEndpoint: !!wmsEndpointElement,
      });

      if (bindAddressElement) {
        bindAddressElement.value = configs["bind_address"] || "0.0.0.0";
        debugLog(
          "Valor establecido para bind-address",
          bindAddressElement.value
        );
      }

      if (bindPortElement) {
        bindPortElement.value = configs["bind_port"] || "8080";
        debugLog("Valor establecido para bind-port", bindPortElement.value);
      }

      if (plcPortElement) {
        plcPortElement.value = configs["plc_port"] || "3200";
        debugLog("Valor establecido para plc-port", plcPortElement.value);
      }

      if (scanIntervalElement) {
        scanIntervalElement.value = configs["scan_interval"] || "30";
        debugLog(
          "Valor establecido para scan-interval",
          scanIntervalElement.value
        );
      }

      if (logLevelElement) {
        logLevelElement.value = configs["log_level"] || "INFO";
        debugLog("Valor establecido para log-level", logLevelElement.value);
      }

      if (wmsEndpointElement) {
        wmsEndpointElement.value =
          configs["wms_endpoint"] || "https://wms.example.com/api/v1/gateways";
        debugLog(
          "Valor establecido para wms-endpoint",
          wmsEndpointElement.value
        );
      }
    } else {
      debugLog("No se encontraron configuraciones");
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
    debugLog("Error cargando configuración", error.message);
  }
}

// Función para probar la carga de configuración
function testLoadConfig() {
  debugLog("Iniciando prueba de carga de configuración");
  loadConfigData();
}

// Exportar la función para poder llamarla desde la consola del navegador
window.testLoadConfig = testLoadConfig;

debugLog("Script de depuración cargado");
