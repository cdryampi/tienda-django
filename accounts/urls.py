from django.urls import path, include
from .views import CustomLoginView
from .views import CustomSignupView

from allauth.account import views as allauth_views


urlpatterns = [
    path('', include('allauth.urls')),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
]
