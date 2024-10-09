# Explicación breve de dispatch():
# El método dispatch() se encarga de enrutar la solicitud HTTP entrante al método adecuado 
# (por ejemplo, get(), post(), etc.) según el tipo de solicitud. Es útil para agregar lógica
# que se ejecuta antes de procesar cualquier solicitud, sin importar si es GET o POST.

# Explicación breve de form_valid():
# El método form_valid() se llama cuando un formulario ha sido validado correctamente.
# Sobrescribirlo permite agregar lógica adicional (como mensajes o redirecciones) justo después
# de que el formulario sea validado y antes de devolver la respuesta.

from django.shortcuts import render
from allauth.account.views import SignupView, LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages 
from .models import UserProfile

# Create your views here.
class CustomSignupView(SignupView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)

        return response

    def dispatch(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "Registro de usuario éxitoso. ¡Ya te puedes loginar en la web!"
        )
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # print(self.request.POST.get('login'))
        # print(self.request.POST.get('password'))
        # Establecer preferencias del usuario en la sesión
        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)

            # Guardar las preferencias en la sesión
            self.request.session['alergias'] = list(profile.alergias.values_list('nombre', flat=True))
            self.request.session['gustos_hamburguesas'] = list(profile.gustos_hamburguesas.values_list('nombre', flat=True))
            self.request.session['preferencias_dieteticas'] = profile.pais.name if profile.pais else ''

            # Mensaje de bienvenida con el nombre del usuario
            messages.success(self.request, f"Bienvenido de nuevo, {user.username}!")


        except UserProfile.DoesNotExist:
            # Si el perfil no existe, se puede manejar la excepción (aunque no debería suceder si está bien implementado)
            messages.error(self.request, "Parece que hubo un problema al cargar tu perfil.")
        return response


    def dispatch(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "Inicio de sessión con éxito. ¡Ya puedes entrar al admin!"
        )
        return super().dispatch(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        response = super().form_valid(form)

        return response
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(
            self.request,
            "Haz salido del sistema. Te esperamos de vuelta"
        )
        return super().dispatch(request, *args, **kwargs)