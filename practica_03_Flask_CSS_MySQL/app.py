from flask import Flask, render_template, request
import pymysql
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
DB_HOST = os.environ.get("MYSQL_HOST", "localhost")
DB_PORT = int(os.environ.get("MYSQL_PORT", 3306))
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
DB_NAME = os.environ.get("MYSQL_DATABASE", "practica_03")
DB_SSL_CA = os.environ.get("MYSQL_SSL_CA", "")  # ruta al certificado, solo para la nube


def obtener_conexion(con_base_datos=True):
    """Crea una conexión a MySQL. Si con_base_datos=False, se conecta
    al servidor sin seleccionar ninguna base de datos todavía (se usa
    una sola vez, para poder crear la base de datos si no existe)."""
    parametros = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "charset": "utf8mb4",
    }

    if con_base_datos:
        parametros["database"] = DB_NAME

    # Si se definió un certificado SSL (necesario para bases de datos en la nube
    # como Aiven), se agrega a la conexión.
    if DB_SSL_CA:
        parametros["ssl_ca"] = DB_SSL_CA
        parametros["ssl_verify_cert"] = True

    return pymysql.connect(**parametros)


def crear_base_datos():
    """Crea la base de datos y la tabla 'alumnos' si todavía no existen."""
    conexion = obtener_conexion(con_base_datos=False)
    cursor = conexion.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conexion.commit()
    cursor.close()
    conexion.close()

    conexion = obtener_conexion(con_base_datos=True)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INT AUTO_INCREMENT PRIMARY KEY,
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
