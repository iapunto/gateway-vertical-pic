// Script para probar la carga de configuración en el frontend con más depuración

// Simular el entorno del navegador
const mockElements = {
  "bind-address": { value: "0.0.0.0" },
  "bind-port": { value: "8080" },
  "plc-port": { value: "3200" },
  "scan-interval": { value: "30" },
  "log-level": { value: "INFO" },
  "wms-endpoint": { value: "https://wms.example.com/api/v1/gateways" },
};

const mockDocument = {
  readyState: "complete",
  getElementById: function (id) {
    console.log(`getElementById: ${id}`);
    return mockElements[id] || null;
  },
};

// Simular fetch
async function mockFetch(url) {
  console.log(`fetch: ${url}`);
  if (url === "/api/v1/config") {
    return {
      ok: true,
      status: 200,
      json: async () => ({
        bind_address: "192.168.1.100",
        bind_port: "9090",
        log_level: "DEBUG",
        plc_port: "3300",
        scan_interval: "60",
        wms_endpoint: "https://test.wms.example.com/api/v1/gateways",
      }),
    };
  }
  return { ok: true, status: 200, json: async () => ({}) };
}

// Variables globales
const API_BASE_URL = "/api/v1";

// Función auxiliar
function showNotification(message, type = "info") {
  console.log(`[NOTIFICATION] ${type}: ${message}`);
}

// Función loadConfigData con depuración (versión del frontend)
async function loadConfigData() {
  console.log("Iniciando loadConfigData");
  try {
    // Obtener configuraciones desde la API
    console.log("Obteniendo configuraciones desde la API");
    const response = await mockFetch(`${API_BASE_URL}/config`);
    console.log("Respuesta de la API recibida", response.status);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const configs = await response.json();
    console.log("Configuraciones obtenidas", configs);

    // Establecer valores en el formulario si existen en la base de datos
    if (configs) {
      console.log("Configuraciones encontradas, estableciendo valores");

      // Verificar que los elementos existan antes de establecer valores
      const bindAddressElement = mockDocument.getElementById("bind-address");
      const bindPortElement = mockDocument.getElementById("bind-port");
      const plcPortElement = mockDocument.getElementById("plc-port");
      const scanIntervalElement = mockDocument.getElementById("scan-interval");
      const logLevelElement = mockDocument.getElementById("log-level");
      const wmsEndpointElement = mockDocument.getElementById("wms-endpoint");

      console.log("Elementos del DOM:", {
        bindAddress: !!bindAddressElement,
        bindPort: !!bindPortElement,
        plcPort: !!plcPortElement,
        scanInterval: !!scanIntervalElement,
        logLevel: !!logLevelElement,
        wmsEndpoint: !!wmsEndpointElement,
      });

      if (bindAddressElement) {
        bindAddressElement.value = configs["bind_address"] || "0.0.0.0";
        console.log(
          "Valor establecido para bind-address:",
          bindAddressElement.value
        );
      }

      if (bindPortElement) {
        bindPortElement.value = configs["bind_port"] || "8080";
        console.log("Valor establecido para bind-port:", bindPortElement.value);
      }

      if (plcPortElement) {
        plcPortElement.value = configs["plc_port"] || "3200";
        console.log("Valor establecido para plc-port:", plcPortElement.value);
      }

      if (scanIntervalElement) {
        scanIntervalElement.value = configs["scan_interval"] || "30";
        console.log(
          "Valor establecido para scan-interval:",
          scanIntervalElement.value
        );
      }

      if (logLevelElement) {
        logLevelElement.value = configs["log_level"] || "INFO";
        console.log("Valor establecido para log-level:", logLevelElement.value);
      }

      if (wmsEndpointElement) {
        wmsEndpointElement.value =
          configs["wms_endpoint"] || "https://wms.example.com/api/v1/gateways";
        console.log(
          "Valor establecido para wms-endpoint:",
          wmsEndpointElement.value
        );
      }
    } else {
      console.log("No se encontraron configuraciones");
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
    showNotification("Error cargando configuración", "error");
  }
}

// Verificar y cargar configuración si es necesario
function checkAndLoadConfig() {
  console.log("Verificando si es necesario cargar configuración");
  const bindAddressElement = mockDocument.getElementById("bind-address");

  // Si el elemento existe pero no tiene valor (o tiene el valor por defecto), cargar configuración
  if (
    bindAddressElement &&
    (!bindAddressElement.value || bindAddressElement.value === "0.0.0.0")
  ) {
    console.log(
      "Configuración no cargada o con valores por defecto, cargando desde API"
    );
    loadConfigData();
  } else {
    console.log("Configuración ya cargada o con valores personalizados");
  }
}

// Ejecutar la prueba
console.log("Valores iniciales:");
console.log("bind-address:", mockElements["bind-address"].value);
console.log("bind-port:", mockElements["bind-port"].value);

console.log("\nIniciando prueba de carga de configuración");
loadConfigData();

console.log("\nValores después de cargar configuración:");
console.log("bind-address:", mockElements["bind-address"].value);
console.log("bind-port:", mockElements["bind-port"].value);
