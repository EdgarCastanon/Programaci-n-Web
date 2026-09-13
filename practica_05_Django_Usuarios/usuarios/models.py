from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """
    Extiende al usuario nativo de Django (User) agregando un rol.
    Esto permite distinguir entre Administrador, Empleado y Cliente
    sin tener que crear un sistema de autenticación desde cero.
    """

    ROLES = [
        ("administrador", "Administrador"),
        ("empleado", "Empleado"),
        ("cliente", "Cliente"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=20, choices=ROLES, default="cliente")

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"
