from django.urls import path
from .views import ProductDetailView, ProductoListView

app_name = 'product'
urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='product_list'),
    path('productos/<slug:slug>/', ProductDetailView.as_view(), name='producto_detalle'),
]
