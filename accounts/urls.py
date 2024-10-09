from django.urls import path, include
from .views import CustomLoginView, CustomSignupView, CustomLogoutView

from allauth.account import views as allauth_views


urlpatterns = [
    path('', include('allauth.urls')),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
]
