from django.apps import AppConfig
from django.contrib.auth.models import Group

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self):
        import accounts.signals
        Group.objects.get_or_create(name='cliente')