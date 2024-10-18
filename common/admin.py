"""
Este archivo contiene la configuración del panel de administración para los modelos `Categoria` y `Tag`.
La gestión de estos modelos incluye:

1. **Campos a mostrar en la lista del admin**:
   - Definimos qué información se muestra en la tabla principal de categorías y etiquetas.
   - Incluye los campos `nombre`, `color`, y la visualización de la imagen asociada.

2. **Campos de búsqueda y filtros**:
   - Permitimos buscar categorías y etiquetas por el nombre, y filtrar resultados por el color o si tienen imágenes asociadas.

3. **Relaciones**:
   - Se gestionan las relaciones con el modelo `MediaFile`, lo que permite añadir imágenes a las categorías y etiquetas.

4. **Visualización de imágenes**:
   - Se incluyen métodos para mostrar las imágenes directamente en el panel de administración.

Este archivo mejora la usabilidad del panel de administración para gestionar categorías y etiquetas, incluyendo campos de descripción con texto enriquecido, colores, y las imágenes asociadas.
"""

from django.contrib import admin
from .models import Categoria, Tag
from django.utils.html import format_html
from multimedia.models import MediaFile
from core.admin.base_img_mixin import filter_image_queryset

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Definir qué columnas se muestran en la lista de categorías
    list_display = ('nombre', 'color', 'mostrar_imagen', 'padre')
    search_fields = ('nombre',)
    list_filter = ('color', 'padre')
    
    # Campos del formulario de creación y edición
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'color', 'imagen', 'padre')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        model_name = Categoria.__name__
        meta_id = None

        if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
            meta_id = request.resolver_match.kwargs['object_id']

        # Ajustar el queryset de imágenes si el campo es 'categorias'
        if db_field.name == 'categorias':
            kwargs['queryset'] = filter_image_queryset(model_name, meta_id)
            kwargs['empty_label'] = 'Sin imagen asociada'
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    # Mostrar la imagen asociada en la lista de categorías
    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.imagen.file.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Imagen"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Definir qué columnas se muestran en la lista de etiquetas
    list_display = ('nombre', 'color', 'mostrar_imagen')
    search_fields = ('nombre',)
    list_filter = ('color',)
    
    # Campos del formulario de creación y edición
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'color', 'imagen')
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        model_name = Categoria.__name__
        meta_id = None

        if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
            meta_id = request.resolver_match.kwargs['object_id']

        # Ajustar el queryset de imágenes si el campo es 'tags'
        if db_field.name == 'tags':
            kwargs['queryset'] = filter_image_queryset(model_name, meta_id)
            kwargs['empty_label'] = 'Sin imagen asociada'
        # Ajustar el queryset de documentos si el campo es 'documento'
    # Mostrar la imagen asociada en la lista de etiquetas
    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.imagen.file.url)
        return "Sin imagen"
    mostrar_imagen.short_description = "Imagen"
