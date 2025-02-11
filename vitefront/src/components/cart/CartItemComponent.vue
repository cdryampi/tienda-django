<template>
  <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
    <td class="px-6 py-4 flex items-center space-x-3">
      <img
        :src="product.image"
        :alt="product.title"
        class="w-12 h-12 object-cover rounded"
      />
      <span class="text-gray-900 dark:text-teal-500">{{ product.title }}</span>
    </td>

    <td class="px-6 py-4 font-medium text-gray-800 dark:text-gray-200">
      {{ product.price }}
    </td>

    <td class="px-6 py-4">
      <CartUpdateComponent
        :product-id="product.product_id"
        :initial-quantity="quantity"
        @updated="updateQuantity"
        @removed="emit('removed', product.product_id)"
      />
    </td>

    <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white">
      {{ subtotal }}
    </td>

    <td class="px-6 py-4">
      <button
        @click="removeItem"
        class="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded shadow-md"
      >
        ❌ Eliminar
      </button>
    </td>
  </tr>
</template>

<script setup>
import { ref, computed, defineEmits } from "vue";
import CartUpdateComponent from "./CartUpdateComponent.vue";
import { toast } from "vue-sonner";
const props = defineProps({
  product: Object,
});

const emit = defineEmits(["updated", "removed"]);

const quantity = ref(props.product.quantity);

// ✅ `subtotal` ahora es reactivo
const subtotal = computed(() => {
  return (
    (
      parseFloat(props.product.price.replace("€", "").replace(",", ".")) *
      quantity.value
    ).toFixed(2) + " €"
  );
});

// ✅ Emitir evento `@updated` correctamente
const updateQuantity = (newQuantity) => {
  quantity.value = newQuantity;
  emit("updated", {
    product_id: props.product.product_id,
    quantity: newQuantity,
  });
};

// ✅ Función para eliminar el producto
const removeItem = async () => {
  try {
    const response = await fetch("/cart/add-to-cart/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({
        product_id: props.product.product_id,
        quantity: 0,
        action: "remove_from_cart",
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      toast.success("Producto eliminado del carrito");
      emit("removed", props.product.product_id); // ✅ Notificar a `CartList.vue` que elimine el producto
    }
  } catch (error) {
    console.error("❌ Error al eliminar el producto:", error);
  }
};

// ✅ Obtener CSRF Token
const getCSRFToken = () => {
  return (
    document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1] || ""
  );
};
</script>
