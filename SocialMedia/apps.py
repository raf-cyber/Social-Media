from django.apps import AppConfig


class SocialmediaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SocialMedia"

class SocialmediaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SocialMedia"

    def ready(self):
        import SocialMedia.signals