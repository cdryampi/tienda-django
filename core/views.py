from django.views.generic import TemplateView
from django.contrib import messages
from product.models import Product
from core.utils.idioma import IdiomaMixin


# Create your views here.

class StripeFindDetailView(TemplateView):
    
    template_name = 'core/payment_sprite.html'

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Revisar si hay mensajes en la request
        storange = messages.get_messages(self.request)

        for message in storange:
            context['mensaje_sistema'] = message
        
        current_language = IdiomaMixin.get_idioma(self)
        moneda = IdiomaMixin.get_moneda_preferida(current_language)
        # Consulta de productos con precios traducidos
        productos = Product.objects.prefetch_related(
            'precios',
            'alergias',
            'hamburguesa'
        ).active_translations(
            current_language
        ).filter(
            is_active = True,
        ).distinct()[:8]

        productos_con_precios = []
        for producto in productos:
            # Obtener el precio basado en la moneda o primer precio disponible
            # Filtrar precios por moneda
            precio = producto.precios.filter(precio_currency=moneda).first()
            # Si no hay precio en la moneda preferida, usar el primer precio disponible
            if not precio:
                precio = producto.precios.first()
            
            # Obtener las alergias y el tipo de hamburguesa (si están configurados)
            alergias = producto.alergias.all()  # Lista de alergias asociadas al producto
            tipo_hamburguesa = producto.hamburguesa  # Tipo de hamburguesa (ForeignKey)
            productos_con_precios.append({
                'id': producto.id,
                'titulo': producto.safe_translation_getter('titulo', current_language),
                'descripcion': producto.safe_translation_getter('descripcion', current_language),
                'precio': precio.precio if precio else None,  # Precio en el formato que necesitas
                'imagen_url': producto.imagen.file.url if producto.imagen else None,
                'producto_slug': producto.slug,
                'alergias': alergias,  # Alergias asociadas
                'tipo_hamburguesa': tipo_hamburguesa.nombre if tipo_hamburguesa else None  # Tipo de hamburguesa
            })

        context['products'] = productos_con_precios
        return context