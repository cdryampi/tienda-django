"""
Este archivo contiene los modelos para las categorías y etiquetas, utilizados en el sistema de productos.

1. `RichTextField (CKEditor5)`:
   - Se utiliza en los campos de descripción de las categorías y etiquetas.
   - Proporciona una interfaz avanzada de edición de texto enriquecido, permitiendo la inclusión de
     texto con formato (negrita, cursiva, subrayado), imágenes, tablas, enlaces y más.
   - CKEditor5 facilita la creación de contenido visualmente atractivo, ideal para descripciones detalladas
     que requieran un formato específico.

2. `ColorField`:
   - Permite asignar un color en formato hexadecimal a cada categoría y etiqueta.
   - Los colores se utilizan para mejorar la interfaz de usuario, destacando o diferenciando visualmente
     las categorías y etiquetas en diferentes páginas (como landings o filtros).
   - El color por defecto es rojo (`#FF0000` para categorías) y azul (`#0000FF` para etiquetas), pero puede 
     personalizarse desde el panel de administración o al crear/editar una categoría o etiqueta.

3. `MediaFile`:
   - Cada categoría y etiqueta puede tener una imagen asociada mediante el modelo `MediaFile`, que permite
     la gestión centralizada de archivos multimedia. Estas imágenes pueden utilizarse en landings de productos,
     páginas de filtros, o para mostrar elementos visuales relacionados con las categorías y etiquetas.
"""

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from colorfield.fields import ColorField
from multimedia.models import MediaFile

class Category(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True
    )
    
    # Usamos CKEditor5 para la descripción de la categoría
    descripcion = CKEditor5Field(
        verbose_name="Descripción",
        null=True,
        blank=True,
        config_name='default'
    )
    
    # Campo para asignar un color a la categoría
    color = ColorField(default='#FF0000')  # Valor por defecto es rojo, puedes cambiarlo
    
    # Imagen relacionada con la categoría, a través de MediaFile
    imagen = models.ForeignKey(
        MediaFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='categorias',
        help_text="Selecciona una imagen para esta categoría"
    )
    
    # Auto-relación para subcategorías
    padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategorias',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre


class Tag(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    # Usamos CKEditor5 para la descripción de la etiqueta
    descripcion = CKEditor5Field(
        verbose_name="Descripción",
        null=True,
        blank=True,
        config_name='default'
    )
    
    # Campo para asignar un color a la etiqueta
    color = ColorField(default='#0000FF')  # Valor por defecto es azul, puedes cambiarlo
    
    # Imagen relacionada con la etiqueta, a través de MediaFile
    imagen = models.ForeignKey(
        MediaFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tags',
        help_text="Selecciona una imagen para esta etiqueta"
    )

    def __str__(self):
        return self.nombre
