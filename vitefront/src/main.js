import { createApp } from "vue";
import App from "./App.vue"; // El componente de Vue para los toasts
import AOS from "aos";
import "aos/dist/aos.css";
import "./style.css";
import ToastAddCarroComponent from "./components/ToastAddCarroComponent.vue";
import CartListComponent from "./components/cart/CartListComponent.vue";

// Inicializar AOS (fuera de Vue)
AOS.init({
  duration: 1000,
  once: true,
});

// Verificar si existe el contenedor de Vue antes de montarlo
document.addEventListener("DOMContentLoaded", () => {

  const toastContainer = document.getElementById("vue-toast");
  const cartButtons = document.querySelectorAll(".vue-add-to-cart");

  if (toastContainer) {
    console.log("✅ `vue-toast` encontrado, montando Vue...");
    const app = createApp(App);
    app.mount("#vue-toast");
  } else {
    console.warn("⚠️ `vue-toast` no encontrado en `base.html`.");
  }
    // Montar cada botón "Añadir al carrito" con Vue
    cartButtons.forEach((element) => {
      const productId = element.dataset.productId;
      const quantity = element.dataset.quantity;
      const cartApp = createApp(ToastAddCarroComponent, { productId, quantity });
      cartApp.mount(element);
    });


    // Verificar si existe el contenedor de Vue antes de montarlo
    const cartApp = document.getElementById("cart-app");
    if (cartApp) {
      console.log("✅ `cart-app` encontrado, montando Vue...");
      console.log(document.getElementById("cart-app"));

      const cartData = JSON.parse(cartApp.dataset.cartItems || "[]"); // ✅ Convertimos `cartData` a JSON
      
      const app = createApp(CartListComponent, { cartItems: cartData });  // ✅ Pasamos `cartItems` como prop
      app.mount("#cart-app");
    } else {
      console.warn("⚠️ `cart-app` no encontrado en `base.html`.");
    }


});