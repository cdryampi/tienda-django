"""
Modelo `PrecioProducto` para gestionar los precios de los productos en diferentes monedas utilizando `MoneyField` de `django-money`.

1. **MoneyField**:
   - Utilizamos `MoneyField` para manejar tanto el valor decimal del precio como la moneda asociada.
   - `MoneyField` proporciona validaciones adicionales para el manejo de monedas, garantizando que el valor del precio y la moneda estén correctamente gestionados.
   - La moneda predeterminada es `EUR`, pero este campo puede manejar múltiples monedas (como `USD` y `GBP`).
   - Las validaciones de moneda y formato están integradas, haciendo que sea más fácil trabajar con precios en diferentes monedas sin campos adicionales.

2. **Relación con Producto**:
   - Cada precio está vinculado a un producto a través de una relación `ForeignKey`.
   - Esto permite que un producto tenga diferentes precios en distintas monedas.

3. **Meta (Restricciones únicas)**:
   - La restricción `unique_together` asegura que no haya dos entradas con la misma combinación de producto y moneda, evitando duplicados.
   - Se utiliza el campo implícito `precio_currency` del `MoneyField` para garantizar que la combinación de producto y moneda sea única.

4. **Flexibilidad y escalabilidad**:
   - Este modelo es escalable para manejar múltiples productos con precios en diversas monedas.
   - Puede ser fácilmente extendido si necesitas agregar lógica adicional para el manejo de conversiones o promociones específicas.

"""

from django.db import models
from djmoney.models.fields import MoneyField  # Importamos MoneyField de django-money

class PriceProduct(models.Model):
    """
    Modelo para manejar precios de productos en diferentes monedas usando MoneyField de django-money.
    """
    
    # Relación con el modelo Producto desde la app product
    producto = models.ForeignKey(
        'product.Product',  # Apuntamos al modelo Producto de la app 'product'
        on_delete=models.CASCADE,
        related_name='precios'
    )
    
    # Campo para el precio y la moneda utilizando MoneyField
    precio = MoneyField(
        max_digits=10,  # Máximo de 10 dígitos (incluyendo decimales)
        decimal_places=2,  # 2 posiciones decimales para el precio
        default_currency='EUR',  # Establecemos EUR como moneda predeterminada
        help_text="Precio del producto con soporte de moneda"
    )

    class Meta:
        # Asegura que no haya duplicados de moneda para el mismo producto
        unique_together = ('producto', 'precio_currency')  # Controlamos moneda usando la relación implícita del MoneyField

    def __str__(self):
        return f"{self.producto} - {self.precio}"