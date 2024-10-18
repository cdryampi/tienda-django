from django.contrib import admin
from .models import PrecioProducto

@admin.register(PrecioProducto)
class PrecioProductoAdmin(admin.ModelAdmin):
    """
    Admin para gestionar los precios del producto en diferentes monedas.
    """
    list_display = ('producto', 'precio', 'precio_currency')
    search_fields = ('producto__translations__titulo', 'precio_currency')
    list_filter = ('precio_currency',)
    
    # Controla los campos que se mostrarán en el formulario del admin
    fieldsets = (
        (None, {
            'fields': ('producto', 'precio')
        }),
    )
