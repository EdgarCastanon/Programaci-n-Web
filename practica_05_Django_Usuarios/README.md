# Práctica 05 — Administrador de usuarios con Django

## Objetivo
Crear un administrador de usuarios empleando Django (Modelos, Vistas y Templates) y SQLite3
como base de datos nativa de Python. Incluye registro, inicio de sesión, roles de usuario
(Administrador, Empleado, Cliente), un mensaje de bienvenida personalizado con JavaScript según
el perfil, y una sección de gestión de usuarios solo visible para el Administrador.

## Estructura del proyecto
```
practica_05_Django_Usuarios/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── config/                 (proyecto Django)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── usuarios/                (app Django)
│   ├── models.py            (modelo Perfil: rol de cada usuario)
│   ├── forms.py              (formulario de registro)
│   ├── views.py               (lógica: registro, login, logout, home, gestión)
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── templates/usuarios/
│       ├── home.html
│       ├── login.html
│       ├── registro.html
│       └── lista_usuarios.html
│
├── templates/
│   └── base.html             (plantilla base con barra de navegación)
│
└── static/
    ├── css/estilos.css
    └── js/bienvenida.js       (mensaje de bienvenida según el rol)
```

## Rutas de la aplicación
| Ruta                          | Vista              | Descripción                                    |
|--------------------------------|--------------------|--------------------------------------------------|
| /                              | home               | Página de bienvenida (requiere sesión iniciada)  |
| /registro/                     | registro           | Alta de un nuevo usuario con su rol              |
| /login/                        | iniciar_sesion     | Inicio de sesión                                 |
| /logout/                       | cerrar_sesion      | Cierre de sesión                                 |
| /usuarios/                     | lista_usuarios     | Lista de usuarios (solo Administrador)           |
| /usuarios/eliminar/<id>/       | eliminar_usuario   | Elimina un usuario (solo Administrador)          |
| /admin/                        | —                  | Panel de administración nativo de Django         |

## Ejecución local
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir en el navegador: http://127.0.0.1:8000

## Despliegue en Render
- Build Command:
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- Start Command:
  ```
  gunicorn config.wsgi
  ```
- Variables de entorno necesarias: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
- Nota: SQLite en el plan gratuito de Render no es permanente entre reinicios del servicio.
