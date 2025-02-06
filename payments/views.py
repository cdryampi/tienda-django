import stripe
from django.conf import settings
from django.http import JsonResponse
import json
from django.shortcuts import render

from django.views import View

from cart.models import Cart, CartItem
from payments.models import Order, OrderItem
from product.models import Product

from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import AnonymousUser
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.contrib.auth.models import User
import datetime

"""
Targetas de prueba para Stripe:
5555 5555 5555 4444
4000 0000 0000 9995
4000 0025 0000 3155
4000 0000 0000 0002
CVC: cualquier número de 3 dígitos
Fecha de expiración: cualquier fecha futura
"""

class CheckoutView(View):
    """
    Vista para el checkout de los productos en el carrito. Si no hay productos en el carrito, mostrar un mensaje.
    """
    def get(self, request, *args, **kwargs):
        cart = Cart.get_or_create_cart(request)
        if not cart or not cart.get_cart_items():
            return render(request, "payments/empty_cart.html")  # Mostrar mensaje si el carrito está vacío
        total = sum(item.get_subtotal() for item in cart.get_cart_items())  # Calcula el total dinámicamente
        return render(request, "payments/checkout.html", {"cart": cart, "STRIPE_PUBLIC_KEY":settings.STRIPE_PUBLIC_KEY, "total": total})


class StripeCheckoutView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart.get_or_create_cart(request)
        if not cart or not cart.get_cart_items():
            return JsonResponse({"error": "Carrito vacío o no encontrado"}, status=400)

        # Crear line_items para Stripe Checkout
        line_items = []
        for item in cart.get_cart_items():
            price_amount = int(item.price.amount * 100)  # Convertir a centavos
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
            # 🔥 Crear la sesión de pago con `success_url` ya definido correctamente
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=request.build_absolute_uri("/payments/success/") + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri("/payments/cancel/"),
            )

            # Determinar el usuario (autenticado o anónimo)
            user = request.user if request.user.is_authenticated else User.objects.get_or_create(username="AnonymousUser", defaults={"is_active": False})[0]

            print(f'🛒 Usuario asignado a la orden: {user}')

            # Crear orden en la base de datos
            order = Order.objects.create(
                user=user,
                total_price=cart.get_total_price(),
                payment_id=checkout_session.id,
                is_paid=False,
            )

            # Guardar los productos comprados en OrderItem
            for item in cart.get_cart_items():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_id=item.product.id,
                    quantity=item.quantity,
                    price=item.price  # Se guarda como `MoneyField`
                )

            return JsonResponse({"id": checkout_session.id})

        except stripe.error.StripeError as e:
            return JsonResponse({"error": f"Error con Stripe: {str(e)}"}, status=500)
        except Exception as e:
            return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)


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
        if not session_id:
            return render(request, "payments/cancel.html", {"error": "No se encontró el ID de la sesión"})

        # Buscar la orden en la base de datos
        order = Order.objects.filter(payment_id=session_id).first()
        if not order:
            return render(request, "payments/error.html", {
                "error_message": "No se encontró la orden asociada a este pago. Si el problema persiste, contacta con soporte."
            })

        # Intentar generar la factura y guardarla en la orden
        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)

            if checkout_session.invoice:
                invoice = stripe.Invoice.retrieve(checkout_session.invoice)
                order.recipt_url = invoice.hosted_invoice_url
                order.is_paid = True
                order.json_data = json.loads(str(checkout_session))
                order.save()
                print(f'✅ Factura generada por Stripe: {invoice.hosted_invoice_url}')
            else:
                print('⚠ No se generó factura automática en Stripe.')
                print(f'recuperando la factura de stripe: {checkout_session}')

            

        except stripe.error.StripeError as e:
            return render(request, "payments/error.html", {
                "error_message": f"Error al recuperar la factura de Stripe: {str(e)}"
            })

        # Comprobar si la orden ya fue pagada antes, pero tenemos que configurar el webhook para que Stripe nos avise, cosa que no haremos en este proyecto.
        # lo más que se puede hacer es generar la factura asignando los productos pero se tendría que volver a pagar
        # La factura se puede generar manualmente desde el dashboard de Stripe y enviarla al cliente.
        
        if not order.is_paid:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                if session.payment_status == "paid":
                    order.is_paid = True
                    order.json_data = json.loads(str(checkout_session))
                    order.save()
                else:
                    return render(request, "payments/error.html", {
                        "error_message": "El pago no fue completado con éxito. Si el problema persiste, contacta con soporte."
                    })
            except Exception as e:
                return render(request, "payments/error.html", {
                    "error_message": f"Hubo un error al procesar el pago: {str(e)}"
                })
            else:
                # 🔥 Vaciar el carrito después del pago exitoso
                request.session["cart_id"] = None

        # Extraer datos útiles del JSON
        json_data = order.json_data
        payment_data = {
            "total": json_data["amount_total"] / 100,
            "currency": json_data["currency"].upper(),
            "customer_email": json_data["customer_details"]["email"],
            "payment_intent": json_data["id"],
            "created": datetime.datetime.fromtimestamp(json_data["created"]).strftime("%Y-%m-%d %H:%M:%S"),
            "payment_status": json_data["payment_status"],
            "receipt_url": order.recipt_url if order.recipt_url else None,
        }

        request.session["cart_id"] = Cart.objects.create(user=request.user).id

        return render(request, "payments/success.html", {
            "order": order,
            "payment_data": payment_data
        })
    
class CancelView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "payments/cancel.html")
    

class PaymentDetailView(View):
    
    def post(self, request, *args, **kwargs):
        payment_id = request.POST.get("payment_id")
        # recuperamos el carro anterior
        if not payment_id:
            return render(request, "payments/error.html", {
                "error_message": "No se encontró el ID de pago"
            })
        order = Order.objects.filter(payment_id=payment_id).first()
        if not order:
            return render(request, "payments/error.html", {
                "error_message": "No se encontró la orden solicitada"
            })
        json_data = order.json_data
        
        if not json_data:
            return render(request, "payments/error.html", {
                "error_message": "No se encontraron datos de pago asociados a esta orden"
            })
        products = OrderItem.objects.filter(order=order)
        products_data = [
            {
                "product": product.product,
                "quantity": product.quantity,
                "price": product.price.amount,
                "currency": product.price.currency,
                "url": Product.objects.filter(id=product.product_id).first().imagen.file.url if Product.objects.filter(id=product.product_id).first().imagen else None,
            }
            for product in products
        ]
        

        payment_data = {
            "total": json_data["amount_total"] / 100,
            "currency": json_data["currency"].upper(),
            "customer_email": json_data["customer_details"]["email"],
            "payment_intent": json_data["id"],
            "created": datetime.datetime.fromtimestamp(json_data["created"]).strftime("%Y-%m-%d %H:%M:%S"),
            "payment_status": json_data["payment_status"],
            "receipt_url": order.recipt_url if order.recipt_url else None,
        }
        return render(request, "payments/payment_detail.html", {"order": order, "payment_data": payment_data, "products": products_data})