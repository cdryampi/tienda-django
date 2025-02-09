import json
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from product.models import Product
from .models import Cart, CartItem
from djmoney.money import Money
from core.utils.idioma import IdiomaMixin
from django.utils.html import escape

from django.contrib.auth.models import User

class AddProductToCart(View):
    """
    Vista para añadir, modificar y eliminar un producto al carrito.
    """

    def post(self, request, *args, **kwargs):
        try:
            # ✅ Leer datos JSON desde la solicitud
            data = json.loads(request.body)
            product_id = data.get("product_id")
            quantity = int(data.get("quantity", 1) or 1)  # ✅ Asegurar que `quantity` es un número

            if not product_id:
                return JsonResponse({'status': 'error', 'message': 'No se ha especificado el ID del producto.'}, status=400)

            product = get_object_or_404(Product, id=product_id)

            # ✅ Obtener el usuario anónimo de forma segura
            anominous, _ = User.objects.get_or_create(username='AnonymousUser', defaults={"is_active": False})

            # ✅ Obtener el carrito del usuario o de la sesión
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id).first()
            else:
                cart = None

            if not cart:
                cart = Cart.objects.create(user=request.user if request.user.is_authenticated else anominous)
                request.session['cart_id'] = cart.id

            # ✅ Obtener el idioma actual y moneda preferida
            current_language = IdiomaMixin.get_idioma(self)
            moneda = IdiomaMixin.get_moneda_preferida(current_language)

            # ✅ Obtener el precio en la moneda preferida o el primero disponible
            precio_producto = product.precios.filter(precio_currency=moneda).first() or product.precios.first()

            if not precio_producto or precio_producto.precio.amount is None:
                return JsonResponse({'status': 'error', 'message': 'El producto no tiene un precio válido asignado.'}, status=400)

            # ✅ Buscar o crear el producto en el carrito
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'price': Money(precio_producto.precio.amount, precio_producto.precio_currency)}
            )

            # ✅ Manejar actualización de cantidad
            if data.get('action') == 'update_quantity':
                change = int(data.get("change", 0) or 0)  # ✅ Asegurar que `change` es un número válido
                cart_item.quantity += change

                if cart_item.quantity <= 0:  # ✅ Si llega a 0, eliminar el producto
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'success',
                        'message': f'{product.titulo} eliminado del carrito.',
                        'removed': True,  # ✅ Enviar flag a Vue
                    })

            # ✅ Manejar eliminación de productos
            if data.get('action') == 'remove_from_cart':
                if CartItem.objects.filter(cart=cart, product=product).exists():
                    CartItem.objects.filter(cart=cart, product=product).delete()
                return JsonResponse({
                    'status': 'success',
                    'message': f'{product.titulo} eliminado del carrito.',
                    'removed': True,  # ✅ Enviar flag a Vue
                })

            # ✅ Asegurar que la cantidad nunca sea negativa
            cart_item.quantity = max(1, cart_item.quantity)
            cart_item.save()

            # ✅ Construir la respuesta JSON
            response = {
                'status': 'success',
                'message': f'{product.titulo} añadido al carrito.',
                'cart_item': {
                    'product_id': product.id,
                    'title': product.titulo,
                    'quantity': cart_item.quantity,
                    'price': str(cart_item.price),
                }
            }

            if data.get('action') == 'update_quantity':
                response['message'] = f'La cantidad de {product.titulo} ha sido actualizada.'

            return JsonResponse(response, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al procesar JSON'}, status=400)
        except Exception as e:
            print("❌ Error en la vista:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el carrito del usuario o de la sesión
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).last()
        else:
            cart_id = self.request.session.get('cart_id')
            cart = Cart.objects.filter(id=cart_id).last()
            if not cart:
                cart = Cart.objects.create(user=self.request.user if self.request.user.is_authenticated else None)
                self.request.session['cart_id'] = cart.id

        cart_items = cart.get_cart_items() if cart else []

        # ✅ Serializar los datos con `json.dumps()` correctamente
        cart_items_serialized = [
            {
                "id": item.id,
                "product_id": item.product.id,
                "title": item.product.titulo,
                "image": item.product.imagen.file.url if item.product.imagen else "",
                "price": str(item.price).replace("\xa0", " "),  # ✅ Reemplazamos `\xa0`
                "quantity": item.quantity,
                "subtotal": str(item.get_subtotal()).replace("\xa0", " "),
            }
            for item in cart_items
        ]

        context['cart_items'] = escape(json.dumps(cart_items_serialized, ensure_ascii=False))  # ✅ Escapamos para evitar HTML mal formado
        context['total'] = str(sum(item.get_subtotal() for item in cart_items)).replace("\xa0", " ")

        return context

# Vista para eliminar el item del carrito
def remove_item(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # Obtener el carrito del usuario o crear uno si no está registrado
    cart = Cart.get_or_create_cart(request)

    # Eliminar el item del carrito
    CartItem.objects.filter(cart=cart, product=product).delete()
    # messages.success(request, f'Se ha eliminado {product.titulo} del carrito.')

    return redirect('cart:cart_detail')
