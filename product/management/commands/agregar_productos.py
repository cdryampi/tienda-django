from django.core.management.base import BaseCommand
from django.utils import translation
from django.db import transaction
from django.conf import settings
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files import File
import shutil


# Importa tus modelos
from product.models import Producto
from pricing.models import PrecioProducto
from multimedia.models import MediaFile, DocumentFile
from common.models import Categoria, Tag
from core.models import Hamburguesa, Alergia
from djmoney.money import Money
from django.utils.text import slugify


from multimedia.utils.utils import archivo_existe
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Agrega productos a la base de datos desde un script con soporte para traducciones y relaciones'

    def handle(self, *args, **kwargs):
        productos_a_agregar = [
            {
                'titulo_es': 'Hamburguesa Clásica',
                'titulo_en': 'Classic Burger',
                'descripcion_es': 'Una deliciosa hamburguesa clásica.',
                'descripcion_en': 'A delicious classic burger.',
                'categoria': 'Comida Rápida',
                'imagen': 'images/sample/burguer1.jpg',
                'hamburguesa': 'clasica',
                'alergias': ['gluten', 'lactosa'],
                'en_stock': True,
                'tags': ['popular', 'oferta'],
                'precios': [
                    {'cantidad': 5.99, 'moneda': 'EUR'},
                    {'cantidad': 6.99, 'moneda': 'USD'},
                ],
            },
            {
                'titulo_es': 'Hamburguesa Doble',
                'titulo_en': 'Double Burger',
                'descripcion_es': 'Hamburguesa con doble carne.',
                'descripcion_en': 'Burger with double meat.',
                'categoria': 'Comida Rápida',
                'imagen': 'images/sample/burguer2.jpg',
                'hamburguesa': 'doble',
                'alergias': ['gluten', 'lactosa', 'soja'],
                'en_stock': True,
                'tags': ['novedad', 'sabroso'],
                'precios': [
                    {'cantidad': 7.99, 'moneda': 'EUR'},
                    {'cantidad': 8.99, 'moneda': 'USD'},
                ],
            },
            {
                'titulo_es': 'Hamburguesa Vegetariana',
                'titulo_en': 'Vegetarian Burger',
                'descripcion_es': 'Una opción saludable sin carne.',
                'descripcion_en': 'A healthy meat-free option.',
                'categoria': 'Comida Saludable',
                'imagen': 'images/sample/burguer3.jpg',
                'hamburguesa': 'vegetariana',
                'alergias': ['gluten', 'soja'],
                'en_stock': True,
                'tags': ['saludable', 'verde'],
                'precios': [
                    {'cantidad': 6.99, 'moneda': 'EUR'},
                    {'cantidad': 7.99, 'moneda': 'USD'},
                ],
            },
            {
                'titulo_es': 'Hamburguesa de Pollo',
                'titulo_en': 'Chicken Burger',
                'descripcion_es': 'Deliciosa hamburguesa de pollo.',
                'descripcion_en': 'Delicious chicken burger.',
                'categoria': 'Comida Rápida',
                'imagen': 'images/sample/burguer4.jpg',
                'hamburguesa': 'pollo',
                'alergias': ['gluten'],
                'en_stock': False,
                'tags': ['pollo', 'popular'],
                'precios': [
                    {'cantidad': 6.49, 'moneda': 'EUR'},
                    {'cantidad': 7.49, 'moneda': 'USD'},
                ],
            },
            {
                'titulo_es': 'Hamburguesa Especial',
                'titulo_en': 'Special Burger',
                'descripcion_es': 'La especialidad de la casa.',
                'descripcion_en': 'The house specialty.',
                'categoria': 'Gourmet',
                'imagen': 'images/sample/burguer5.jpg',
                'hamburguesa': 'especial',
                'alergias': ['gluten', 'lactosa', 'huevo'],
                'en_stock': True,
                'tags': ['especial', 'gourmet'],
                'precios': [
                    {'cantidad': 9.99, 'moneda': 'EUR'},
                    {'cantidad': 11.99, 'moneda': 'USD'},
                ],
            },
        ]

        User = get_user_model()
        owner = User.objects.first()
        if not owner:
            self.stderr.write(self.style.ERROR('No se encontró un usuario para asignar como propietario.'))
            return
        
        for producto_data in productos_a_agregar:
            with transaction.atomic():
                # Manejo de la categoría
                categoria, _ = Categoria.objects.get_or_create(nombre=producto_data['categoria'])

                # Manejo de la imagen
                imagen = self.handle_image(producto_data.get('imagen'), owner)

                # Manejo de Hamburguesa
                hamburguesa, _ = Hamburguesa.objects.get_or_create(nombre=producto_data['hamburguesa'])

                # Crear el producto
                producto, creado = Producto.objects.get_or_create(
                    categoria=categoria,
                    imagen=imagen,
                    hamburguesa=hamburguesa,
                    en_stock=producto_data.get('en_stock', True),
                )

                # Solo proceder si el producto fue creado
                if creado:
                    # Manejar las traducciones
                    self.add_translations(producto, producto_data)

                    # Crear el slug
                    self.generate_unique_slug(producto, producto_data['titulo_es'])

                    # Manejo de alergias
                    self.handle_alergias(producto, producto_data.get('alergias', []))

                    # Manejo de tags
                    self.handle_tags(producto, producto_data.get('tags', []))

                    # Manejo de precios
                    self.handle_precios(producto, producto_data.get('precios', []))

                    self.stdout.write(self.style.SUCCESS(f"Producto '{producto}' creado exitosamente."))
                else:
                    self.stdout.write(self.style.WARNING(f"El producto '{producto}' ya existe."))
    

    def handle_image(self, imagen_ruta, owner):
        ruta_imagen = archivo_existe(imagen_ruta)
        if ruta_imagen:
            nombre_archivo = os.path.basename(imagen_ruta)
            destino_imagen = os.path.join('media_files', nombre_archivo)
            ruta_destino = os.path.join(settings.MEDIA_ROOT, destino_imagen)

            os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
            shutil.copyfile(ruta_imagen, ruta_destino)

            imagen, _ = MediaFile.objects.get_or_create(
                file=destino_imagen,
                defaults={'title': nombre_archivo, 'owner': owner}
            )
            return imagen
        return None

    def add_translations(self, producto, producto_data):
        for lang_code in ['es', 'en']:
            translation.activate(lang_code)
            producto.set_current_language(lang_code)
            producto.titulo = producto_data.get(f'titulo_{lang_code}')
            producto.descripcion = producto_data.get(f'descripcion_{lang_code}')
            producto.save()
            translation.deactivate()

    def generate_unique_slug(self, producto, titulo_es):
        if titulo_es:
            base_slug = slugify(titulo_es)
            slug = base_slug
            num = 1
            while Producto.objects.filter(slug=slug).exclude(pk=producto.pk).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            producto.slug = slug
            producto.save(update_fields=['slug'])
    
    def handle_alergias(self, producto, alergias_nombres):
        alergias_objs = Alergia.objects.filter(nombre__in=alergias_nombres)
        producto.alergias.set(alergias_objs)

    def handle_tags(self, producto, tags_nombres):
        tags_objs = []
        for tag_nombre in tags_nombres:
            tag, _ = Tag.objects.get_or_create(nombre=tag_nombre)
            tags_objs.append(tag)
        producto.tags.set(tags_objs)

    def handle_precios(self, producto, precios):
        for precio_data in precios:
            PrecioProducto.objects.create(
                producto=producto,
                precio=Money(precio_data['cantidad'], precio_data['moneda'])
            )
