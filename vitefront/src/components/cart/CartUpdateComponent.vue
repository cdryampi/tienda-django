<template>
  <div class="flex items-center space-x-2">
    <button
      @click="updateQuantity(-1)"
      class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded"
    >
      −
    </button>
    <span class="px-4 py-2 border border-gray-300 rounded-md">{{
      quantity
    }}</span>
    <button
      @click="updateQuantity(1)"
      class="bg-teal-500 hover:bg-teal-600 text-white px-2 py-1 rounded"
    >
      +
    </button>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { toast } from "vue-sonner";

const props = defineProps({
  productId: Number,
  initialQuantity: Number,
});

const quantity = ref(props.initialQuantity);
const emit = defineEmits(["updated", "removed"]);

const updateQuantity = async (change) => {
  try {
    const newQuantity = quantity.value + change; // ✅ Ahora usamos `quantity.value`

    const response = await fetch("/es/cart/add-to-cart/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({
        product_id: props.productId,
        change: change,
        action: newQuantity <= 0 ? "remove_from_cart" : "update_quantity",
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      if (data.removed) {
        emit("removed", props.productId);
        toast.success("Producto eliminado del carrito");
      } else {
        quantity.value = Number(data.cart_item.quantity);
        toast.success(
          `producto ${data.cart_item.title} actualizado a ${quantity.value}`
        );
        emit("updated", quantity.value); // ✅ Emitimos la cantidad actualizada
      }
    }
  } catch (error) {
    console.error("❌ Error al actualizar cantidad:", error);
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
