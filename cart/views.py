from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from product.models import Product
from .models import Cart, CartItem
from djmoney.money import Money
from core.utils.idioma import IdiomaMixin

class addProductToCard(View):
    """
    Vista para añadir un producto al carrito.
    """

    def post(self, request, *args, **kwards):
        try:

            product_id = request.POST.get('product_id')
            if not product_id:
                return JsonResponse({'status': 'error', 'message': 'No se ha especificado el ID del producto.'})
            quantity = request.POST.get('quantity', 1)

            product = get_object_or_404(Product, id=product_id)

            # Obtener el carrito del usuario o de la sesión

            cart_id = request.session.get('cart_id')

            if cart_id:
                try:
                    cart = Cart.objects.get(id=cart_id)
                except Cart.DoesNotExist:
                    if request.user.is_authenticated:
                        cart = Cart.objects.create(user=request.user)
                        request.session['cart_id'] = cart.id
                    else:
                        cart = Cart.objects.create(user=None)
                        request.session['cart_id'] = cart.id
            else:
                if request.user.is_authenticated:
                    cart = Cart.objects.create(user=request.user)
                    request.session['cart_id'] = cart.id
                else:
                    cart = Cart.objects.create(user=None)
                    request.session['cart_id'] = cart.id
            
            # Obtener el idioma actual
            current_language = IdiomaMixin.get_idioma(self)  # Pasar request en lugar de self
            moneda = IdiomaMixin.get_moneda_preferida(current_language)

            # Buscar el precio en la moneda preferida o el primero disponible
            precio_producto = product.precios.filter(precio_currency=moneda).first()

            if not precio_producto:
                # Si no hay un precio en la moneda preferida, usamos el primer precio disponible
                precio_producto = product.precios.first()

            # Verificar si el producto tiene un precio válido
            if not precio_producto or precio_producto.precio.amount is None:
                # Mensaje de error si el producto no tiene un precio válido
                # messages.error(request, "El producto no tiene un precio válido asignado.")
                return redirect('product:producto_detalle', slug=product.slug)

            # Buscar si el producto ya está en el carrito
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'price': precio_producto.precio}
            )

            if not created:
                # Si el producto ya estaba en el carrito, incrementar la cantidad
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
                # Asegurarse de que el precio esté correctamente asignado
                cart_item.price = Money(precio_producto.precio.amount, precio_producto.precio_currency)

            # Guardar el item del carrito
            cart_item.save()

            # Devolver una respuesta JSON

            response = {
                'status': 'success',
                'message': f'{product.titulo} añadido al carrito.',
            }
            print(cart.get_cart_items())
            print(request.session['cart_id'])
            print(cart.user)
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})



class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = get_object_or_404(Product, slug=product_slug)

        # Obtener el ID del carrito desde la sesión
        cart_id = request.session.get('cart_id')

        if cart_id:
            # Si ya existe un carrito en la sesión
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=None)  # Crear un nuevo carrito para usuario anónimo
                request.session['cart_id'] = cart.id
        else:
            # Si no existe, creamos un carrito en la sesión
            cart = Cart.objects.create(user=None)
            request.session['cart_id'] = cart.id

        # Obtener la cantidad que el usuario quiere agregar (por defecto 1)
        quantity = int(request.POST.get('quantity', 1))

        # Obtener el idioma actual
        current_language = IdiomaMixin.get_idioma(self)  # Pasar request en lugar de self
        moneda = IdiomaMixin.get_moneda_preferida(current_language)

        # Buscar el precio en la moneda preferida o el primero disponible
        precio_producto = product.precios.filter(precio_currency=moneda).first()

        if not precio_producto:
            # Si no hay un precio en la moneda preferida, usamos el primer precio disponible
            precio_producto = product.precios.first()

        # Verificar si el producto tiene un precio válido
        if not precio_producto or precio_producto.precio.amount is None:
            # Mensaje de error si el producto no tiene un precio válido
            # messages.error(request, "El producto no tiene un precio válido asignado.")
            return redirect('product:producto_detalle', slug=product.slug)

        # Buscar si el producto ya está en el carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'price': precio_producto.precio}
        )

        if not created:
            # Si el producto ya estaba en el carrito, incrementar la cantidad
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            # Asegurarse de que el precio esté correctamente asignado
            cart_item.price = Money(precio_producto.precio.amount, precio_producto.precio_currency)

        # Guardar el item del carrito
        cart_item.save()

        # Redirigir al detalle del producto después de añadir al carrito
        # messages.success(request, f"{product.titulo} añadido al carrito.")
        return redirect('product:producto_detalle', slug=product.slug)


class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el carrito del usuario o de la sesión
        cart = Cart.objects.filter(user=self.request.user).last()
        
        # Si el carrito no existe (fue eliminado), crear uno nuevo
        if not cart:
            cart = Cart.objects.create(user=self.request.user if self.request.user.is_authenticated else None)
            self.request.session['cart_id'] = cart.id

        cart_items = cart.get_cart_items()
        total = sum(item.get_subtotal() for item in cart_items)  # Calcula el total dinámicamente

        context['cart'] = cart
        context['cart_items'] = cart.items.all()
        context['total'] = total

        return context



def update_quantity(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Obtener el carrito del usuario o crear uno si no está registrado
    cart = Cart.get_or_create_cart(request)
    
    # Obtener el item del carrito
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
            # messages.success(request, f'Se ha aumentado la cantidad de {product.titulo}.')
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                # messages.success(request, f'Se ha disminuido la cantidad de {product.titulo}.')
            else:
                cart_item.delete()
                # messages.success(request, f'Se ha eliminado {product.titulo} del carrito.')

    return redirect('cart:cart_detail')


# Vista para eliminar el item del carrito
def remove_item(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # Obtener el carrito del usuario o crear uno si no está registrado
    cart = Cart.get_or_create_cart(request)

    # Eliminar el item del carrito
    CartItem.objects.filter(cart=cart, product=product).delete()
    # messages.success(request, f'Se ha eliminado {product.titulo} del carrito.')

    return redirect('cart:cart_detail')
