from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = _("User Management")

    def ready(self):
        # Import signals to ensure they are registered
        import apps.users.signals
        
        # Optionally, you can connect other signals here, like post_migrate if needed
        # post_migrate.connect(your_function, sender=self.get_model('YourModel'))
