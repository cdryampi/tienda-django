from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from guardian.admin import GuardedModelAdmin
from .models import UserProfile

# Registrar el perfil en el admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfiles de Usuario'

# Personalizar el admin de User
class CustomUserAdmin(GuardedModelAdmin, UserAdmin):
    # Limitar los usuarios que se muestran en la lista
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    # Restringir los permisos de cambio
    def has_change_permission(self, request, obj=None):
        has_perm = super().has_change_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None:
            return obj == request.user
        return True

    # Evitar que puedan eliminar usuarios
    def has_delete_permission(self, request, obj=None):
        return False

    # Evitar que puedan agregar usuarios
    def has_add_permission(self, request):
        return False

    # Limitar los campos que pueden editar
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        return [
            (None, {'fields': ('username', 'password')}),
            ('Información personal', {'fields': ('first_name', 'last_name', 'email',)}),
            
        ]

    # Hacer que ciertos campos sean de solo lectura
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ['username', 'is_staff', 'is_superuser', 'user_permissions', 'groups', 'last_login', 'date_joined']


class UserProfileAdmin(admin.ModelAdmin):
    # Opcional: Define los campos que quieres mostrar en la lista
    list_display = ('user',)
    verbose_name = 'Foto de perfil'
    # Limita los perfiles visibles al del usuario actual
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    # Permite que los usuarios solo puedan cambiar su propio perfil
    def has_change_permission(self, request, obj=None):
        has_perm = super().has_change_permission(request, obj)
        if not has_perm:
            return False
        if obj is None:
            return True  # Permite acceder a la lista (filtrada en get_queryset)
        return obj.user == request.user

    # Evita que los usuarios puedan eliminar perfiles
    def has_delete_permission(self, request, obj=None):
        return False

    # Evita que los usuarios puedan agregar nuevos perfiles
    def has_add_permission(self, request):
        return False

    # Opcional: Limita los campos que pueden editar
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        # Por ejemplo, hacer el campo 'user' de solo lectura
        return ['user']

admin.site.register(UserProfile, UserProfileAdmin)

# Registrar los cambios en el admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
