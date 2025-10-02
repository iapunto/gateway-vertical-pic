// Funcionalidad adicional para la interfaz web del Gateway

// Variables globales
let plcStatusChart = null;
let responseTimeChart = null;
let cpuChart = null;
let memoryChart = null;
let networkChart = null;
let diskChart = null;

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
    view.style.display = "none";
  });

  // Mostrar la vista solicitada
  const targetView = document.getElementById(viewName + "-view");
  if (targetView) {
    targetView.style.display = "block";

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
      case "monitoring":
        loadMonitoringData();
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

  // Gráfico de CPU
  const cpuCtx = document.getElementById("cpu-chart").getContext("2d");
  cpuChart = new Chart(cpuCtx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Uso de CPU (%)",
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
          max: 100,
        },
      },
    },
  });

  // Gráfico de memoria
  const memoryCtx = document.getElementById("memory-chart").getContext("2d");
  memoryChart = new Chart(memoryCtx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Uso de Memoria (%)",
          data: [],
          borderColor: "#4895ef",
          backgroundColor: "rgba(72, 149, 239, 0.1)",
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
          max: 100,
        },
      },
    },
  });

  // Gráfico de tráfico de red
  const networkCtx = document.getElementById("network-chart").getContext("2d");
  networkChart = new Chart(networkCtx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Entrada (KB/s)",
          data: [],
          borderColor: "#4cc9f0",
          backgroundColor: "rgba(76, 201, 240, 0.1)",
          tension: 0.4,
          fill: true,
        },
        {
          label: "Salida (KB/s)",
          data: [],
          borderColor: "#4895ef",
          backgroundColor: "rgba(72, 149, 239, 0.1)",
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

  // Gráfico de uso de disco
  const diskCtx = document.getElementById("disk-chart").getContext("2d");
  diskChart = new Chart(diskCtx, {
    type: "doughnut",
    data: {
      labels: ["Usado", "Libre"],
      datasets: [
        {
          data: [0, 0],
          backgroundColor: ["#4361ee", "#e9ecef"],
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
}

// Cargar datos del dashboard
function loadDashboardData() {
  // Simular datos para el dashboard
  document.getElementById("plc-count").textContent = "5";
  document.getElementById("command-count").textContent = "24";
  document.getElementById("event-count").textContent = "8";

  // Actualizar estado del sistema
  document.getElementById("system-status-content").innerHTML = `
        <p><i class="fas fa-check-circle text-success"></i> Sistema operativo</p>
        <p><i class="fas fa-check-circle text-success"></i> Conexión a red estable</p>
        <p><i class="fas fa-check-circle text-success"></i> Base de datos accesible</p>
        <p><i class="fas fa-check-circle text-success"></i> API REST funcionando</p>
    `;

  // Actualizar eventos recientes
  document.getElementById("recent-events-content").innerHTML = `
        <p><i class="fas fa-bell text-warning"></i> PLC-001 conectado - 10:30 AM</p>
        <p><i class="fas fa-bell text-success"></i> Comando MOVE ejecutado - 10:25 AM</p>
        <p><i class="fas fa-bell text-info"></i> Escaneo de red completado - 10:20 AM</p>
        <p><i class="fas fa-bell text-warning"></i> PLC-003 reconectado - 10:15 AM</p>
    `;

  // Actualizar gráficos
  if (plcStatusChart) {
    plcStatusChart.data.datasets[0].data = [4, 1, 0];
    plcStatusChart.update();
  }

  // Actualizar gráfico de tiempo de respuesta con datos simulados
  if (responseTimeChart) {
    const now = new Date();
    const times = [];
    const data = [];

    for (let i = 9; i >= 0; i--) {
      const time = new Date(now.getTime() - i * 60000);
      times.push(time.toTimeString().substring(0, 5));
      data.push(Math.floor(Math.random() * 100) + 50);
    }

    responseTimeChart.data.labels = times;
    responseTimeChart.data.datasets[0].data = data;
    responseTimeChart.update();
  }
}

// Cargar datos de PLCs
function loadPLCsData() {
  // Simular datos de PLCs
  const plcsTable = document
    .getElementById("plcs-table")
    .getElementsByTagName("tbody")[0];
  plcsTable.innerHTML = "";

  const plcs = [
    {
      id: "PLC-001",
      ip: "192.168.1.101",
      status: "online",
      lastSeen: "2023-05-15 10:30:25",
    },
    {
      id: "PLC-002",
      ip: "192.168.1.102",
      status: "online",
      lastSeen: "2023-05-15 10:28:42",
    },
    {
      id: "PLC-003",
      ip: "192.168.1.103",
      status: "offline",
      lastSeen: "2023-05-15 09:15:30",
    },
    {
      id: "PLC-004",
      ip: "192.168.1.104",
      status: "online",
      lastSeen: "2023-05-15 10:32:10",
    },
    {
      id: "PLC-005",
      ip: "192.168.1.105",
      status: "online",
      lastSeen: "2023-05-15 10:29:55",
    },
  ];

  plcs.forEach((plc) => {
    const row = plcsTable.insertRow();
    row.innerHTML = `
            <td>${plc.id}</td>
            <td>${plc.ip}</td>
            <td>
                <span class="status-indicator status-${
                  plc.status === "online" ? "online" : "offline"
                }"></span>
                ${plc.status === "online" ? "En línea" : "Fuera de línea"}
            </td>
            <td>${plc.lastSeen}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="openCommandModal('${
                  plc.id
                }')">
                    <i class="fas fa-terminal"></i> Comando
                </button>
            </td>
        `;
  });
}

// Cargar datos de comandos
function loadCommandsData() {
  // Simular datos de comandos
  const commandsTable = document
    .getElementById("commands-table")
    .getElementsByTagName("tbody")[0];
  commandsTable.innerHTML = "";

  const commands = [
    {
      time: "2023-05-15 10:30:25",
      command: "MOVE",
      machine: "PLC-001",
      status: "success",
      response: "OK",
    },
    {
      time: "2023-05-15 10:28:42",
      command: "STATUS",
      machine: "PLC-002",
      status: "success",
      response: "OK",
    },
    {
      time: "2023-05-15 10:25:15",
      command: "START",
      machine: "PLC-004",
      status: "success",
      response: "OK",
    },
    {
      time: "2023-05-15 10:20:30",
      command: "MOVE",
      machine: "PLC-001",
      status: "success",
      response: "OK",
    },
    {
      time: "2023-05-15 10:15:45",
      command: "STOP",
      machine: "PLC-003",
      status: "error",
      response: "TIMEOUT",
    },
  ];

  commands.forEach((cmd) => {
    const row = commandsTable.insertRow();
    row.innerHTML = `
            <td>${cmd.time}</td>
            <td>${cmd.command}</td>
            <td>${cmd.machine}</td>
            <td>
                <span class="status-indicator status-${
                  cmd.status === "success" ? "online" : "offline"
                }"></span>
                ${cmd.status === "success" ? "Éxito" : "Error"}
            </td>
            <td>${cmd.response}</td>
        `;
  });
}

// Cargar datos de eventos
function loadEventsData() {
  // Simular datos de eventos
  const eventsTable = document
    .getElementById("events-table")
    .getElementsByTagName("tbody")[0];
  eventsTable.innerHTML = "";

  const events = [
    {
      time: "2023-05-15 10:30:25",
      type: "CONNECTION",
      description: "PLC-001 conectado",
      machine: "PLC-001",
      level: "INFO",
    },
    {
      time: "2023-05-15 10:28:42",
      type: "COMMAND",
      description: "Comando MOVE ejecutado",
      machine: "PLC-001",
      level: "INFO",
    },
    {
      time: "2023-05-15 10:25:15",
      type: "SCAN",
      description: "Escaneo de red completado",
      machine: "SYSTEM",
      level: "INFO",
    },
    {
      time: "2023-05-15 10:20:30",
      type: "CONNECTION",
      description: "PLC-003 reconectado",
      machine: "PLC-003",
      level: "WARNING",
    },
    {
      time: "2023-05-15 10:15:45",
      type: "ERROR",
      description: "Timeout en comando STOP",
      machine: "PLC-003",
      level: "ERROR",
    },
  ];

  events.forEach((event) => {
    const row = eventsTable.insertRow();
    row.innerHTML = `
            <td>${event.time}</td>
            <td>${event.type}</td>
            <td>${event.description}</td>
            <td>${event.machine}</td>
            <td>
                <span class="badge badge-${event.level.toLowerCase()}">${
      event.level
    }</span>
            </td>
        `;
  });
}

// Cargar datos de monitoreo
function loadMonitoringData() {
  // Simular datos de monitoreo
  const now = new Date();
  const times = [];
  const cpuData = [];
  const memoryData = [];
  const networkInData = [];
  const networkOutData = [];

  for (let i = 9; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60000);
    times.push(time.toTimeString().substring(0, 5));
    cpuData.push(Math.floor(Math.random() * 30) + 20);
    memoryData.push(Math.floor(Math.random() * 20) + 40);
    networkInData.push(Math.floor(Math.random() * 100) + 50);
    networkOutData.push(Math.floor(Math.random() * 80) + 30);
  }

  if (cpuChart) {
    cpuChart.data.labels = times;
    cpuChart.data.datasets[0].data = cpuData;
    cpuChart.update();
  }

  if (memoryChart) {
    memoryChart.data.labels = times;
    memoryChart.data.datasets[0].data = memoryData;
    memoryChart.update();
  }

  if (networkChart) {
    networkChart.data.labels = times;
    networkChart.data.datasets[0].data = networkInData;
    networkChart.data.datasets[1].data = networkOutData;
    networkChart.update();
  }

  // Actualizar gráfico de disco
  if (diskChart) {
    diskChart.data.datasets[0].data = [65, 35]; // 65% usado, 35% libre
    diskChart.update();
  }
}

// Cargar datos de configuración
function loadConfigData() {
  // Simular carga de configuración
  document.getElementById("bind-address").value = "0.0.0.0";
  document.getElementById("bind-port").value = "8080";
  document.getElementById("scan-interval").value = "30";
  document.getElementById("log-level").value = "INFO";
}

// Configurar eventos
function setupEventListeners() {
  // Botón de escaneo de PLCs
  document.getElementById("scan-plcs").addEventListener("click", function () {
    showNotification("Escaneo de red iniciado...", "info");
    // Simular escaneo
    setTimeout(() => {
      showNotification(
        "Escaneo de red completado. Se encontraron 2 nuevos PLCs.",
        "success"
      );
      loadPLCsData();
    }, 2000);
  });

  // Botón de enviar comando
  document
    .getElementById("send-command-btn")
    .addEventListener("click", function () {
      openCommandModal();
    });

  // Botón de refrescar PLCs
  document
    .getElementById("refresh-plcs")
    .addEventListener("click", function () {
      showNotification("Actualizando lista de PLCs...", "info");
      loadPLCsData();
      setTimeout(() => {
        showNotification("Lista de PLCs actualizada.", "success");
      }, 500);
    });

  // Botón de refrescar comandos
  document
    .getElementById("refresh-commands")
    .addEventListener("click", function () {
      showNotification("Actualizando lista de comandos...", "info");
      loadCommandsData();
      setTimeout(() => {
        showNotification("Lista de comandos actualizada.", "success");
      }, 500);
    });

  // Botón de refrescar eventos
  document
    .getElementById("refresh-events")
    .addEventListener("click", function () {
      showNotification("Actualizando lista de eventos...", "info");
      loadEventsData();
      setTimeout(() => {
        showNotification("Lista de eventos actualizada.", "success");
      }, 500);
    });

  // Botón de refrescar estado
  document
    .getElementById("refresh-status")
    .addEventListener("click", function () {
      showNotification("Actualizando estado del sistema...", "info");
      loadDashboardData();
      setTimeout(() => {
        showNotification("Estado del sistema actualizado.", "success");
      }, 500);
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

  // Botón de enviar comando en modal
  document
    .getElementById("send-command-submit")
    .addEventListener("click", function () {
      sendCommand();
    });

  // Cerrar modal
  const closeButtons = document.querySelectorAll(".close, .close-modal");
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      document.getElementById("command-modal").style.display = "none";
    });
  });

  // Formulario de configuración
  document
    .getElementById("config-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      saveConfig();
    });
}

// Mostrar notificación
function showNotification(message, type) {
  // Crear elemento de notificación
  const notification = document.createElement("div");
  notification.className = `alert alert-${type}`;
  notification.innerHTML = `
        <i class="fas fa-${
          type === "success"
            ? "check-circle"
            : type === "error"
            ? "exclamation-circle"
            : "info-circle"
        }"></i>
        ${message}
    `;

  // Agregar al inicio del contenido principal
  const mainContent = document.querySelector(".main-content");
  mainContent.insertBefore(notification, mainContent.firstChild);

  // Remover después de 3 segundos
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

// Abrir modal de comando
function openCommandModal(machineId = null) {
  // Cargar máquinas disponibles
  const machineSelect = document.getElementById("machine-select");
  machineSelect.innerHTML = '<option value="">Seleccionar máquina...</option>';

  const machines = ["PLC-001", "PLC-002", "PLC-003", "PLC-004", "PLC-005"];
  machines.forEach((machine) => {
    const option = document.createElement("option");
    option.value = machine;
    option.textContent = machine;
    if (machineId && machineId === machine) {
      option.selected = true;
    }
    machineSelect.appendChild(option);
  });

  // Mostrar modal
  document.getElementById("command-modal").style.display = "flex";
}

// Enviar comando
function sendCommand() {
  const command = document.getElementById("command-select").value;
  const machine = document.getElementById("machine-select").value;

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

  showNotification(`Comando ${command} enviado a ${machine}.`, "success");
  document.getElementById("command-modal").style.display = "none";

  // Actualizar la tabla de comandos
  setTimeout(() => {
    loadCommandsData();
  }, 1000);
}

// Guardar configuración
function saveConfig() {
  const bindAddress = document.getElementById("bind-address").value;
  const bindPort = document.getElementById("bind-port").value;
  const scanInterval = document.getElementById("scan-interval").value;
  const logLevel = document.getElementById("log-level").value;

  // Validar datos
  if (!bindAddress || !bindPort || !scanInterval) {
    showNotification("Por favor complete todos los campos.", "error");
    return;
  }

  // Simular guardado
  showNotification("Configuración guardada exitosamente.", "success");

  // En una implementación real, aquí se enviaría la configuración al servidor
  console.log("Configuración guardada:", {
    bindAddress,
    bindPort,
    scanInterval,
    logLevel,
  });
}
