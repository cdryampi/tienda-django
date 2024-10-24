from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Cart, CartItem

class CartAdmin(GuardedModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'id')
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        # Si el carrito no tiene usuario asignado, permite que el superusuario lo cambie
        return obj.user == request.user or request.user.is_superuser or obj.user is None

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request, obj)
        # Si el carrito no tiene usuario asignado, permite que el superusuario lo elimine
        return obj.user == request.user or request.user.is_superuser or obj.user is None


# Admin para CartItem
class CartItemAdmin(GuardedModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'price')
    search_fields = ('product__titulo', 'cart__id')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Solo superusuarios ven todos los items
        if request.user.is_superuser:
            return qs
        # Limitar la vista a los items del carrito del usuario logueado
        return qs.filter(cart__user=request.user)

    def has_change_permission(self, request, obj=None):
        has_perm = super().has_change_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None:
            # Los usuarios solo pueden cambiar los items de su propio carrito
            return obj.cart.user == request.user or request.user.is_superuser
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            # Solo el propietario o superusuario puede eliminar los items
            return obj.cart.user == request.user or request.user.is_superuser
        return super().has_delete_permission(request, obj)

# Registrar en el admin
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)