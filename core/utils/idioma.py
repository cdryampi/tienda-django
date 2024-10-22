from django.utils import translation
from django.conf import settings

class IdiomaMixin:
    """
    Mixin para recuperar el idioma actual desde la sesión o el usuario.
    """
    def get_idioma(self):
        # Obtener el idioma actual desde la sesión
        idioma = self.request.session.get('django_language')

        # Si no hay idioma en la sesión, usar el idioma actual de Django
        if not idioma:
            idioma = translation.get_language()

        return idioma
    
    def get_moneda_preferida(idioma):
        """
        Método opcional para recuperar la moneda preferida según el idioma o el país.
        """

        return settings.IDIOMA_A_MONEDA.get(idioma, 'EUR')  # Devolver EUR por defecto