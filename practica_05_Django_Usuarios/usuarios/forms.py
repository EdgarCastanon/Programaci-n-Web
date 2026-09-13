from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    rol = forms.ChoiceField(choices=Perfil.ROLES, label="Rol del usuario")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "rol"]
