from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"


from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        import os
        from django.contrib.auth import get_user_model
        if os.environ.get("CREATE_SUPERUSER") == "True":
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="sakthi",
                    email="admin@example.com",
                    password="sakthi"
                )

