<template>
    <Toaster />
  </template>
  
  <script setup>
  import { Toaster, toast } from "vue-sonner";
  import { onMounted } from "vue";
  // Función para mostrar un toast desde Django
  const showToast = (message, type = "success") => {
    if (type === "success") {
      toast.success(message);
    } else if (type === "error") {
      toast.error(message);
    } else if (type === "info") {
      toast(message);
    }else if (type === "warning") {
      toast.warning(message);
    }else{
      toast("No se reconoce el tipo de mensaje");
    }
  };
  
  // Exponer la función globalmente para que Django pueda llamarla
  onMounted(() => {
  window.showToast = showToast;
});
  </script>