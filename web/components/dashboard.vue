<template>
  <div class="dashboard">
    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">PLCs Conectados</div>
        <div class="stat-value">{{ stats.plcCount }}</div>
        <div class="stat-label">En línea</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Comandos Hoy</div>
        <div class="stat-value">{{ stats.commandCount }}</div>
        <div class="stat-label">Ejecutados</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Eventos Hoy</div>
        <div class="stat-value">{{ stats.eventCount }}</div>
        <div class="stat-label">Registrados</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Estado del Sistema</div>
        <div class="stat-value">
          <i class="fas fa-circle" :class="systemStatusClass"></i>
        </div>
        <div class="stat-label">{{ systemStatusText }}</div>
      </div>
    </div>

    <!-- Dashboard Grid -->
    <div class="dashboard-grid">
      <!-- System Status Card -->
      <div class="card">
        <div class="card-header">
          <h3>Estado del Sistema</h3>
          <div class="card-actions">
            <button class="btn btn-outline" @click="refreshStatus">
              <i class="fas fa-sync-alt"></i> Actualizar
            </button>
          </div>
        </div>
        <div class="card-body">
          <div
            class="system-status-item"
            v-for="check in systemStatus.checks"
            :key="check.name"
          >
            <i
              class="status-icon"
              :class="
                check.status === 'healthy'
                  ? 'fas fa-check-circle text-success'
                  : check.status === 'unhealthy'
                  ? 'fas fa-times-circle text-danger'
                  : 'fas fa-question-circle text-warning'
              "
            ></i>
            <span class="status-text">{{ check.message }}</span>
          </div>
        </div>
      </div>

      <!-- Recent Events Card -->
      <div class="card">
        <div class="card-header">
          <h3>Últimos Eventos</h3>
          <div class="card-actions">
            <button
              class="btn btn-outline"
              @click="$emit('navigate', 'events')"
            >
              <i class="fas fa-eye"></i> Ver Todos
            </button>
          </div>
        </div>
        <div class="card-body">
          <div
            class="recent-event"
            v-for="event in recentEvents"
            :key="event.id"
          >
            <i class="event-icon" :class="eventIconClass(event.level)"></i>
            <div class="event-content">
              <div class="event-description">{{ event.description }}</div>
              <div class="event-time">{{ event.timestamp }}</div>
            </div>
          </div>
          <div v-if="recentEvents.length === 0" class="no-events">
            No hay eventos recientes
          </div>
        </div>
      </div>

      <!-- PLC Status Chart -->
      <div class="card">
        <div class="card-header">
          <h3>Estado de PLCs</h3>
          <div class="card-actions">
            <button class="btn btn-outline" @click="$emit('navigate', 'plcs')">
              <i class="fas fa-eye"></i> Ver Todos
            </button>
          </div>
        </div>
        <div class="chart-container">
          <canvas ref="plcStatusChart"></canvas>
        </div>
      </div>

      <!-- Command Response Time Chart -->
      <div class="card">
        <div class="card-header">
          <h3>Tiempo de Respuesta</h3>
        </div>
        <div class="chart-container">
          <canvas ref="responseTimeChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "https://cdn.jsdelivr.net/npm/chart.js";

Chart.register(...registerables);

