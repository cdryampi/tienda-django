"""
Este archivo contiene la configuración del panel de administración para el modelo `Producto`.
Utilizamos `TranslatableAdmin` de Django Parler para permitir la gestión multilingüe de ciertos campos del modelo.

El objetivo de este código es personalizar la forma en que el modelo `Producto` se gestiona desde el panel de administración de Django. Se establecen varios elementos clave:

1. **Campos a mostrar en la lista del admin**: 
   Definimos qué información se muestra en la tabla principal de productos en el panel de administración.

2. **Campos de búsqueda y filtros**:
   Permitimos buscar productos por ciertos campos y filtrar resultados por categorías o estados de stock.

3. **Relaciones**:
   Configuramos cómo se gestionan las relaciones con otros modelos, como `Hamburguesa`, `Alergia`, y cómo se manejan las imágenes y documentos adjuntos.

4. **Campos de metadatos**:
   Incluimos campos adicionales relacionados con la auditoría (quién creó o actualizó un producto) y campos de metadatos (SEO) que permiten optimizar el producto para los motores de búsqueda.

5. **Visualización de imágenes y documentos**:
   Se incluyen métodos para mostrar imágenes y enlaces a documentos directamente en el panel de administración.

6. **Slug automático**:
   Configuramos la generación automática de slugs basados en el título del producto.

Este archivo se ajustará para mejorar la usabilidad del panel de administración y garantizar que se gestione correctamente la estructura de productos, imágenes, y documentos asociados.
"""

# Importaciones necesarias
from django.contrib import admin  # Importamos el módulo de administración de Django
from parler.admin import TranslatableAdmin  # TranslatableAdmin permite gestionar campos traducibles
from .models import Product  # Importamos el modelo Producto
from core.models import BurgerType, Allergy  # Importamos los modelos relacionados (Hamburguesa y Alergia)
from core.admin.utils import METADATA_FIELDS, METABASE_FIELDS, AUDIT_FIELDS, SLUG  # Importamos utilidades del admin para metadatos y otros campos
from core.admin.base_img_mixin import filter_image_queryset  # Función personalizada para filtrar imágenes en función del modelo
from django.utils.html import format_html  # Para renderizar contenido HTML en la interfaz del admin
from django.utils.text import slugify  # Para generar automáticamente slugs basados en texto
from pricing.models import PriceProduct
# Aquí comienza la configuración específica del modelo Producto

class PrecioProductoInline(admin.TabularInline):
    """
    Inline para gestionar los precios del producto desde el admin de Producto.
    """
    model = PriceProduct
    extra = 1  # Permite agregar un precio adicional

@admin.register(Product)
class ProductoAdmin(TranslatableAdmin):
    list_display = ('titulo', 'categoria', 'en_stock', 'mostrar_documento')
    search_fields = ('translations__titulo', 'categoria__nombre', 'hamburguesa__nombre')
    list_filter = ('categoria', 'en_stock')

    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'categoria', 'en_stock', 'imagen', 'documento','hamburguesa', 'alergias')
        }),
        ('Metadatos (SEO)', {
            'fields': METADATA_FIELDS,
            'classes': ('collapse',),
        }),
        ('Auditoría', {
            'fields': AUDIT_FIELDS,
            'classes': ('collapse',),
        }),
        ('Información de Estado', {
            'fields': METABASE_FIELDS,
            'classes': ('collapse',),
        }),
    )
    
    inlines = [PrecioProductoInline]
    readonly_fields = METABASE_FIELDS + AUDIT_FIELDS + SLUG

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    # Filtrar imágenes en función del modelo y objeto
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        model_name = Product.__name__
        meta_id = None

        if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
            meta_id = request.resolver_match.kwargs['object_id']

        # Ajustar el queryset de imágenes si el campo es 'productos_imagenes'
        if db_field.name == 'productos_imagenes':
            kwargs['queryset'] = filter_image_queryset(model_name, meta_id)
            kwargs['empty_label'] = 'Sin imagen asociada'

        # Ajustar el queryset de documentos si el campo es 'documento'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Mostrar imagen en el listado del admin
    def mostrar_imagen(self, obj):
        if obj.productos_imagenes:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.productos_imagenes.file.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Imagen"

    # Mostrar documento en el listado del admin
    def mostrar_documento(self, obj):
        if obj.documento:
            return format_html('<a href="{}" target="_blank">Ver documento</a>', obj.documento.file.url)
        return "Sin documento"
    mostrar_documento.short_description = "Documento"

    # Método para generar el slug automáticamente y asignar campos de auditoría
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        if not obj.slug:
            obj.slug = slugify(obj.titulo)
        super().save_model(request, obj, form, change)
