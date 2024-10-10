from django.db.models.signals import post_save, post_migrate, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm
from django.contrib.auth.signals import user_logged_in
from .models import UserProfile
from django.contrib import messages

# Crear perfil de usuario y asignar grupo cuando se crea un nuevo usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.username == 'AnonymousUser':
        return  # No hacer nada para el usuario anónimo

    if created:
        # Crear perfil de usuario
        profile, _ = UserProfile.objects.get_or_create(user=instance)

        # Asignar grupo 'cliente'
        grupo, _ = Group.objects.get_or_create(name='cliente')
        instance.groups.add(grupo)

        # Asignar permisos de ver y cambiar el perfil al usuario
        assign_perm('change_userprofile', instance, profile)
        assign_perm('view_userprofile', instance, profile)

        # Actualizar el campo 'is_staff' (opcional)
        instance.is_staff = True
        instance.save(update_fields=['is_staff'])

        # Asignar permisos sobre el propio usuario
        assign_perm('auth.view_user', instance, instance)
        assign_perm('auth.change_user', instance, instance)

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
