from flask import Flask, render_template, request
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (solo en local)
load_dotenv()

app = Flask(__name__)

# ==========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# Estas variables cambian según el entorno:
#   - En LOCAL se leen desde el archivo .env
#   - En RENDER (nube) se configuran en el Dashboard, en "Environment"
# ==========================================================
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
DB_NAME = os.environ.get("POSTGRES_DATABASE", "practica_04")
DB_SSL_CA = os.environ.get("POSTGRES_SSL_CA", "")  # ruta al certificado, solo para la nube


def obtener_conexion(nombre_bd=None):
    """Crea una conexión a PostgreSQL. Si no se indica nombre_bd, se usa
    la base de datos configurada en DB_NAME."""
    parametros = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "dbname": nombre_bd if nombre_bd else DB_NAME,
    }

    # Si se definió un certificado SSL (necesario para bases de datos en la nube
    # como Aiven), se agrega a la conexión.
    if DB_SSL_CA:
        parametros["sslmode"] = "verify-ca"
        parametros["sslrootcert"] = DB_SSL_CA

    return psycopg2.connect(**parametros)


def crear_base_datos():
    """Crea la base de datos (si no existe) y la tabla 'alumnos'."""
    try:
        conexion = obtener_conexion(nombre_bd="postgres")
        conexion.autocommit = True
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        existe = cursor.fetchone()
        if not existe:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
        cursor.close()
        conexion.close()
    except Exception as error:
        # En algunos servidores en la nube la base de datos ya viene creada
        # y el usuario no tiene permiso para crear otras; no es un error grave.
        print("Aviso al verificar/crear la base de datos:", error)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            pasatiempos VARCHAR(255),
            me_gusta VARCHAR(255)
        )
    """)
    conexion.commit()
    cursor.close()
    conexion.close()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/saludar", methods=["POST"])
def f_saludar():
    nombre = request.form["nombre"]
    pasatiempos = request.form.getlist("pasatiempos")
    me_gusta = request.form["me_gusta"]

    pasatiempos_texto = ", ".join(pasatiempos)

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO alumnos (nombre, pasatiempos, me_gusta)
        VALUES (%s, %s, %s)
    """, (nombre, pasatiempos_texto, me_gusta))
    conexion.commit()
    cursor.close()
    conexion.close()

    return render_template(
        "saludar.html",
        nombre=nombre,
        pasatiempos=pasatiempos,
        me_gusta=me_gusta
    )


@app.route("/alumnos")
def listar_alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, pasatiempos, me_gusta FROM alumnos ORDER BY id")
    alumnos = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template(
        "listar_alumnos.html",
        alumnos=alumnos
    )


crear_base_datos()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=True)
