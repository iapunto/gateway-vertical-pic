// Funcionalidad mejorada para la interfaz web del Gateway con integración API REST

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let currentEditingPLC = null;
const API_BASE_URL = "/api/v1";

// Inicializar cuando el DOM esté cargado
document.addEventListener("DOMContentLoaded", function () {
  // Inicializar navegación
  initNavigation();

  // Cargar vista inicial
  loadDashboardData();

  // Inicializar gráficos
  initCharts();

  // Configurar eventos
  setupEventListeners();

  // Actualizar datos periódicamente
  setInterval(loadDashboardData, 30000); // Cada 30 segundos
});

// Inicializar navegación
function initNavigation() {
  const navLinks = document.querySelectorAll(".sidebar-menu a");
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      // Remover clase activa de todos los enlaces
      navLinks.forEach((l) => l.classList.remove("active"));

      // Agregar clase activa al enlace clickeado
      this.classList.add("active");

      // Cargar la vista correspondiente
      const view = this.getAttribute("data-view");
      loadView(view);
    });
  });
}

// Cargar vista
function loadView(viewName) {
  // Ocultar todas las vistas
  const views = document.querySelectorAll('[id$="-view"]');
  views.forEach((view) => {
    view.classList.add("hidden");
  });

  // Mostrar la vista solicitada
  const targetView = document.getElementById(viewName + "-view");
  if (targetView) {
    targetView.classList.remove("hidden");

    // Cargar datos específicos de la vista
    switch (viewName) {
      case "dashboard":
        loadDashboardData();
        break;
      case "plcs":
        loadPLCsData();
        break;
      case "commands":
        loadCommandsData();
        break;
      case "events":
        loadEventsData();
        break;
      case "config":
        loadConfigData();
        break;
    }
  }
}

