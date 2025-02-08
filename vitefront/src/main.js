import { createApp } from "vue";
import App from "./App.vue"; // El componente de Vue para los toasts
import { Toaster, toast } from "vue-sonner";
import AOS from "aos";
import "aos/dist/aos.css";
import "./style.css";

// Inicializar AOS (fuera de Vue)
AOS.init({
  duration: 1000,
  once: true,
});

// Verificar si existe el contenedor de Vue antes de montarlo
document.addEventListener("DOMContentLoaded", () => {
  const toastContainer = document.getElementById("vue-toast");

  if (toastContainer) {
    console.log("✅ `vue-toast` encontrado, montando Vue...");
    const app = createApp(App);
    app.mount("#vue-toast");
  } else {
    console.warn("⚠️ `vue-toast` no encontrado en `base.html`.");
  }
});