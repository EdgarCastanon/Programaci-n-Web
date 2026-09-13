from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/eliminar/<int:usuario_id>/", views.eliminar_usuario, name="eliminar_usuario"),
]
