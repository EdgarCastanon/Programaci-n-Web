# Práctica 04 — Flask + CSS + PostgreSQL

## Objetivo
Enviar los datos capturados en el formulario (nombre, pasatiempos, qué te gusta hacer — igual
que en las Prácticas 01, 02 y 03) y almacenarlos en una base de datos **PostgreSQL**, primero en
una instancia local y después en una instancia en la nube.

## Estructura del proyecto
```
practica_04_Flask_CSS_Postgres/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   ├── saludar.html
│   └── listar_alumnos.html
│
└── static/
    └── css/
        └── estilos.css
```

## Variables de entorno
| Variable            | Descripción                                  |
|---------------------|-----------------------------------------------|
| POSTGRES_HOST       | Dirección del servidor PostgreSQL             |
| POSTGRES_PORT       | Puerto (5432 por defecto)                     |
| POSTGRES_USER       | Usuario de PostgreSQL                         |
| POSTGRES_PASSWORD   | Contraseña de PostgreSQL                      |
| POSTGRES_DATABASE   | Nombre de la base de datos                    |
| POSTGRES_SSL_CA     | Ruta al certificado SSL (solo nube, opcional) |

## Ejecución local (con PostgreSQL instalado en Windows)
1. Instalar PostgreSQL (postgresql.org) y anotar la contraseña que se asigne al usuario `postgres`.
2. Copiar `.env.example` a `.env` y completar `POSTGRES_PASSWORD` con esa contraseña.
3. Crear el entorno virtual e instalar dependencias:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```
   python app.py
   ```
5. Abrir en el navegador:
   - http://127.0.0.1:5000
   - http://127.0.0.1:5000/alumnos

La aplicación crea automáticamente la base de datos y la tabla `alumnos` si no existen.

## Despliegue en la nube (Render + Aiven PostgreSQL)
1. Crear una base de datos PostgreSQL gratuita en Aiven (aiven.io).
2. En Render, configurar las variables de entorno con los datos que da Aiven
   (host, puerto, usuario, contraseña, nombre de base de datos) y subir el certificado `ca.pem`
   como Secret File.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
