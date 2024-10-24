from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from product.models import Product
from djmoney.models.fields import MoneyField
from django.db.models import Sum


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Usuario registrado al que pertenece este carrito. Puede ser nulo si es un carrito de sesión."
    )
    session_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Carrito de {self.user.username}"
        else:
            return f"Carrito de sesión {self.session_id}"

    @staticmethod
    def get_or_create_cart(request):
        # Intentar obtener el carrito de la sesión
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                # Devolver el carrito si existe
                return Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                pass

        # Intentar obtener el carrito del usuario autenticado
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            if created:
                request.session['cart_id'] = cart.id
            return cart

        return None
    
    def get_cart_items(self):
        # Si no hay una ForeignKey, usar una consulta personalizada para obtener los items.
        return CartItem.objects.filter(cart=self)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')

    def get_subtotal(self):
        # Asegúrate de no usar paréntesis como si `price` fuera una función
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.titulo}"
