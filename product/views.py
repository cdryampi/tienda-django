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

        # Obtener los precios del producto
        context['precios'] = self.object.precios.all()

        # Obtener las alergias asociadas
        context['alergias'] = self.object.alergias.all()

        # Tipo de hamburguesa
        context['tipo_hamburguesa'] = self.object.hamburguesa.nombre if self.object.hamburguesa else None

        return context

# productos

class ProductoListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        # Obtener el idioma y la moneda preferida del usuario o sesión
        current_language = IdiomaMixin.get_idioma(self)
        moneda = IdiomaMixin.get_moneda_preferida(current_language)
        # Consulta de productos activos con precios, alergias y hamburguesa
        productos  = Product.objects.prefetch_related(
            'precios',
            'alergias',
            'hamburguesa'
        ).active_translations(
            current_language
        ).filter(
            is_active = True,
            
        ).distinct()
        # Obtener los datos del formulario de POST
        categoria_id = self.request.POST.get('categoria')
        precio_min = self.request.POST.get('precio_min')
        precio_max = self.request.POST.get('precio_max')

        # Aplicar los filtros en el queryset
        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)

        if precio_min:
            productos = productos.filter(precios__precio__gte=precio_min)
        
        if precio_max:
            productos = productos.filter(precios__precio__lte=precio_max)

        productos_con_precios = []

        for producto in productos:
            # Obtener el precio basado en la moneda preferida o el primer precio disponible
            precio = producto.precios.filter(precio_currency=moneda).first()
            if not precio:
                precio = producto.precios.first()
            print(f"Producto: {producto.titulo}, Slug: {producto.slug}")
            # Construir el diccionario para cada producto con la información necesaria
            productos_con_precios.append({
                'titulo': producto.safe_translation_getter('titulo', current_language),
                'descripcion': producto.safe_translation_getter('descripcion', current_language),
                'precio': precio.precio if precio else None,  # Precio en la moneda seleccionada o None
                'imagen_url': producto.imagen.file.url if producto.imagen else None,
                'product_slug': producto.slug,
                'alergias': producto.alergias.all(),  # Alergias asociadas
                'tipo_hamburguesa': producto.hamburguesa.nombre if producto.hamburguesa else None  # Tipo de hamburguesa
            })
        return productos_con_precios



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()  # Pasar las categorías al contexto
        # El queryset ya tiene la lista de productos procesada en get_queryset
        context['products'] = self.get_queryset()
        return context
    def post(self, request, *args, **kwargs):
        # Sobreescribimos el método post para manejar las solicitudes POST
        if request.method == 'POST':
            return self.get(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(['POST'])