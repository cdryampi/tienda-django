from django.urls import path
from .views import HomeView, StripeFindDetailView
app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stripe/', StripeFindDetailView.as_view(), name='stripe'),
]