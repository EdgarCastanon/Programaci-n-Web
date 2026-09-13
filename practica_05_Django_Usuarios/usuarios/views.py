from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistroForm
from .models import Perfil


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(usuario=usuario, rol=form.cleaned_data["rol"])
            messages.success(request, "Usuario registrado correctamente. Ya puedes iniciar sesión.")
            return redirect("login")
    else:
        form = RegistroForm()

    return render(request, "usuarios/registro.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            auth_login(request, usuario)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "usuarios/login.html")


def cerrar_sesion(request):
    auth_logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")


def _es_administrador(request, perfil_actual):
    """Un usuario cuenta como administrador si su Perfil dice 'administrador'
    o si es superusuario/staff de Django (por ejemplo el creado con
    createsuperuser, que no tiene Perfil propio)."""
    if request.user.is_superuser or request.user.is_staff:
        return True
    return bool(perfil_actual and perfil_actual.rol == "administrador")


@login_required(login_url="login")
def home(request):
    perfil = Perfil.objects.filter(usuario=request.user).first()
    if perfil:
        rol = perfil.rol
    elif request.user.is_superuser:
        rol = "administrador"
    else:
        rol = "sin_perfil"
    return render(request, "usuarios/home.html", {"rol": rol})


@login_required(login_url="login")
def lista_usuarios(request):
    perfil_actual = Perfil.objects.filter(usuario=request.user).first()
    if not _es_administrador(request, perfil_actual):
        messages.error(request, "No tienes permiso para ver esta sección.")
        return redirect("home")

    usuarios = Perfil.objects.select_related("usuario").all().order_by("usuario__id")
    return render(request, "usuarios/lista_usuarios.html", {"usuarios": usuarios})


@login_required(login_url="login")
def eliminar_usuario(request, usuario_id):
    perfil_actual = Perfil.objects.filter(usuario=request.user).first()
    if not _es_administrador(request, perfil_actual):
        messages.error(request, "No tienes permiso para esta acción.")
        return redirect("home")

    usuario = get_object_or_404(User, id=usuario_id)

    if usuario == request.user:
        messages.error(request, "No puedes eliminar tu propio usuario mientras tienes la sesión activa.")
        return redirect("lista_usuarios")

    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("lista_usuarios")
