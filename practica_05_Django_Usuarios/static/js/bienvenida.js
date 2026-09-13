// ==========================================================
// Este script identifica el perfil (rol) del usuario que inició
// sesión y muestra un mensaje de bienvenida distinto según su rol.
// El rol viene desde Django, guardado en el atributo data-rol
// del contenedor #bienvenida (ver home.html).
// ==========================================================

document.addEventListener("DOMContentLoaded", function () {
    var contenedor = document.getElementById("bienvenida");
    var mensaje = document.getElementById("mensaje-rol");

    if (!contenedor || !mensaje) {
        return;
    }

    var rol = contenedor.dataset.rol;
    var usuario = contenedor.dataset.usuario;

    var textos = {
        administrador: "Tienes acceso completo para administrar los usuarios del sistema.",
        empleado: "Bienvenido, puedes consultar la información asignada a tu perfil.",
        cliente: "Bienvenido, este es tu panel como cliente.",
    };

    var colores = {
        administrador: "#f8d7da",
        empleado: "#fff3cd",
        cliente: "#d4edda",
    };

    mensaje.textContent = textos[rol] || ("Bienvenido, " + usuario + ".");
    mensaje.style.background = colores[rol] || "#eef2f7";
});
