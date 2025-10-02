// Importar Vue desde CDN
import { createApp } from "https://cdn.jsdelivr.net/npm/vue@3/dist/vue.esm-browser.prod.js";

// Crear la aplicación Vue
const app = createApp({
  data() {
    return {
      currentView: "dashboard",
      notifications: [],
    };
  },
  methods: {
    navigate(view) {
      this.currentView = view;
    },
    showNotification(notification) {
      const id = Date.now();
      this.notifications.push({
        id,
        ...notification,
      });

      // Eliminar la notificación después de 3 segundos
      setTimeout(() => {
        this.notifications = this.notifications.filter((n) => n.id !== id);
      }, 3000);
    },
  },
  mounted() {
    // Cargar la vista inicial
    console.log("Aplicación Vue cargada");
  },
});

// Registrar los componentes globales
app.component("dashboard-view", {
  template: `<div>Cargando dashboard...</div>`,
  async mounted() {
    const { default: Dashboard } = await import("./components/dashboard.vue");
    const component = app.component("dashboard-component", Dashboard);
    this.$el.innerHTML =
      '<dashboard-component @navigate="navigate" @notification="showNotification"></dashboard-component>';
  },
  methods: {
    navigate(view) {
      this.$emit("navigate", view);
    },
    showNotification(notification) {
      this.$emit("notification", notification);
    },
  },
});

app.component("plcs-view", {
  template: `<div>Cargando gestión de PLCs...</div>`,
  async mounted() {
    const { default: PLCManager } = await import(
      "./components/plc-manager.vue"
    );
    app.component("plc-manager", PLCManager);
    this.$el.innerHTML =
      '<plc-manager @notification="showNotification"></plc-manager>';
  },
  methods: {
    showNotification(notification) {
      this.$emit("notification", notification);
    },
  },
});

app.component("commands-view", {
  template: `<div>Cargando gestión de comandos...</div>`,
  async mounted() {
    const { default: CommandManager } = await import(
      "./components/command-manager.vue"
    );
    app.component("command-manager", CommandManager);
    // Pasar la lista de PLCs simulada
    this.$el.innerHTML =
      '<command-manager :plcs="plcs" @notification="showNotification"></command-manager>';
  },
  data() {
    return {
      plcs: [
        { id: "PLC-001", name: "Carrusel Principal" },
        { id: "PLC-002", name: "Carrusel Secundario" },
      ],
    };
  },
  methods: {
    showNotification(notification) {
      this.$emit("notification", notification);
    },
  },
});

app.component("events-view", {
  template: `<div>Cargando eventos...</div>`,
  async mounted() {
    const { default: EventManager } = await import(
      "./components/event-manager.vue"
    );
    app.component("event-manager", EventManager);
    this.$el.innerHTML = "<event-manager></event-manager>";
  },
});

app.component("config-view", {
  template: `<div>Cargando configuración...</div>`,
  async mounted() {
    const { default: ConfigManager } = await import(
      "./components/config-manager.vue"
    );
    app.component("config-manager", ConfigManager);
    this.$el.innerHTML =
      '<config-manager @notification="showNotification"></config-manager>';
  },
  methods: {
    showNotification(notification) {
      this.$emit("notification", notification);
    },
  },
});

// Montar la aplicación
app.mount("#app");
