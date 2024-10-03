from django.urls import path
from .views import ProductoDetailView1, ProductoDetailView2, ProductoDetailView3, ProductosList

app_name = 'product'
urlpatterns = [
    path('producto1/', ProductoDetailView1.as_view(), name='producto1'),
    path('producto2/', ProductoDetailView2.as_view(), name='producto2'),
    path('producto3/', ProductoDetailView3.as_view(), name='producto3'),
    path('', ProductosList.as_view(), name='product_list')
]
