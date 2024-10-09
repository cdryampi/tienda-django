from django.core.management.base import BaseCommand
from core.models import Hamburguesa, Alergia

class Command(BaseCommand):
    help = 'Crea hamburguesas favoritas y alergias iniciales'

    def handle(self, *args, **kwargs):
        hamburguesas = [
            {'nombre': 'Clásica', 'descripcion': 'Hamburguesa tradicional con ingredientes frescos.'},
            {'nombre': 'Doble carne', 'descripcion': 'Hamburguesa con doble porción de carne de res.'},
            {'nombre': 'Vegetariana', 'descripcion': 'Hamburguesa con ingredientes vegetales y sin carne.'},
            {'nombre': 'Pollo', 'descripcion': 'Hamburguesa con carne de pollo marinada.'},
            {'nombre': 'Especial de la casa', 'descripcion': 'Nuestra receta secreta con los mejores ingredientes.'},
        ]

        for h in hamburguesas:
            Hamburguesa.objects.get_or_create(nombre=h['nombre'], defaults={'descripcion': h['descripcion']})

        alergias = [
            'Gluten', 'Lactosa', 'Soja', 'Frutos secos', 'Mariscos', 
            'Huevo', 'Pescado', 'Apio', 'Mostaza', 'Sésamo'
        ]

        for a in alergias:
            Alergia.objects.get_or_create(nombre=a)

        self.stdout.write(self.style.SUCCESS('Hamburguesas y Alergias creadas exitosamente'))
