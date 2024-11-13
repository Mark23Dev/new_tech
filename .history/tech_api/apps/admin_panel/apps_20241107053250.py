from django.apps import AppConfig

class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'
    verbose_name = "Admin Panel"

    def ready(self):
        """
        This method is called when the app is ready. You can perform app-specific
        startup actions here, such as registering signals or custom checks.
        """
        # Import signals or any other startup code here if necessary
        try:
            import admin_panel.signals  # noqa: F401 (Ignore linting error if not used in this file)
        except ImportError:
            pass
