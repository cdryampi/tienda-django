from django.shortcuts import render
from allauth.account.views import SignupView, LoginView, LogoutView
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
class CustomSignupView(SignupView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        print("LLego")
        return response

class CustomLoginView(LoginView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        print(self.request.POST.get('login'))
        print(self.request.POST.get('password'))
        return response

class CustomLogoutView(LogoutView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)

        return response