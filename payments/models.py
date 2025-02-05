from django.db import models
from django.conf import settings
from cart.models import CartItem
from djmoney.models.fields import MoneyField

# Create your models here.

class Order(models.Model):
    """
    Modelo para las ordenes de compra con Stripe
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='EUR'
    )
    payment_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Orden {self.id} - {self.total_price} - {'Pagado' if self.is_paid else 'Pendiente'}"
    

class OrderItem(models.Model):
    """
    Modelo para los items de las ordenes de compra
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255) # Nombre del producto
    quantity = models.PositiveIntegerField(default=1)
    price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='EUR'
    )

    def __str__(self):
        return f"Item {self.quantity} - {self.product} - {self.price}"