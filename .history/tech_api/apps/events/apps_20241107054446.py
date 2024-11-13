from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.events'  # Adjust if your app's path is different
    verbose_name = "Events"  # This is optional and can be customized

    def ready(self):
        # Import signals here if you have any in the events app
        import apps.events.signals  # Ensure signals are defined in events/signals.py
