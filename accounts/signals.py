from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile
from guardian.shortcuts import assign_perm
from django.db.models.signals import post_delete
from django.dispatch import receiver



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
    if created:
        # Asignar permisos de ver y cambiar al usuario sobre sí mismo
        assign_perm('auth.view_user', instance, instance)
        assign_perm('auth.change_user', instance, instance)

@receiver(post_delete, sender=UserProfile)
def eliminar_imagen_usuario(sender, instance, **kwargs):
    if instance.foto_perfil:
        instance.foto_perfil.delete(False)