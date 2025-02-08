from django.urls import path
from .views import AddToCartView, CartDetailView, update_quantity, remove_item, addProductToCard

app_name = 'cart'

urlpatterns = [
    path('add/<slug:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('update/<slug:slug>/', update_quantity, name='update_quantity'),
    path('remove/<slug:slug>/', remove_item, name='remove_item'),
    path('detail/', CartDetailView.as_view(), name='cart_detail'),
    path('add-to-cart/', addProductToCard.as_view(), name='add-to-cart'),
]
