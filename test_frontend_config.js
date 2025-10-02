// Script de prueba para verificar la función loadConfigData

// Simular la función fetch
global.fetch = async (url) => {
  if (url === "/api/v1/config") {
    return {
      json: async () => ({
        bind_address: "0.0.0.0",
        bind_port: "8080",
        log_level: "INFO",
        plc_port: "3200",
        scan_interval: "30",
        wms_endpoint: "https://wms.example.com/api/v1/gateways",
      }),
    };
  }
  return { json: async () => ({}) };
};

// Simular el DOM
global.document = {
  getElementById: (id) => ({
    value: "",
  }),
};

// Simular la función showNotification
global.showNotification = (message, type) => {
  console.log(`Notification (${type}): ${message}`);
};

// Importar la función loadConfigData desde script.js
const fs = require("fs");
const scriptContent = fs.readFileSync("./web/script.js", "utf8");

// Extraer la función loadConfigData del script
const functionStart = scriptContent.indexOf("async function loadConfigData()");
const functionEnd = scriptContent.indexOf("}\n\n", functionStart) + 2;
const loadConfigDataFunction = scriptContent.substring(
  functionStart,
  functionEnd
);

// Evaluar la función en el contexto global
eval(loadConfigDataFunction);

// Ejecutar la función de prueba
console.log("Ejecutando prueba de loadConfigData...");
loadConfigData()
  .then(() => {
    console.log("Prueba completada exitosamente");
  })
  .catch((error) => {
    console.error("Error en la prueba:", error);
  });
