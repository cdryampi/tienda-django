from django.core.management.base import BaseCommand
from core.models import BurgerType, Allergy
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Crea hamburguesas favoritas y alergias iniciales'

    def handle(self, *args, **kwargs):
        """
            Función que genera los datos iniciales de la aplicación además de limpia la base de datos.
        """
        self.stdout.write(self.style.SUCCESS('Eliminando la base de datos...'))
        call_command('delete_all_data')


        self.stdout.write(self.style.SUCCESS('Hamburguesas y Alergias creadas exitosamente'))

        hamburguesas = [
            {'nombre': 'clasica', 'descripcion': 'Hamburguesa clasica con doble porción de carne de res.'},
            {'nombre': 'doble', 'descripcion': 'Hamburguesa con doble porción de carne de res.'},
            {'nombre': 'vegetariana', 'descripcion': 'Hamburguesa con ingredientes vegetales y sin carne.'},
            {'nombre': 'pollo', 'descripcion': 'Hamburguesa con carne de pollo marinada.'},
            {'nombre': 'especial', 'descripcion': 'Nuestra receta secreta con los mejores ingredientes.'},
        ]

        for h in hamburguesas:
            BurgerType.objects.get_or_create(nombre=h['nombre'])

        alergias = [
            'gluten', 'lactosa', 'soja', 'frutos_secos', 'mariscos', 
            'huevo'
        ]

        for a in alergias:
            Allergy.objects.get_or_create(nombre=a)
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales creados exitosamente'))
        self.stdout.write(self.style.SUCCESS('creando superusuario y usuarios de muestra...'))
        call_command('add_super_user_and_sample_users')

        self.stdout.write(self.style.SUCCESS('Añadiendo productos de muestra...'))
        call_command('agregar_productos')