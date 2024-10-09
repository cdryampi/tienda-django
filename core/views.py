from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages

# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Revisar si hay mensajes en la request
        storange = messages.get_messages(self.request)

        for message in storange:
            print(message)
            context['mensaje_sistema'] = message

        context['products'] = [
            {
                'nombre': 'Hamburguesa Vegana',
                'descripcion': 'Una opción saludable con un medallón de garbanzos, lechuga, tomate y aguacate.',
                'precio': 7.99,
                'imagen': 'images/sample/burguer3.jpg',
                'url': '/productos/producto1/',
                'preloader_id': 'preloader-1',
                'alergias': ['soja', 'gluten'],
                'gustos': ['vegetariana'],
                'preferencias_dieteticas': ['vegano', 'vegetariano']
            },
            {
                'nombre': 'Hamburguesa BBQ',
                'descripcion': 'Jugosa hamburguesa cubierta con nuestra salsa BBQ especial, cebolla caramelizada y queso cheddar.',
                'precio': 9.99,
                'imagen': 'images/sample/burguer2.jpg',
                'url': '/productos/producto2/',
                'preloader_id': 'preloader-2',
                'alergias': ['lactosa', 'gluten'],
                'gustos': ['doble'],
                'preferencias_dieteticas': ['carnivoro']
            },
            {
                'nombre': 'Hamburguesa Clásica',
                'descripcion': 'Deliciosa hamburguesa clásica con lechuga, tomate, queso cheddar y carne de res de la mejor calidad.',
                'precio': 8.99,
                'imagen': 'images/sample/burguer1.jpg',
                'url': '/productos/producto3/',
                'preloader_id': 'preloader-3',
                'alergias': ['lactosa', 'gluten'],
                'gustos': ['clasica'],
                'preferencias_dieteticas': ['carnivoro']
            },
            {
                'nombre': 'Hamburguesa Picante',
                'descripcion': 'Hamburguesa con un toque picante, jalapeños y salsa especial picante.',
                'precio': 9.49,
                'imagen': 'images/sample/burguer4.jpg',
                'url': '/productos/producto4/',
                'preloader_id': 'preloader-4',
                'alergias': ['gluten'],
                'gustos': ['doble'],
                'preferencias_dieteticas': ['carnivoro']
            },
            {
                'nombre': 'Hamburguesa Especial de la Casa',
                'descripcion': 'Nuestra receta especial con ingredientes frescos y un sabor único.',
                'precio': 10.99,
                'imagen': 'images/sample/burguer5.jpg',
                'url': '/productos/producto5/',
                'preloader_id': 'preloader-5',
                'alergias': ['gluten', 'huevo'],
                'gustos': ['especial'],
                'preferencias_dieteticas': ['carnivoro']
            }
        ]

        return context
