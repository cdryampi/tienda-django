"""
Modelo `Producto` con soporte para categorías, etiquetas, imágenes, documentos y otros metadatos.

Futuras modificaciones pendientes:

1. **Atributos para Comentarios y Likes**:
   - Faltan los atributos para gestionar los comentarios y likes en productos, hamburguesas y alergias. Se planea añadir relaciones con un modelo de comentarios y un contador de likes para cada uno de estos modelos. 
   - Esto implicará la creación de un modelo `Comentario` que podría tener relación con `Producto`, `Hamburguesa`, y `Alergia`.

2. **Imágenes adicionales en Hamburguesa y Alergia**:
   - En los modelos `Hamburguesa` y `Alergia`, se añadirá un campo para gestionar imágenes. Esto permitirá asociar imágenes a estos modelos de la misma manera que se hace con `Producto`.

3. **Restricción en el Admin**:
   - Se limitará el acceso al panel de administración de Django para que solo los usuarios con permisos de `super_user` puedan acceder y realizar cambios en los modelos sensibles, incluyendo `Producto`, `Hamburguesa`, y `Alergia`. 
   - Esto se implementará mediante ajustes en las configuraciones del `admin.py`.

4. **Activación de Multi-idiomas**:
   - Se habilitará el soporte multi-idioma para el modelo `Producto` y otros modelos relevantes mediante la integración con Django `parler` o una solución similar para manejar traducciones de campos como `nombre`, `descripcion`, etc.

5. **Serialización y creación de API**:
   - Se planificará la serialización de este modelo utilizando Django Rest Framework (DRF) para exponer una API que permita la consulta de productos, hamburguesas, alergias, y otros modelos.
   - Esta API facilitará la integración con otras aplicaciones, como frontends o aplicaciones móviles.
"""

from django.db import models
from multimedia.models import MediaFile, DocumentFile
from core.models import MetaBase, MetadataModel, AuditModel, SlugModel, Hamburguesa, Alergia
from common.models import Categoria, Tag
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from django.utils.text import slugify


class Producto(TranslatableModel, MetaBase, MetadataModel, AuditModel, SlugModel):
    """
    Modelo que representa un producto con soporte para categorías, etiquetas, múltiples precios, imágenes, 
    documentos, y otros metadatos como la auditoría y el manejo de slugs.
    """
    translations = TranslatedFields(
        titulo=models.CharField(max_length=100, verbose_name="Título"),
        descripcion=CKEditor5Field(verbose_name="Descripción", null=True, blank=True, config_name='default')
    )
    # Relación con Categoria desde la app common
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        help_text="Categoría a la que pertenece el producto"
    )
    
    # Relación con MediaFile para la imagen del producto
    imagen = models.ForeignKey(
        MediaFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='productos_imagenes',
        help_text="Selecciona una imagen desde la galería de archivos multimedia"
    )

    # Relación con DocumentFile para un documento o nota relevante del producto
    documento = models.ForeignKey(
        DocumentFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos_documentos',
        help_text="Sube una nota o documento relevante asociado con el producto"
    )

    # Relación con Hamburguesa y Alergia
    hamburguesa = models.ForeignKey(
        Hamburguesa,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    alergias = models.ManyToManyField(
        Alergia,
        blank=True,
        help_text="Alergias relacionadas con el producto"
    )

    # Campo de stock para indicar disponibilidad
    en_stock = models.BooleanField(default=True)

    # Relación con Tag desde la app common
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='productos',
        help_text="Etiquetas relacionadas con el producto"
    )

    # Método para obtener las imágenes relacionadas con el producto en función de la fecha
    def filtrar_imagenes(self, fecha_inicio=None, fecha_fin=None):
        """
        Filtra las imágenes asociadas al producto según criterios como fecha de subida.
        """
        imagenes = self.imagen.productos.all()
        
        if fecha_inicio:
            imagenes = imagenes.filter(uploaded_at__gte=fecha_inicio)
        
        if fecha_fin:
            imagenes = imagenes.filter(uploaded_at__lte=fecha_fin)
        
        return imagenes
    def save(self, *args, **kwargs):
        # Si el objeto no tiene un pk, lo guardamos primero
        if not self.pk:
            super().save(*args, **kwargs)

        # Generar el slug si no existe
        if not self.slug:
            # Obtener el título en cualquier idioma disponible
            titulo = self.safe_translation_getter('titulo', any_language=True)
            if titulo:
                base_slug = slugify(titulo)
                slug = base_slug
                num = 1
                # Asegurarse de que el slug es único, excluyendo el objeto actual
                while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{num}"
                    num += 1
                self.slug = slug
            else:
                # Si no hay título, asignar un slug genérico usando el pk
                self.slug = str(self.pk)
            # Guardamos nuevamente para actualizar el slug
            super().save(update_fields=['slug'])
        else:
            super().save(*args, **kwargs)
    def __str__(self):
        return self.safe_translation_getter('titulo', any_language=True)
