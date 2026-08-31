# Práctica 03 — Flask + CSS + MySQL

## Objetivo
Enviar los datos capturados en el formulario (nombre, pasatiempos, qué te gusta hacer — igual
que en las Prácticas 01 y 02) y almacenarlos en una base de datos **MySQL**, primero en una
instancia local y después en una instancia en la nube.

## Estructura del proyecto
```
practica_03_Flask_CSS_MySQL/
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
La conexión a MySQL se configura con variables de entorno (nunca se escriben usuario/contraseña
directamente en el código):

| Variable        | Descripción                                  |
|-----------------|-----------------------------------------------|
| MYSQL_HOST      | Dirección del servidor MySQL                  |
| MYSQL_PORT      | Puerto (3306 por defecto)                     |
| MYSQL_USER      | Usuario de MySQL                              |
| MYSQL_PASSWORD  | Contraseña de MySQL                           |
| MYSQL_DATABASE  | Nombre de la base de datos                    |
| MYSQL_SSL_CA    | Ruta al certificado SSL (solo nube, opcional) |

## Ejecución local (con XAMPP)
1. Instalar XAMPP y arrancar el módulo MySQL.
2. Copiar `.env.example` a `.env` (los valores por defecto ya sirven para XAMPP).
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

## Despliegue en la nube (Render + Aiven MySQL)
1. Crear una base de datos MySQL gratuita en Aiven (aiven.io).
2. En Render, configurar las variables de entorno con los datos que da Aiven
   (host, puerto, usuario, contraseña, nombre de base de datos) y subir el certificado `ca.pem`.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
