# Práctica 02 — Flask + Jinja + CSS + SQLite

## Objetivo
Capturar datos de un alumno mediante un formulario HTML con estilos CSS, almacenarlos en una
base de datos SQLite y permitir consultarlos y listarlos utilizando una plantilla Jinja.

## Estructura del proyecto
```
practica_02_FlaskJingaCSS_BD/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── database/
│   └── practica.db
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

## Rutas de la aplicación
| Ruta       | Función            | Plantilla             | Propósito                     |
|------------|--------------------|-----------------------|--------------------------------|
| /          | inicio()           | index.html            | Mostrar formulario             |
| /saludar   | f_saludar()        | saludar.html          | Guardar y confirmar registro   |
| /alumnos   | listar_alumnos()   | listar_alumnos.html   | Consultar y mostrar alumnos    |

## Ejecución local
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Luego abrir en el navegador:
- http://127.0.0.1:5000
- http://127.0.0.1:5000/alumnos

## Despliegue en Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
