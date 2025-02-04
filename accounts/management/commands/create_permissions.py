from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.apps import apps

class Command(BaseCommand):
    help = "Crea todos los permisos necesarios para los modelos en todas las aplicaciones."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🛠 Iniciando creación de permisos..."))

        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                content_type, _ = ContentType.objects.get_or_create(app_label=app_config.label, model=model.__name__.lower())

                # Lista de permisos estándar
                permisos = [
                    ("add", f"Can add {model.__name__}"),
                    ("change", f"Can change {model.__name__}"),
                    ("delete", f"Can delete {model.__name__}"),
                    ("view", f"Can view {model.__name__}")
                ]

                for codename, nombre in permisos:
                    permiso, creado = Permission.objects.get_or_create(
                        codename=f"{codename}_{model.__name__.lower()}",
                        content_type=content_type,
                        defaults={"name": nombre}
                    )
                    if creado:
                        self.stdout.write(self.style.SUCCESS(f"✅ Permiso creado: {permiso.codename}"))
                    else:
                        self.stdout.write(f"🔄 Permiso ya existente: {permiso.codename}")

        self.stdout.write(self.style.SUCCESS("🎉 Todos los permisos han sido creados correctamente."))