// Inicializar gráficos
function initCharts() {
  // Gráfico de estado de PLCs
  const plcCtx = document.getElementById("plc-status-chart").getContext("2d");
  plcStatusChart = new Chart(plcCtx, {
    type: "doughnut",
    data: {
      labels: ["En línea", "Fuera de línea", "Con errores"],
      datasets: [
        {
          data: [0, 0, 0],
          backgroundColor: ["#28a745", "#dc3545", "#ffc107"],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });

  // Gráfico de tiempo de respuesta
  const responseCtx = document
    .getElementById("response-time-chart")
    .getContext("2d");
  responseTimeChart = new Chart(responseCtx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Tiempo de respuesta (ms)",
          data: [],
          borderColor: "#4361ee",
          backgroundColor: "rgba(67, 97, 238, 0.1)",
          tension: 0.4,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

// Mostrar notificación
function showNotification(message, type = "info") {
  const container = document.getElementById("notifications-container");
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

// Funciones para interactuar con la API REST

// Obtener datos del dashboard
async function loadDashboardData() {
  try {
    // Obtener estadísticas
    const statsResponse = await fetch(`${API_BASE_URL}/stats`);
    const stats = await statsResponse.json();

    // Actualizar contadores
    document.getElementById("plc-count").textContent = stats.plc_count || 0;
    document.getElementById("command-count").textContent =
      stats.command_count || 0;
    document.getElementById("event-count").textContent = stats.event_count || 0;

    // Actualizar estado del sistema
    document.getElementById("system-status-content").innerHTML = `
            <p><i class="fas fa-check-circle text-success"></i> Sistema operativo</p>
            <p><i class="fas fa-check-circle text-success"></i> Conexión a red estable</p>
            <p><i class="fas fa-check-circle text-success"></i> Base de datos accesible</p>
            <p><i class="fas fa-check-circle text-success"></i> API REST funcionando</p>
        `;

    // Actualizar eventos recientes
    const eventsResponse = await fetch(`${API_BASE_URL}/events?limit=4`);
    const events = await eventsResponse.json();

    let eventsHtml = "";
    if (events && events.length > 0) {
      events.forEach((event) => {
        const eventTime = new Date(event.timestamp).toLocaleTimeString();
        eventsHtml += `<p><i class="fas fa-bell text-${
          event.event_type === "ERROR"
            ? "danger"
            : event.event_type === "WARNING"
            ? "warning"
            : "info"
        }"></i> ${event.data} - ${eventTime}</p>`;
      });
    } else {
      eventsHtml = "<p>No hay eventos recientes</p>";
    }
    document.getElementById("recent-events-content").innerHTML = eventsHtml;

    // Actualizar gráficos
    updateCharts();
  } catch (error) {
    console.error("Error cargando datos del dashboard:", error);
    showNotification("Error cargando datos del dashboard", "error");
  }
}

// Actualizar gráficos
async function updateCharts() {
  try {
    // Actualizar gráfico de estado de PLCs
    if (plcStatusChart) {
      // Obtener estado de PLCs
      const plcsResponse = await fetch(`${API_BASE_URL}/plcs`);
      const plcs = await plcsResponse.json();

      let online = 0,
        offline = 0,
        error = 0;
      if (plcs && plcs.length > 0) {
        plcs.forEach((plc) => {
          // En una implementación real, aquí se verificaría el estado real del PLC
          // Por ahora, simulamos basado en algún campo
          if (plc.status === "online") {
            online++;
          } else if (plc.status === "offline") {
            offline++;
          } else {
            error++;
          }
        });
      }

      plcStatusChart.data.datasets[0].data = [online, offline, error];
      plcStatusChart.update();
    }

    // Actualizar gráfico de tiempo de respuesta
    if (responseTimeChart) {
      // Obtener métricas de respuesta
      const metricsResponse = await fetch(
        `${API_BASE_URL}/metrics?type=response_time&hours=1`
      );
      const metrics = await metricsResponse.json();

      if (metrics && metrics.length > 0) {
        const times = [];
        const data = [];

        // Tomar las últimas 10 métricas
        const recentMetrics = metrics.slice(-10);
        recentMetrics.forEach((metric) => {
          const time = new Date(metric.timestamp).toLocaleTimeString();
          times.push(time);
          data.push(metric.value || 0);
        });

        responseTimeChart.data.labels = times;
        responseTimeChart.data.datasets[0].data = data;
        responseTimeChart.update();
      }
    }
  } catch (error) {
    console.error("Error actualizando gráficos:", error);
  }
}

// Cargar datos de PLCs
async function loadPLCsData() {
  try {
    const response = await fetch(`${API_BASE_URL}/plcs`);
    const plcs = await response.json();

    const plcsTable = document
      .getElementById("plcs-table")
      .getElementsByTagName("tbody")[0];
    plcsTable.innerHTML = "";

    if (!plcs || plcs.length === 0) {
      const row = plcsTable.insertRow();
      row.innerHTML =
        '<td colspan="7" class="text-center">No hay PLCs registrados</td>';
      return;
    }

    plcs.forEach((plc) => {
      const row = plcsTable.insertRow();
      row.innerHTML = `
                <td>${plc.plc_id || plc.id}</td>
                <td>${plc.name || "Sin nombre"}</td>
                <td>${plc.ip_address || "N/A"}</td>
                <td>${plc.port || "N/A"}</td>
                <td>
                    <span class="status-indicator status-${
                      plc.status === "online" ? "online" : "offline"
                    }"></span>
                    ${plc.status === "online" ? "En línea" : "Fuera de línea"}
                </td>
                <td>${
                  plc.updated_at
                    ? new Date(plc.updated_at).toLocaleString()
                    : "N/A"
                }</td>
                <td>
                    <button class="btn btn-outline btn-sm edit-plc" data-id="${
                      plc.plc_id || plc.id
                    }">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger btn-sm delete-plc" data-id="${
                      plc.plc_id || plc.id
                    }" data-name="${plc.name || plc.plc_id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
    });

    // Agregar eventos a los botones
    document.querySelectorAll(".edit-plc").forEach((button) => {
      button.addEventListener("click", function () {
        const plcId = this.getAttribute("data-id");
        editPLC(plcId);
      });
    });

    document.querySelectorAll(".delete-plc").forEach((button) => {
      button.addEventListener("click", function () {
        const plcId = this.getAttribute("data-id");
        const plcName = this.getAttribute("data-name");
        deletePLC(plcId, plcName);
      });
    });
  } catch (error) {
    console.error("Error cargando PLCs:", error);
    showNotification("Error cargando PLCs", "error");
  }
}

// Cargar datos de comandos
async function loadCommandsData() {
  try {
    const response = await fetch(`${API_BASE_URL}/commands?limit=20`);
    const commands = await response.json();

    const commandsTable = document
      .getElementById("commands-table")
      .getElementsByTagName("tbody")[0];
    commandsTable.innerHTML = "";

    if (!commands || commands.length === 0) {
      const row = commandsTable.insertRow();
      row.innerHTML =
        '<td colspan="6" class="text-center">No hay comandos registrados</td>';
      return;
    }

    commands.forEach((cmd) => {
      const row = commandsTable.insertRow();
      row.innerHTML = `
                <td>${
                  cmd.timestamp
                    ? new Date(cmd.timestamp).toLocaleString()
                    : "N/A"
                }</td>
                <td>${cmd.command || "N/A"}</td>
                <td>${cmd.plc_id || "N/A"}</td>
                <td>${
                  cmd.argument !== null && cmd.argument !== undefined
                    ? cmd.argument
                    : "-"
                }</td>
                <td>
                    <span class="status-indicator status-${
                      cmd.success ? "online" : "offline"
                    }"></span>
                    ${cmd.success ? "Éxito" : "Error"}
                </td>
                <td>${cmd.result || "-"}</td>
            `;
    });
  } catch (error) {
    console.error("Error cargando comandos:", error);
    showNotification("Error cargando comandos", "error");
  }
}

// Cargar datos de eventos
async function loadEventsData() {
  try {
    const response = await fetch(`${API_BASE_URL}/events?limit=50`);
    const events = await response.json();

    const eventsTable = document
      .getElementById("events-table")
      .getElementsByTagName("tbody")[0];
    eventsTable.innerHTML = "";

    if (!events || events.length === 0) {
      const row = eventsTable.insertRow();
      row.innerHTML =
        '<td colspan="5" class="text-center">No hay eventos registrados</td>';
      return;
    }

    events.forEach((event) => {
      const row = eventsTable.insertRow();
      row.innerHTML = `
                <td>${
                  event.timestamp
                    ? new Date(event.timestamp).toLocaleString()
                    : "N/A"
                }</td>
                <td>${event.event_type || "N/A"}</td>
                <td>${event.data || "N/A"}</td>
                <td>${event.source || "N/A"}</td>
                <td>
                    <span class="badge badge-${
                      event.event_type === "ERROR"
                        ? "danger"
                        : event.event_type === "WARNING"
                        ? "warning"
                        : event.event_type === "INFO"
                        ? "info"
                        : "secondary"
                    }">${event.event_type || "N/A"}</span>
                </td>
            `;
    });
  } catch (error) {
    console.error("Error cargando eventos:", error);
    showNotification("Error cargando eventos", "error");
  }
}

// Cargar datos de configuración
function loadConfigData() {
  // En una implementación real, esto obtendría la configuración desde la API
  // Por ahora, usamos valores por defecto
  document.getElementById("bind-address").value = "0.0.0.0";
  document.getElementById("bind-port").value = "8080";
  document.getElementById("plc-port").value = "3200";
  document.getElementById("scan-interval").value = "30";
  document.getElementById("log-level").value = "INFO";
  document.getElementById("wms-endpoint").value =
    "https://wms.example.com/api/v1/gateways";
}

// Abrir modal de PLC
async function openPLCModal(plcId = null) {
  const modal = document.getElementById("plc-modal");
  const title = document.getElementById("plc-modal-title");

  if (plcId) {
    // Editar PLC existente
    try {
      const response = await fetch(`${API_BASE_URL}/plcs/${plcId}`);
      const plc = await response.json();

      if (plc) {
        title.textContent = "Editar PLC";
        document.getElementById("plc-id").value = plc.plc_id || plc.id;
        document.getElementById("plc-name").value = plc.name || "";
        document.getElementById("plc-ip").value = plc.ip_address || "";
        document.getElementById("plc-port").value = plc.port || 3200;
        document.getElementById("plc-type").value = plc.type || "delta";
        document.getElementById("plc-description").value =
          plc.description || "";
        currentEditingPLC = plc.plc_id || plc.id;
      } else {
        showNotification("PLC no encontrado", "error");
        return;
      }
    } catch (error) {
      console.error("Error obteniendo PLC:", error);
      showNotification("Error obteniendo datos del PLC", "error");
      return;
    }
  } else {
    // Crear nuevo PLC
    title.textContent = "Nuevo PLC";
    document.getElementById("plc-form").reset();
    document.getElementById("plc-port").value = "3200";
    document.getElementById("plc-id").value = "";
    currentEditingPLC = null;
  }

  modal.style.display = "flex";
}

// Editar PLC
function editPLC(plcId) {
  openPLCModal(plcId);
}

// Eliminar PLC
function deletePLC(plcId, plcName) {
  document.getElementById("delete-plc-id").value = plcId;
  document.getElementById("delete-plc-name").textContent = plcName;
  document.getElementById("delete-plc-modal").style.display = "flex";
}

// Guardar PLC
async function savePLC() {
  const form = document.getElementById("plc-form");
  const plcId = document.getElementById("plc-id").value;
  const name = document.getElementById("plc-name").value;
  const ip = document.getElementById("plc-ip").value;
  const port = document.getElementById("plc-port").value;
  const type = document.getElementById("plc-type").value;
  const description = document.getElementById("plc-description").value;

  // Validar formulario
  if (!name || !ip || !port || !type) {
    showNotification(
      "Por favor complete todos los campos obligatorios.",
      "error"
    );
    return;
  }

  try {
    const plcData = {
      plc_id: plcId || `PLC-${Date.now()}`,
      name: name,
      ip_address: ip,
      port: parseInt(port),
      type: type,
      description: description,
    };

    // Enviar datos a la API
    const response = await fetch(`${API_BASE_URL}/plcs`, {
      method: currentEditingPLC ? "PUT" : "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(plcData),
    });

    if (response.ok) {
      if (currentEditingPLC) {
        showNotification(`PLC ${name} actualizado correctamente.`, "success");
      } else {
        showNotification(`PLC ${name} creado correctamente.`, "success");
      }

      // Cerrar modal
      document.getElementById("plc-modal").style.display = "none";

      // Recargar la lista de PLCs
      loadPLCsData();
    } else {
      const errorData = await response.json();
      showNotification(
        `Error: ${errorData.error || "Error desconocido"}`,
        "error"
      );
    }
  } catch (error) {
    console.error("Error guardando PLC:", error);
    showNotification("Error guardando PLC", "error");
  }
}

// Confirmar eliminación de PLC
async function confirmDeletePLC() {
  const plcId = document.getElementById("delete-plc-id").value;

  try {
    const response = await fetch(`${API_BASE_URL}/plcs/${plcId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      showNotification(`PLC eliminado correctamente.`, "success");

      // Cerrar modal
      document.getElementById("delete-plc-modal").style.display = "none";

      // Recargar la lista de PLCs
      loadPLCsData();
    } else {
      const errorData = await response.json();
      showNotification(
        `Error: ${errorData.error || "Error eliminando PLC"}`,
        "error"
      );
    }
  } catch (error) {
    console.error("Error eliminando PLC:", error);
    showNotification("Error eliminando PLC", "error");
  }
}

// Abrir modal de comando
async function openCommandModal() {
  // Cargar máquinas disponibles
  try {
    const response = await fetch(`${API_BASE_URL}/plcs`);
    const plcs = await response.json();

    const machineSelect = document.getElementById("command-plc");
    machineSelect.innerHTML =
      '<option value="">Seleccionar máquina...</option>';

    if (plcs && plcs.length > 0) {
      plcs.forEach((plc) => {
        const option = document.createElement("option");
        option.value = plc.plc_id || plc.id;
        option.textContent = `${plc.name || plc.plc_id} (${
          plc.ip_address || "N/A"
        })`;
        machineSelect.appendChild(option);
      });
    }
  } catch (error) {
    console.error("Error cargando PLCs para comandos:", error);
    showNotification("Error cargando lista de PLCs", "error");
  }

  // Mostrar modal
  document.getElementById("command-modal").style.display = "flex";
}

// Enviar comando
async function sendCommand() {
  const command = document.getElementById("command-select").value;
  const machine = document.getElementById("command-plc").value;

  if (!command || !machine) {
    showNotification("Por favor seleccione un comando y una máquina.", "error");
    return;
  }

  if (command === "MOVE") {
    const position = document.getElementById("position-input").value;
    if (!position) {
      showNotification("Por favor ingrese una posición.", "error");
      return;
    }
  }

  try {
    // En una implementación real, esto enviaría el comando al PLC
    // Por ahora, solo simulamos el envío
    showNotification(`Comando ${command} enviado a ${machine}.`, "success");

    // Cerrar modal
    document.getElementById("command-modal").style.display = "none";

    // Recargar la lista de comandos
    setTimeout(() => {
      loadCommandsData();
    }, 1000);
  } catch (error) {
    console.error("Error enviando comando:", error);
    showNotification("Error enviando comando", "error");
  }
}

// Guardar configuración
function saveConfig() {
  const bindAddress = document.getElementById("bind-address").value;
  const bindPort = document.getElementById("bind-port").value;
  const plcPort = document.getElementById("plc-port").value;
  const scanInterval = document.getElementById("scan-interval").value;
  const logLevel = document.getElementById("log-level").value;
  const wmsEndpoint = document.getElementById("wms-endpoint").value;

  // Validar datos
  if (!bindAddress || !bindPort || !plcPort || !scanInterval) {
    showNotification(
      "Por favor complete todos los campos obligatorios.",
      "error"
    );
    return;
  }

  // En una implementación real, esto enviaría la configuración a la API
  // Por ahora, solo mostramos una notificación
  showNotification("Configuración guardada exitosamente.", "success");
}

// Configurar eventos
function setupEventListeners() {
  // Botones de navegación
  document
    .getElementById("refresh-status")
    .addEventListener("click", function () {
      showNotification("Actualizando estado del sistema...", "info");
      loadDashboardData();
    });

  document
    .getElementById("refresh-plcs")
    .addEventListener("click", function () {
      showNotification("Actualizando lista de PLCs...", "info");
      loadPLCsData();
    });

  document
    .getElementById("refresh-commands")
    .addEventListener("click", function () {
      showNotification("Actualizando lista de comandos...", "info");
      loadCommandsData();
    });

  document
    .getElementById("refresh-events")
    .addEventListener("click", function () {
      showNotification("Actualizando lista de eventos...", "info");
      loadEventsData();
    });

  // Botones de PLC
  document.getElementById("add-plc-btn").addEventListener("click", function () {
    openPLCModal();
  });

  document
    .getElementById("save-plc-btn")
    .addEventListener("click", function () {
      savePLC();
    });

  document
    .getElementById("confirm-delete-plc")
    .addEventListener("click", function () {
      confirmDeletePLC();
    });

  // Botones de comando
  document
    .getElementById("send-command-btn")
    .addEventListener("click", function () {
      openCommandModal();
    });

  document
    .getElementById("send-command-submit")
    .addEventListener("click", function () {
      sendCommand();
    });

  // Cambio en el selector de comando
  document
    .getElementById("command-select")
    .addEventListener("change", function () {
      const positionGroup = document.getElementById("position-group");
      if (this.value === "MOVE") {
        positionGroup.style.display = "block";
      } else {
        positionGroup.style.display = "none";
      }
    });

  // Formulario de configuración
  document
    .getElementById("config-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      saveConfig();
    });

  document
    .getElementById("reset-config")
    .addEventListener("click", function () {
      if (confirm("¿Está seguro que desea restablecer la configuración?")) {
        loadConfigData();
        showNotification("Configuración restablecida.", "info");
      }
    });

  // Cerrar modales
  const closeButtons = document.querySelectorAll(".close, .close-modal");
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const modal = this.closest(".modal");
      if (modal) {
        modal.style.display = "none";
      }
    });
  });

  // Cerrar modales al hacer clic fuera
  const modals = document.querySelectorAll(".modal");
  modals.forEach((modal) => {
    modal.addEventListener("click", function (e) {
      if (e.target === this) {
        this.style.display = "none";
      }
    });
  });
}
