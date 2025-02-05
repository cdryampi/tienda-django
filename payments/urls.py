from django.urls import path
from payments.views import StripeCheckoutView, stripe_webhook, OrderListView, CheckoutView, SuccessView, CancelView

app_name = 'payments'

urlpatterns = [
    path("create-checkout-session/", StripeCheckoutView.as_view(), name="create_checkout_session"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
]