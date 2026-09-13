import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from usuarios.models import Perfil


class Command(BaseCommand):
    help = (
        "Crea un superusuario (y su Perfil de administrador) usando las "
        "variables de entorno DJANGO_SUPERUSER_USERNAME, "
        "DJANGO_SUPERUSER_EMAIL y DJANGO_SUPERUSER_PASSWORD. "
        "Si el usuario ya existe, no hace nada. Pensado para usarse en el "
        "Build Command de Render, donde no hay acceso a Shell en el plan gratuito."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                "No se definieron DJANGO_SUPERUSER_USERNAME / "
                "DJANGO_SUPERUSER_PASSWORD. Se omite la creación del superusuario."
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f"El usuario '{username}' ya existe, no se vuelve a crear."
            ))
            return

        usuario = User.objects.create_superuser(
            username=username, email=email, password=password
        )
        Perfil.objects.get_or_create(usuario=usuario, defaults={"rol": "administrador"})

        self.stdout.write(self.style.SUCCESS(
            f"Superusuario '{username}' creado correctamente con rol administrador."
        ))
