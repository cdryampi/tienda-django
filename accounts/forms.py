# accounts/forms.py
from django import forms
from django_countries.fields import CountryField
from .models import UserProfile
from core.models import BurgerType, Allergy


class CustomSignupForm(forms.Form):
    # Definición de los campos adicionales
    foto_perfil = forms.ImageField(required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=255, required=False)
    ciudad = forms.CharField(max_length=100, required=False)
    codigo_postal = forms.CharField(max_length=10, required=False)
    pais = CountryField().formfield(label='País', required=False)
    suscripcion_boletin = forms.BooleanField(required=False)
    gustos_hamburguesas = forms.ModelMultipleChoiceField(
        queryset=BurgerType.objects.all(),  # Reemplaza con el queryset de tus hamburguesas
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    alergias = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),  # Reemplaza con el queryset de tus alergias
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gustos_hamburguesas'].queryset = BurgerType.objects.all()  # Ajusta según tu modelo
        self.fields['alergias'].queryset = Allergy.objects.all()  # Ajusta según tu modelo

    def signup(self, request, user):
        # Crear o actualizar el perfil de usuario asociado
        print("Ejecutando el método signup para actualizar el perfil de usuario.")
        try:
            # Obtener el perfil existente o crearlo si no existe (aunque debería ya estar creado por la señal)
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Actualizar los campos del perfil con los datos adicionales del formulario
            user_profile.foto_perfil = self.cleaned_data.get('foto_perfil')
            user_profile.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
            user_profile.telefono = self.cleaned_data.get('telefono')
            user_profile.direccion = self.cleaned_data.get('direccion')
            user_profile.ciudad = self.cleaned_data.get('ciudad')
            user_profile.codigo_postal = self.cleaned_data.get('codigo_postal')
            user_profile.pais = self.cleaned_data.get('pais')
            user_profile.suscripcion_boletin = self.cleaned_data.get('suscripcion_boletin')

            # Guardar los cambios del perfil antes de asignar campos ManyToMany
            user_profile.save()

            # Asignar campos ManyToMany (gustos de hamburguesas y alergias)
            gustos = self.cleaned_data.get('gustos_hamburguesas')
            alergias = self.cleaned_data.get('alergias')
            print(gustos)
            print(alergias)
            if gustos:
                user_profile.gustos_hamburguesas.set(gustos)
            if alergias:
                user_profile.alergias.set(alergias)

            print("Perfil de usuario actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar el perfil de usuario: {e}")
