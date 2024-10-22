from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField  # Necesitarás instalar django-countries
from core.models import BurgerType, Allergy


class UserProfile(models.Model):
    # Relación OneToOne con el usuario
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="Usuario asociado a este perfil"
    )

    # Información personal
    foto_perfil = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text="Sube una foto de perfil (opcional)"
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        help_text="Ingresa tu fecha de nacimiento"
    )
    telefono = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Número de teléfono de contacto"
    )
    direccion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Dirección de residencia (calle y número)"
    )
    ciudad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Ciudad donde vives"
    )
    codigo_postal = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Código postal de tu área"
    )
    pais = CountryField(
        null=True,
        blank=True,
        help_text="País de residencia"
    )

    gustos_hamburguesas = models.ManyToManyField(
        BurgerType,  # Referencia como cadena
        blank=True,
        help_text="Selecciona tus hamburguesas favoritas"
    )

    alergias = models.ManyToManyField(
        Allergy,  # Referencia como cadena
        blank=True,
        help_text="Indica si tienes alguna alergia alimentaria"
    )


    suscripcion_boletin = models.BooleanField(
        default=False,
        help_text="Marca esta casilla si deseas recibir nuestro boletín de noticias"
    )

    # Información adicional
    puntos_fidelidad = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        help_text="Puntos acumulados en el programa de fidelidad"
    )
    fecha_registro = models.DateTimeField(
        help_text="Fecha en que te uniste a nosotros",
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username
