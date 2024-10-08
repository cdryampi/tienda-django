from django.db import models
from django.utils import timezone

# Create your models here.
class MetadataModel(models.Model):
    """
        Modelo que representa los metadatos del sitio para los otros modelos.
    """

    meta_titulo = models.CharField(
        max_length= 255,
        help_text= "Metatitulo para el Seo",
        null = True,
        blank= True,
        verbose_name= "Metatitulo"
    )

    meta_descripcion = models.CharField(
        max_length= 255,
        help_text= "Metadescripción para el Seo",
        null = True,
        blank= True,
        verbose_name= "Metatitulo"
    )

    class Meta:
        abstract = True

class MetaBase(models.Model):
    """
    Clase abstracta para agregar metadatos comunes a los modelos.
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']  # Ordenar por fecha de creación

    def soft_delete(self):
        """Método para desactivar el objeto sin eliminarlo permanentemente."""
        self.is_active = False
        self.save()

    def restore(self):
        """Método para restaurar un objeto que ha sido desactivado."""
        self.is_active = True
        self.save()


class Hamburguesa(models.Model):
    NOMBRES_HAMBURGUESAS = [
        ('clasica', 'Clásica'),
        ('doble', 'Doble carne'),
        ('vegetariana', 'Vegetariana'),
        ('pollo', 'Pollo'),
        ('especial', 'Especial de la casa'),
    ]
    nombre = models.CharField(
        max_length=20,
        choices=NOMBRES_HAMBURGUESAS,
        unique=True
    )

    def __str__(self):
        return self.get_nombre_display()

    def save(self, *args, **kwargs):
        # Evita guardar nuevas instancias si el nombre no está en las opciones
        if self.nombre not in dict(self.NOMBRES_HAMBURGUESAS):
            raise ValueError("Esta opción de hamburguesa no es válida.")
        super().save(*args, **kwargs)


class Alergia(models.Model):
    TIPOS_ALERGIAS = [
        ('gluten', 'Gluten'),
        ('lactosa', 'Lactosa'),
        ('soja', 'Soja'),
        ('frutos_secos', 'Frutos secos'),
        ('mariscos', 'Mariscos'),
        ('huevo', 'Huevo'),
    ]
    nombre = models.CharField(
        max_length=20,
        choices=TIPOS_ALERGIAS,
        unique=True
    )

    def __str__(self):
        return self.get_nombre_display()

    def save(self, *args, **kwargs):
        # Evita guardar nuevas instancias si el nombre no está en las opciones
        if self.nombre not in dict(self.TIPOS_ALERGIAS):
            raise ValueError("Esta opción de alergia no es válida.")
        super().save(*args, **kwargs)