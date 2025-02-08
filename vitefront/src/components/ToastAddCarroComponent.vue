<template>
    <button
      @click="addToCart"
      class="bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 
             text-white font-bold px-6 py-2.5 rounded-lg shadow-md transition transform active:scale-95"
    >
      🛒 Añadir al carrito
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