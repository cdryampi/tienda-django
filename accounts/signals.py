from django.db.models.signals import post_save, post_migrate, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm
from django.contrib.auth.signals import user_logged_in
from .models import UserProfile
from django.contrib import messages
import requests
from django.core.files.base import ContentFile


# Crear perfil de usuario y asignar grupo cuando se crea un nuevo usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.username == 'AnonymousUser':
        return  # No hacer nada para el usuario anónimo

    if created:
        # Crear el perfil si no existe
        user_profile, _ = UserProfile.objects.get_or_create(user=instance)

        # Asignar grupo 'cliente'
        grupo = Group.objects.filter(name='cliente').first()
        if grupo:
            instance.groups.add(grupo)

        # Actualizar el campo 'is_staff'
        instance.is_staff = True
        instance.save(update_fields=['is_staff'])

        # Asignar permisos

        assign_perm('auth.view_user', instance, instance)
        assign_perm('auth.change_user', instance, instance)
        assign_perm('change_userprofile', instance, user_profile)
        assign_perm('view_userprofile', instance, user_profile)

        # Si el usuario fue creado por un registro social y hay imagen en la sesión

        if hasattr(instance, 'socialaccount_set'):
            social_accounts = instance.socialaccount_set.all()
            if social_accounts.exists():
                extra_data = social_accounts.first().extra_data
                if 'picture' in extra_data:
                    image_url = extra_data['picture']['data']['url']

                    # Descargar la imagen desde la URL
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Crear un archivo desde el contenido de la respuesta
                        image_content = ContentFile(response.content)
                        # Guardar la imagen en el campo de imagen del perfil
                        user_profile.foto_perfil.save(f'{instance.username}_profile.jpg', image_content, save=True)

# Eliminar imagen de perfil cuando se elimina un perfil de usuario
@receiver(post_delete, sender=UserProfile)
def eliminar_imagen_usuario(sender, instance, **kwargs):
    if instance.foto_perfil:
        instance.foto_perfil.delete(False)

# Configurar preferencias del usuario en la sesión al iniciar sesión
@receiver(user_logged_in)
def set_user_preferences(sender, user, request, **kwargs):
    if user.is_anonymous:
        return  # No hacer nada para el usuario anónimo

    try:
        # Recuperar el perfil del usuario
        profile = UserProfile.objects.get(user=user)

        # Guardar las alergias y preferencias dietéticas en la sesión
        request.session['alergias'] = list(profile.alergias.values_list('nombre', flat=True))
        request.session['gustos_hamburguesas'] = list(profile.gustos_hamburguesas.values_list('nombre', flat=True))
        request.session['preferencias_dieteticas'] = profile.pais.name if profile.pais else ''
    except UserProfile.DoesNotExist:
        pass

# Crear grupo 'cliente' después de las migraciones
@receiver(post_migrate)
def create_cliente_group(sender, **kwargs):
    Group.objects.get_or_create(name='cliente')
