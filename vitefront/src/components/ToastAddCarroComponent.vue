<template>
    <button
      @click="addToCart"
      class="flex items-center justify-center gap-2 bg-gradient-to-r 
             from-teal-500 to-teal-600 hover:from-teal-600 hover:to-teal-700
             text-white font-bold px-6 py-3 rounded-lg shadow-lg transition 
             transform active:scale-95 focus:outline-none focus:ring-2 
             focus:ring-offset-2 focus:ring-teal-500"
      aria-label="Añadir al carrito"
    >
      <!-- Icono de carrito -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="2"
        stroke="currentColor"
        class="w-6 h-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-1 2m11-2l1 2m-5 0v2m0 0h2m-2 0H9m10-12h2"
        />
      </svg>
      
      <span>Añadir al carrito</span>
    </button>
  </template>
  
  
  <script setup>
  import { defineProps } from "vue";
  import { toast } from "vue-sonner";
  
  const props = defineProps({
    productId: String, // Recibe el ID del producto desde Django
  });
  
  const addToCart = async () => {
    try {
      const formData = new FormData();
      formData.append("product_id", props.productId);
  
      const response = await fetch("cart/add-to-cart/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      });
  
      const data = await response.json();
  
      if (data.status === "success") {
        toast.success(`✅ ${data.message}`);
      } else {
        toast.error(`❌ ${data.message}`);
      }
    } catch (error) {
      console.error("Error al añadir al carrito:", error);
      toast.error("❌ Hubo un problema con la solicitud.");
    }
  };
  
  // Función para obtener el CSRF token de Django

const getCSRFToken = () => {
  const csrfCookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
  return csrfCookie || "";
};
  </script>