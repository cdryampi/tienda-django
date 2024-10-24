from django.urls import path
from .views import ProductDetailView, ProductoListView

app_name = 'product'
urlpatterns = [
    path('', ProductoListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='producto_detalle'),
]
