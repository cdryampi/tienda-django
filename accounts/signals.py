# Explicación breve del decorador @receiver:
# El decorador @receiver se utiliza para conectar una función a un signal específico en Django.
# Esto significa que la función decorada "escucha" cuando ese signal es disparado, como por ejemplo cuando un usuario inicia sesión.
# Al decorarla con @receiver, la función se ejecutará automáticamente al producirse el evento indicado por el signal.
# Esto facilita la ejecución de lógica adicional (como establecer preferencias del usuario) sin tener que modificar las vistas directamente.

from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile
from guardian.shortcuts import assign_perm
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib import messages 

from django.contrib.auth.signals import user_logged_in
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.signals import social_account_updated
from allauth.socialaccount.signals import social_account_removed


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Solo crea el perfil si no existe
        UserProfile.objects.get_or_create(user=instance)

        # Asignar grupo 'cliente'
        grupo = Group.objects.filter(name='cliente').first()
        if grupo:
            instance.groups.add(grupo)

        # Actualizar el campo 'is_staff'
        instance.is_staff = True
        instance.save(update_fields=['is_staff'])

        print(f"grupo asignado a: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Verificar si el perfil ya existe o crearlo si no existe
    user_profile, created = UserProfile.objects.get_or_create(user=instance)

    # Si el perfil ya existía, simplemente se actualiza
    user_profile.save()

@receiver(post_save, sender=UserProfile)
def assign_profile_permissions(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        assign_perm('change_userprofile', user, instance)
        assign_perm('view_userprofile', user, instance)

@receiver(post_save, sender=User)
def assign_user_permissions(sender, instance, created, **kwargs):
    if instance.username == 'AnonymousUser':
        return
    
    if created:
        # Asignar permisos de ver y cambiar al usuario sobre sí mismo
        assign_perm('auth.view_user', instance, instance)
        assign_perm('auth.change_user', instance, instance)

@receiver(post_delete, sender=UserProfile)
def eliminar_imagen_usuario(sender, instance, **kwargs):
    if instance.foto_perfil:
        instance.foto_perfil.delete(False)

@receiver(user_logged_in)
def set_user_preferences(sender, user, request, **kwargs):
    try:
        # Recuperar el perfil del usuario
        profile = UserProfile.objects.get(user=user)
        
        # Guardar las alergias y preferencias dietéticas en la sesión
        request.session['alergias'] = list(profile.alergias.values_list('nombre', flat=True))
        request.session['gustos_hamburguesas'] = list(profile.gustos_hamburguesas.values_list('nombre', flat=True))
        request.session['preferencias_dieteticas'] = profile.pais.name if profile.pais else ''
    except UserProfile.DoesNotExist:
        # Si el perfil no existe, no se hace nada
        pass

@receiver(post_migrate)
def create_cliente_group(sender, **kwargs):
    Group.objects.get_or_create(name='cliente')


##login con facebook

# Signal para crear el perfil del usuario después del inicio de sesión social exitoso
@receiver(social_account_added)
def create_or_update_profile_after_social_login(request, sociallogin, **kwargs):
    user = sociallogin.user

    # Asegúrate de que el usuario está guardado antes de crear o actualizar el perfil
    if not user.pk:
        user.save()

    # Crea o actualiza el perfil del usuario
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Datos adicionales de Facebook
    extra_data = sociallogin.account.extra_data
    if 'first_name' in extra_data:
        user.first_name = extra_data['first_name']
    if 'last_name' in extra_data:
        user.last_name = extra_data['last_name']
    if 'picture' in extra_data:
        # Guardar la URL de la foto de perfil
        profile.foto_perfil_url = extra_data['picture']['data']['url']

    # Guarda los cambios realizados
    user.save()
    profile.save()

    # Mensaje para indicar al usuario que la cuenta ha sido conectada con éxito
    messages.success(request, "Has conectado exitosamente tu cuenta de Facebook.")

# Signal para acciones adicionales antes del login
@receiver(pre_social_login)
def before_social_login(request, sociallogin, **kwargs):
    # Realiza acciones antes de que el login se procese completamente
    profile_data = sociallogin.account.extra_data  # Datos adicionales del perfil del proveedor social
    if profile_data.get('email'):
        print(f"Email del usuario autenticado: {profile_data['email']}")
    # Lógica personalizada: Podrías verificar si hay un usuario con este correo

# Signal para actualizar el perfil cuando la cuenta social es actualizada
@receiver(social_account_updated)
def after_social_account_updated(request, sociallogin, **kwargs):
    # Realiza acciones después de que una cuenta social haya sido actualizada
    updated_data = sociallogin.account.extra_data
    messages.info(request, "Se ha actualizado la información de tu cuenta social.")

# Signal para manejar cuando un usuario elimina una cuenta social
@receiver(social_account_removed)
def after_social_account_removed(request, socialaccount, **kwargs):
    # Realiza acciones después de que se elimine una cuenta social
    messages.warning(request, f"Has desconectado tu cuenta de {socialaccount.provider}.")