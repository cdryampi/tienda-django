from django.views.generic import ListView, DetailView
from .models import Product, Category
from core.utils.idioma import IdiomaMixin
from django.http import HttpResponseNotAllowed

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_obj = self.object  # Guardamos el objeto para evitar múltiples llamadas

        # Obtener idioma y moneda preferida
        current_language = IdiomaMixin.get_idioma(self)
        moneda = IdiomaMixin.get_moneda_preferida(current_language)

        # Obtener el precio del producto en la moneda deseada o el primero disponible
        precio_actual = product_obj.precios.filter(precio_currency=moneda).first()
        if not precio_actual:
            precio_actual = product_obj.precios.first()

        # Construcción del diccionario de producto
        product_data = {
            'id': product_obj.id,
            'titulo': product_obj.safe_translation_getter('titulo', current_language),
            'descripcion': product_obj.safe_translation_getter('descripcion', current_language),
            'precio': precio_actual.precio if precio_actual else None,
            'imagen_url': product_obj.imagen.file.url if product_obj.imagen else None,
            'product_slug': product_obj.slug,
            'alergias': product_obj.alergias.all(),
            'tipo_hamburguesa': product_obj.hamburguesa.nombre if product_obj.hamburguesa else None
        }

        # Consulta de productos relacionados optimizada
        productos_relacionados_queryset = Product.objects.prefetch_related(
            'precios', 
            'alergias', 
            'hamburguesa'
        ).filter(
            is_active=True,
            categoria=product_obj.categoria
        ).exclude(pk=product_obj.pk)  # Excluir el producto actual




        # Agregar al contexto
        context['product'] = product_data

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