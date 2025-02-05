import stripe
from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render

from django.views import View

from cart.models import Cart, CartItem
from payments.models import Order, OrderItem
from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import AnonymousUser
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.contrib.auth.models import User


class CheckoutView(View):
    """
    Vista para el checkout de los productos en el carrito. Si no hay productos en el carrito, mostrar un mensaje.
    """
    def get(self, request, *args, **kwargs):
        cart = Cart.get_or_create_cart(request)
        if not cart or not cart.get_cart_items():
            return render(request, "payments/empty_cart.html")  # Mostrar mensaje si el carrito está vacío

        return render(request, "payments/checkout.html", {"cart": cart, "STRIPE_PUBLIC_KEY":settings.STRIPE_PUBLIC_KEY})



class StripeCheckoutView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart.get_or_create_cart(request)
        if not cart:
            return JsonResponse({"error": "Carrito no encontrado"}, status=400)

        line_items = []
        for item in cart.get_cart_items():
            price_amount = int(item.price.amount * 100)
            currency = item.price.currency

            line_items.append({
                "price_data": {
                    "currency": currency,
                    "unit_amount": price_amount,
                    "product_data": {"name": item.product.titulo},
                },
                "quantity": item.quantity,
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="http://127.0.0.1:8000/payments/success/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8000/payments/cancel/",
            )
            
            # Guardar la orden en la base de datos, si no hay usuario, asignarlo a AnonymousUser
            print(f'El usuario es: {cart.user}')
            anonymous_user, created = User.objects.get_or_create(username="AnonymousUser", defaults={"is_active": False})
            user = cart.user if cart.user and cart.user.is_authenticated else anonymous_user
            order = Order.objects.create(
                user=user,
                total_price=cart.get_total_price(),
                payment_id=checkout_session.id,
                is_paid=False,
            )

            # Guardar los productos en OrderItem
            for item in cart.get_cart_items():
                OrderItem.objects.create(
                    order=order,
                    product=item.product.titulo,
                    quantity=item.quantity,
                    price=item.price
                )

            return JsonResponse({"id": checkout_session.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt  # Stripe enviará datos externos, no podemos usar CSRF
def stripe_webhook(request):
    """
    Manejar los eventos de Stripe https://docs.stripe.com/webhooks
    """
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_KEY
        )
    except ValueError:
        return HttpResponse(status=400)  # Payload inválido
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Firma inválida

    # Manejar el evento de pago exitoso
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order = Order.objects.filter(payment_id=session["id"]).first()
        if order:
            order.is_paid = True
            order.save()

    return HttpResponse(status=200)


class OrderListView(LoginRequiredMixin, ListView):
    """
    Vista para listar las ordenes de un usuario
    """
    model = Order
    template_name = "payments/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
    


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        order = Order.objects.filter(payment_id=session_id).first()
        return render(request, "payments/success.html", {"order": order})

class CancelView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payments/cancel.html")