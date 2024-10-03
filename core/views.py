from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['products'] = [
            {
                'nombre': 'Hamburguesa Vegana',
                'descripcion': 'Una opción saludable con un medallón de garbanzos, lechuga, tomate y aguacate.',
                'precio': 7.99,
                'imagen': 'images/sample/burguer3.jpg',
                'url': '/productos/producto1/',
                'preloader_id': 'preloader-1'

            },
            {
                'nombre': 'Hamburguesa BBQ',
                'descripcion': 'Jugosa hamburguesa cubierta con nuestra salsa BBQ especial, cebolla caramelizada y queso cheddar.',
                'precio': 9.99,
                'imagen': 'images/sample/burguer2.jpg',
                'url': '/productos/producto2/',
                'preloader_id': 'preloader-2'
            },
            {
                'nombre': 'Hamburguesa Clásica',
                'descripcion': 'Deliciosa hamburguesa clásica con lechuga, tomate, queso cheddar y carne de res de la mejor calidad.',
                'precio': 8.99,
                'imagen': 'images/sample/burguer1.jpg',
                'url': '/productos/producto3/',
                'preloader_id': 'preloader-3'
            }
        ]

        return context
