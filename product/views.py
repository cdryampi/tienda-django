from django.views.generic import ListView, DetailView
from .models import Product, Category
from core.utils.idioma import IdiomaMixin
from django.http import HttpResponseNotAllowed




class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_language = IdiomaMixin.get_idioma(self)
        moneda = IdiomaMixin.get_moneda_preferida(current_language)

        context['product'] = self.get_object()
        context['product_price'] = self.get_object().precios.filter(precio_currency=moneda).first().precio
        # Consulta de productos relacionados (excluyendo el producto actual)
        productos_relacionados_queryset = Product.objects.prefetch_related(
            'precios', 'alergias', 'hamburguesa'
        ).active_translations(
            current_language
        ).filter(
            is_active=True,
            categoria = self.object.categoria
        ).exclude(
            pk=self.object.pk  # Excluir el producto actual
        ).distinct()[:4]

        productos_relacionados = []
        for producto in productos_relacionados_queryset:
            # Obtener el precio basado en la moneda preferida o el primer precio disponible
            precio = producto.precios.filter(precio_currency=moneda).first()
            if not precio:
                precio = producto.precios.first()

            # Construir el diccionario para cada producto con la información necesaria
            productos_relacionados.append({
                'id': producto.id,
                'titulo': producto.safe_translation_getter('titulo', current_language),
                'descripcion': producto.safe_translation_getter('descripcion', current_language),
                'precio': precio.precio if precio else None,  # Precio en la moneda seleccionada o None
                'imagen_url': producto.imagen.file.url if producto.imagen else None,
                'product_slug': producto.slug,
                'alergias': producto.alergias.all(),  # Alergias asociadas
                'tipo_hamburguesa': producto.hamburguesa.nombre if producto.hamburguesa else None  # Tipo de hamburguesa
            })

        # Añadir los productos relacionados al contexto
        context['productos_relacionados'] = productos_relacionados

        return context


# productos

class ProductoListView(ListView):
    model = Product
    template_name = 'product/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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