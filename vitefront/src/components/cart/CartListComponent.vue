<template>
    <div>
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead>
          <tr>
            <th>Producto</th>
            <th>Precio</th>
            <th>Cantidad</th>
            <th>Subtotal</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <CartItemComponent 
            v-for="item in cartItems" 
            :key="item.product_id" 
            :product="item"
            @updated="updateCartItem"
            @removed="removeItem"
          />
        </tbody>
      </table>
  
      <div class="mt-6 flex justify-between items-center">
        <h4 class="text-2xl font-bold text-gray-800 dark:text-white flex items-center">
            <span class="text-gray-500 dark:text-gray-300">Total:</span>
            <span class="ml-2 text-teal-600 dark:text-teal-400 bg-green-100 dark:bg-teal-800 px-3 py-1 rounded-lg shadow-md">
                {{ total }}
            </span>
        </h4>

        <a href="/payments/checkout/" class="bg-teal-500 hover:bg-teal-600 text-white font-bold py-3 px-6 rounded-lg">
          🛒 Proceder al Pago
        </a>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, defineProps } from "vue";
  import CartItemComponent from "./CartItemComponent.vue";


  const props = defineProps({
    cartItems: Array
  });
  
  // ✅ Hacer `cartItems` completamente reactivo
  const cartItems = ref([...props.cartItems]);
  
  // ✅ Función para actualizar la cantidad de un producto y forzar reactividad
  const updateCartItem = (updatedItem) => {
    const index = cartItems.value.findIndex(item => item.product_id === updatedItem.product_id);
    if (index !== -1) {
      cartItems.value[index].quantity = updatedItem.quantity;
    }
    
    cartItems.value = [...cartItems.value];  // 🔥 SOLUCIÓN: Forzar Vue a detectar cambios
  };
  
  // ✅ Función para eliminar un producto en tiempo real
  const removeItem = (productId) => {
    cartItems.value = cartItems.value.filter(item => item.product_id !== productId);
    cartItems.value = [...cartItems.value];  // 🔥 SOLUCIÓN: Forzar Vue a detectar cambios
  };
  
  // ✅ `total` ahora es `computed()` para que sea reactivo
  const total = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + (parseFloat(item.price.replace("€", "").replace(",", ".")) * item.quantity), 0).toFixed(2) + " €";
  });
  </script>
  