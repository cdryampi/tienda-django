from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm
from .models import Cart, CartItem
from django.contrib.auth.models import User, Group

# Asignar permisos al usuario cuando se crea el carrito
@receiver(post_save, sender=Cart)
def assign_cart_permissions(sender, instance, created, **kwargs):
    if created and instance.user and instance.user.is_authenticated:
        # Solo asignamos permisos si el carrito pertenece a un usuario autenticado
        assign_perm('view_cart', instance.user, instance)
        assign_perm('change_cart', instance.user, instance)
        assign_perm('delete_cart', instance.user, instance)
    elif instance.user is None:
        # Para carritos no asignados, asegurarse de que al menos existan permisos de sesión si se desea
        pass
    
# Asignar permisos al grupo 'admin' y superusuarios cuando se crea un carrito
@receiver(post_save, sender=Cart)
def assign_cart_permissions_to_admin_and_superuser(sender, instance, created, **kwargs):
    if created:
        try:
            # Asigna permisos al grupo 'admin'
            admin_group = Group.objects.get(name='admin')
            assign_perm('view_cart', admin_group, instance)
            assign_perm('change_cart', admin_group, instance)
            assign_perm('delete_cart', admin_group, instance)  # Permiso para eliminar

            # Asigna permisos a todos los superusuarios
            superusers = User.objects.filter(is_superuser=True)
            for superuser in superusers:
                assign_perm('view_cart', superuser, instance)
                assign_perm('change_cart', superuser, instance)
                assign_perm('delete_cart', superuser, instance)  # Permiso para eliminar
        except Group.DoesNotExist:
            pass  # Si el grupo 'admin' no existe, lo ignoramos o podríamos crearlo

# Asignar permisos al grupo 'admin' y superusuarios para los CartItem cuando se crea
@receiver(post_save, sender=CartItem)
def assign_cartitem_permissions_to_admin_and_superuser(sender, instance, created, **kwargs):
    if created:
        try:
            # Asigna permisos al grupo 'admin'
            admin_group = Group.objects.get(name='admin')
            assign_perm('view_cartitem', admin_group, instance)
            assign_perm('change_cartitem', admin_group, instance)
            assign_perm('delete_cartitem', admin_group, instance)

            # Asigna permisos a todos los superusuarios
            superusers = User.objects.filter(is_superuser=True)
            for superuser in superusers:
                assign_perm('view_cartitem', superuser, instance)
                assign_perm('change_cartitem', superuser, instance)
                assign_perm('delete_cartitem', superuser, instance)
        except Group.DoesNotExist:
            pass

# Eliminar permisos cuando se elimina el carrito
@receiver(post_delete, sender=Cart)
def remove_cart_permissions(sender, instance, **kwargs):
    if instance.user:
        # Eliminar permisos de ver, cambiar y eliminar el carrito al usuario
        remove_perm('view_cart', instance.user, instance)
        remove_perm('change_cart', instance.user, instance)
        remove_perm('delete_cart', instance.user, instance)

# Asociar carrito de la sesión al usuario al hacer login
@receiver(user_logged_in)
def assign_cart_to_user(sender, user, request, **kwargs):
    cart_id = request.session.get('cart_id')
    if cart_id:
        try:
            # Si hay un carrito en la sesión, lo asignamos al usuario
            cart = Cart.objects.get(id=cart_id, user__isnull=True)
            cart.user = user
            cart.save()

            # Asignar permisos al usuario autenticado
            assign_perm('view_cart', user, cart)
            assign_perm('change_cart', user, cart)
            assign_perm('delete_cart', user, cart)

            # Eliminar el carrito de la sesión ya que se ha asociado al usuario
            del request.session['cart_id']
        except Cart.DoesNotExist:
            pass
