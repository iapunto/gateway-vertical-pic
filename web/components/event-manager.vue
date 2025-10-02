<template>
  <div class="event-manager">
    <div class="card">
      <div class="card-header">
        <h3>Eventos del Sistema</h3>
        <div class="card-actions">
          <button class="btn btn-outline" @click="refreshEvents">
            <i class="fas fa-sync-alt"></i> Actualizar
          </button>
        </div>
      </div>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Fecha/Hora</th>
              <th>Tipo</th>
              <th>Descripción</th>
              <th>Fuente</th>
              <th>Nivel</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="event in events" :key="event.id">
              <td>{{ event.timestamp }}</td>
              <td>{{ event.type }}</td>
              <td>{{ event.description }}</td>
              <td>{{ event.source }}</td>
              <td>
                <span class="badge" :class="event.level.toLowerCase()">
                  {{ event.level }}
                </span>
              </td>
            </tr>
            <tr v-if="events.length === 0">
              <td colspan="5" class="text-center">
                No hay eventos registrados
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EventManager",
  data() {
    return {
      events: [],
    };
  },
  mounted() {
    this.loadEvents();
  },
  methods: {
    async loadEvents() {
      try {
        // En una implementación real, esto haría una llamada a la API
        // const response = await fetch('/api/v1/events');
        // this.events = await response.json();

        // Simulación de datos
        this.events = [
          {
            id: 1,
            timestamp: "2023-05-15 10:30:25",
            type: "CONNECTION",
            description: "PLC-001 conectado",
            source: "PLC-001",
            level: "INFO",
          },
          {
            id: 2,
            timestamp: "2023-05-15 10:28:42",
            type: "COMMAND",
            description: "Comando MOVE ejecutado",
            source: "PLC-001",
            level: "INFO",
          },
          {
            id: 3,
            timestamp: "2023-05-15 10:25:15",
            type: "SCAN",
            description: "Escaneo de red completado",
            source: "SYSTEM",
            level: "INFO",
          },
          {
            id: 4,
            timestamp: "2023-05-15 10:20:30",
            type: "CONNECTION",
            description: "PLC-003 reconectado",
            source: "PLC-003",
            level: "WARNING",
          },
          {
            id: 5,
            timestamp: "2023-05-15 10:15:45",
            type: "ERROR",
            description: "Timeout en comando STOP",
            source: "PLC-003",
            level: "ERROR",
          },
        ];
      } catch (error) {
        console.error("Error cargando eventos:", error);
      }
    },
    refreshEvents() {
      this.loadEvents();
    },
  },
};
</script>

<style scoped>
.event-manager {
  padding: 20px;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.badge.info {
  background-color: #dbeafe;
  color: #1d4ed8;
}

.badge.warning {
  background-color: #fef3c7;
  color: #d97706;
}

.badge.error {
  background-color: #fee2e2;
  color: #dc2626;
}

.text-center {
  text-align: center;
}
</style>
