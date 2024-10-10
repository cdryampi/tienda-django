# accounts/adapters/custom_account_adapter.py
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Permitir o restringir el registro
        return True

    def get_login_redirect_url(self, request):
        # Redirigir al usuario después del login
        return '/'
