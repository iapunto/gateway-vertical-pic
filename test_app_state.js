// Script para verificar el estado actual de la aplicación

// Simular el entorno del navegador
const mockElements = {
  "bind-address": { value: "0.0.0.0" },
  "bind-port": { value: "8080" },
  "plc-port": { value: "3200" },
  "scan-interval": { value: "30" },
  "log-level": { value: "INFO" },
  "wms-endpoint": { value: "https://wms.example.com/api/v1/gateways" },
  "plcs-table": {
    getElementsByTagName: function (tagName) {
      if (tagName === "tbody") {
        return [
          {
            innerHTML: "",
            insertRow: function () {
              return {
                innerHTML: "",
              };
            },
          },
        ];
      }
      return [];
    },
  },
};

const mockDocument = {
  readyState: "complete",
  addEventListener: function (event, callback) {
    console.log(`addEventListener: ${event}`);
    if (event === "DOMContentLoaded") {
      console.log("Simulando DOMContentLoaded");
      setTimeout(callback, 100);
    }
  },
  getElementById: function (id) {
    console.log(`getElementById: ${id}`);
    return mockElements[id] || null;
  },
  querySelectorAll: function (selector) {
    console.log(`querySelectorAll: ${selector}`);
    return [];
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
  if (url === "/api/v1/plcs") {
    return {
      ok: true,
      status: 200,
      json: async () => [
        {
          created_at: "2025-10-02 19:07:46",
          description: "",
          id: 3,
          ip_address: "192.168.1.50",
          name: "Vertical PIC Principal",
          plc_id: "PLC-1759432066207",
          port: 3200,
          type: "delta",
          updated_at: "2025-10-02 19:07:46",
        },
      ],
    };
  }
  return { ok: true, status: 200, json: async () => ({}) };
}

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Función auxiliar
function showNotification(message, type = "info") {
  console.log(`[NOTIFICATION] ${type}: ${message}`);
}

// Funciones del frontend
async function loadConfigData() {
  console.log("Iniciando loadConfigData");
  try {
    const response = await mockFetch(`${API_BASE_URL}/config`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const configs = await response.json();
    console.log("Configuraciones obtenidas", configs);

    if (configs) {
      const bindAddressElement = mockDocument.getElementById("bind-address");
      const bindPortElement = mockDocument.getElementById("bind-port");
      const plcPortElement = mockDocument.getElementById("plc-port");
      const scanIntervalElement = mockDocument.getElementById("scan-interval");
      const logLevelElement = mockDocument.getElementById("log-level");
      const wmsEndpointElement = mockDocument.getElementById("wms-endpoint");

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
    }
  } catch (error) {
    console.error("Error cargando configuración:", error);
    showNotification("Error cargando configuración", "error");
  }
}

async function loadPLCsData() {
  console.log("Iniciando loadPLCsData");
  try {
    const response = await mockFetch(`${API_BASE_URL}/plcs`);
    const plcs = await response.json();
    console.log("PLCs obtenidos", plcs);
  } catch (error) {
    console.error("Error cargando PLCs:", error);
    showNotification("Error cargando PLCs", "error");
  }
}

function checkAndLoadConfig() {
  console.log("Verificando si es necesario cargar configuración");
  const bindAddressElement = mockDocument.getElementById("bind-address");

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

function loadView(viewName) {
  console.log("Cargando vista:", viewName);

  switch (viewName) {
    case "config":
      console.log("Cargando datos de configuración");
      checkAndLoadConfig();
      break;
    case "plcs":
      console.log("Cargando datos de PLCs");
      loadPLCsData();
      break;
  }
}

// Simular la inicialización de la aplicación
console.log("Simulando inicialización de la aplicación");

mockDocument.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded disparado");

  // Cargar configuración automáticamente al iniciar
  setTimeout(() => {
    console.log("Cargando configuración automáticamente al iniciar");
    loadConfigData();
  }, 1000);

  // Cargar PLCs automáticamente al iniciar
  setTimeout(() => {
    console.log("Cargando PLCs automáticamente al iniciar");
    loadPLCsData();
  }, 1500);
});

// Simular navegación a la vista de configuración
setTimeout(() => {
  console.log("\nSimulando navegación a la vista de configuración");
  loadView("config");
}, 2000);

// Simular navegación a la vista de PLCs
setTimeout(() => {
  console.log("\nSimulando navegación a la vista de PLCs");
  loadView("plcs");
}, 2500);

console.log("Valores iniciales:");
console.log("bind-address:", mockElements["bind-address"].value);
console.log("bind-port:", mockElements["bind-port"].value);
