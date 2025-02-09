from django.urls import path
from .views import CartDetailView, remove_item, AddProductToCart

app_name = 'cart'

urlpatterns = [
    path('remove/<slug:slug>/', remove_item, name='remove_item'),
    path('detail/', CartDetailView.as_view(), name='cart_detail'),
    path('add-to-cart/', AddProductToCart.as_view(), name='add_to_cart'),
]
