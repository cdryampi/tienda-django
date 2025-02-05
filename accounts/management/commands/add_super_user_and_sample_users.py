from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Crea un superusuario y usuarios de muestra si no existen'

    def handle(self, *args, **kwargs):
        
        self.stdout.write(self.style.SUCCESS('Iniciando la creación de usuarios...'))

        self.stdout.write(self.style.SUCCESS('Creando permisos...'))

        call_command('create_permissions')
        
        User = get_user_model()
        # Crear el grupo 'cliente' si no existe
        cliente_group, created = Group.objects.get_or_create(name='cliente')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "cliente" creado.'))
        else:
            self.stdout.write(self.style.SUCCESS('Grupo "cliente" ya existe.'))

        # Crear el superusuario 'admin' si no existe
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            # Crear el perfil de superusuario si no existe
            #UserProfile.objects.get_or_create(user=admin_user)
            admin_user.groups.add(cliente_group)
            self.stdout.write(self.style.SUCCESS('Superusuario "admin" creado exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario "admin" ya existe.'))
            
            # Verificar si el perfil ya existe, si no, crearlo
            admin_user = User.objects.get(username='admin')
            UserProfile.objects.get_or_create(user=admin_user)

        # Crear usuarios de muestra
        sample_users = [
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1'},
            {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2'},
            {'username': 'user3', 'email': 'user3@example.com', 'password': 'password3'},
            {'username': 'AnonymousUser', 'email': 'anonymoususer@example.com', 'password': 'password4'},
        ]

        for user_data in sample_users:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                # Crear el perfil de usuario
                UserProfile.objects.get_or_create(user=user)
                
                # Añadir al grupo 'cliente'
                user.groups.add(cliente_group)
                self.stdout.write(self.style.SUCCESS(f"Usuario '{user_data['username']}' creado exitosamente."))
            else:
                self.stdout.write(self.style.WARNING(f"El usuario '{user_data['username']}' ya existe."))

                # Verificar si el perfil ya existe, si no, crearlo
                user = User.objects.get(username=user_data['username'])
                UserProfile.objects.get_or_create(user=user)