export default {
  name: "Dashboard",
  data() {
    return {
      stats: {
        plcCount: 0,
        commandCount: 0,
        eventCount: 0,
      },
      systemStatus: {
        status: "unknown",
        checks: [],
      },
      recentEvents: [],
      plcStatusChart: null,
      responseTimeChart: null,
    };
  },
  computed: {
    systemStatusClass() {
      switch (this.systemStatus.status) {
        case "healthy":
          return "text-success";
        case "unhealthy":
          return "text-danger";
        case "degraded":
          return "text-warning";
        default:
          return "text-gray";
      }
    },
    systemStatusText() {
      switch (this.systemStatus.status) {
        case "healthy":
          return "Operativo";
        case "unhealthy":
          return "Error";
        case "degraded":
          return "Degradado";
        default:
          return "Desconocido";
      }
    },
  },
  mounted() {
    this.loadDashboardData();
    this.initCharts();
  },
  methods: {
    eventIconClass(level) {
      switch (level.toLowerCase()) {
        case "info":
          return "fas fa-info-circle text-info";
        case "warning":
          return "fas fa-exclamation-circle text-warning";
        case "error":
          return "fas fa-exclamation-triangle text-danger";
        default:
          return "fas fa-bell text-gray";
      }
    },
    async loadDashboardData() {
      try {
        // En una implementación real, esto haría llamadas a la API
        // const statsResponse = await fetch('/api/v1/stats');
        // this.stats = await statsResponse.json();

        // const statusResponse = await fetch('/api/v1/health');
        // this.systemStatus = await statusResponse.json();

        // const eventsResponse = await fetch('/api/v1/events?limit=5');
        // this.recentEvents = await eventsResponse.json();

        // Simulación de datos
        this.stats = {
          plcCount: 5,
          commandCount: 24,
          eventCount: 8,
        };

        this.systemStatus = {
          status: "healthy",
          checks: [
            {
              name: "Gateway Status",
              status: "healthy",
              message: "Gateway is running",
            },
            {
              name: "PLC Connections",
              status: "healthy",
              message: "5/5 PLCs connected",
            },
            {
              name: "System Resources",
              status: "healthy",
              message: "CPU: 25%, Memory: 45%",
            },
          ],
        };

        this.recentEvents = [
          {
            id: 1,
            timestamp: "10:30 AM",
            description: "PLC-001 conectado",
            level: "INFO",
          },
          {
            id: 2,
            timestamp: "10:25 AM",
            description: "Comando MOVE ejecutado",
            level: "INFO",
          },
          {
            id: 3,
            timestamp: "10:20 AM",
            description: "Escaneo de red completado",
            level: "INFO",
          },
        ];

        this.updateCharts();
      } catch (error) {
        console.error("Error cargando datos del dashboard:", error);
      }
    },
    refreshStatus() {
      this.loadDashboardData();
    },
    initCharts() {
      // Inicializar gráficos cuando el canvas esté disponible
      this.$nextTick(() => {
        if (this.$refs.plcStatusChart) {
          this.plcStatusChart = new Chart(this.$refs.plcStatusChart, {
            type: "doughnut",
            data: {
              labels: ["En línea", "Fuera de línea", "Con errores"],
              datasets: [
                {
                  data: [0, 0, 0],
                  backgroundColor: ["#4ade80", "#ef4444", "#f59e0b"],
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

        if (this.$refs.responseTimeChart) {
          this.responseTimeChart = new Chart(this.$refs.responseTimeChart, {
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
      });
    },
    updateCharts() {
      // Actualizar gráfico de estado de PLCs
      if (this.plcStatusChart) {
        this.plcStatusChart.data.datasets[0].data = [4, 1, 0];
        this.plcStatusChart.update();
      }

      // Actualizar gráfico de tiempo de respuesta
      if (this.responseTimeChart) {
        const now = new Date();
        const times = [];
        const data = [];

        for (let i = 9; i >= 0; i--) {
          const time = new Date(now.getTime() - i * 60000);
          times.push(time.toTimeString().substring(0, 5));
          data.push(Math.floor(Math.random() * 100) + 50);
        }

        this.responseTimeChart.data.labels = times;
        this.responseTimeChart.data.datasets[0].data = data;
        this.responseTimeChart.update();
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  margin: 10px 0;
  color: #4361ee;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  font-size: 1.2rem;
  font-weight: 500;
  color: #212529;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.card-body {
  padding: 15px 0;
}

.system-status-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.status-icon {
  margin-right: 10px;
}

.status-text {
  flex: 1;
}

.recent-event {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.recent-event:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.event-icon {
  margin-right: 10px;
  margin-top: 3px;
}

.event-content {
  flex: 1;
}

.event-description {
  margin-bottom: 5px;
}

.event-time {
  font-size: 0.8rem;
  color: #6c757d;
}

.no-events {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 20px 0;
}

.chart-container {
  height: 300px;
  position: relative;
}

.text-success {
  color: #4ade80;
}

.text-danger {
  color: #ef4444;
}

.text-warning {
  color: #f59e0b;
}

.text-info {
  color: #3b82f6;
}

.text-gray {
  color: #6c757d;
}
</style>
