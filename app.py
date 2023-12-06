# --------------------------------------------------------------------
# Instalar con pip install Flask
from click import INT
from flask import Flask, request, jsonify
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python
import os
import time
# --------------------------------------------------------------------
app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas


class Catalogo:
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:

            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS juegos (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(255) NOT NULL,
            participantes_min INT NOT NULL,
            participantes_max INT NOT NULL,
            url_imagen VARCHAR(255),
            url_video VARCHAR(255))AUTO_INCREMENT=100;''')
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
    # ----------------------------------------------------------------

    def listar_juegos(self):
        self.cursor.execute("SELECT * FROM juegos")
        juegos = self.cursor.fetchall()
        return juegos

    # ----------------------------------------------------------------
    def consultar_juego(self, codigo):
        self.cursor.execute(f"SELECT * FROM juegos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    # ----------------------------------------------------------------
    def mostrar_juego(juego):
        if juego:
            print("-" * 40)
            print(f"Código.....: {juego['codigo']}")
            print(f"Nombre: {juego['nombre']}")
            print(f"Descripción: {juego['descripcion']}")
            print(f"Min Participantes...: {juego['participantes_min']}")
            print(f"Máx Participantes.....: {juego['participantes_max']}")
            print(f"URL Imagen.....: {juego['url_imagen']}")
            print(f"URL Video..: {juego['url_video']}")
            print("-" * 40)
        else:
            print("Juego no encontrado.")
    # ---------------------------------------------------------------

    def agregar_juego(self, nombre, descripcion, participantesMin, participantesMax, urlImagen, urlVideo):
        self.cursor.execute(f"SELECT * FROM juegos WHERE nombre = '{nombre}'")
        juego_existe = self.cursor.fetchone()
        if juego_existe:
            return False

        sql = "INSERT INTO juegos (nombre, descripcion, participantes_min, participantes_max,url_imagen, url_video) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, descripcion, participantesMin,
                   participantesMax, urlImagen, urlVideo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def eliminar_juego(self, codigo):
        self.cursor.execute(f"DELETE FROM juegos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def modificar_juego(self, codigo, nuevo_nombre, nueva_descripcion, nueva_urlImagen, nuevo_participantesMin, nuevo_participantesMax, nuevo_urlVideo):
        sql = "UPDATE juegos SET nombre = %s, descripcion = %s, urlImagen = %s,  = %s, participantesMin = %s, participantesMax = %s, urlVideo = %s" + \
            f"WHERE codigo = {codigo}"
        valores = (nuevo_nombre, nueva_descripcion, nueva_urlImagen,
                   nuevo_participantesMin, nuevo_participantesMax, nuevo_urlVideo)
        self.cursor.execute(sql, valores)
        self.conn. commit()
        return self.cursor.rowcount > 0


# ----------------------------------------------------------------
# Cuerpo del programa
# ----------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='1959marcos',
                    database='juegos_db')

# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'

# ----------------------------------------------------------------


@app.route("/juegos", methods=["GET"])
def listar_juegos():
    juegos = catalogo.listar_juegos()
    return jsonify(juegos)

# ----------------------------------------------------------------


@app.route("/juegos/<int:codigo>", methods=["GET"])
def mostrar_juego(codigo):
    catalogo.mostrar_juego(codigo)
    juego = catalogo.consultar_juego(codigo)
    if juego:
        return jsonify(juego)
    else:
        return "Juego no encontrado", 404
# ----------------------------------------------------------------


@app.route("/juegos", methods=["POST"])
def agregar_juego():
    print(request.form)
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    participantesMin = request.form['participantesMin']
    participantesMax = request.form['participantesMax']
    urlImagen = request.form['urlImagen']
    urlVideo = request.form['urlVideo']

    if catalogo.agregar_juego(nombre, descripcion, participantesMin, participantesMax, urlImagen, urlVideo):
        return jsonify({"mensaje": "Juego agregado"}), 201
    else:
        return jsonify({"mensaje": "Juego ya existe"}), 400


@app.route("/juegos/<int:codigo>", methods=["DELETE"])
def eliminar_juego(codigo):
    juego = catalogo.consultar_juego(codigo)
    if juego:
        if catalogo.eliminar_juego(id):
            return jsonify({"mensaje": "Juego eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el juego"}), 500
    else:
        return jsonify({"mensaje": "Juego no encontrado"}), 404


@app.route("/juegos/<int:codigo>", methods=["PUT"])
def modificar_juego(codigo):
    # Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nueva_descripcion = request.form.get("descripcion")
    nuevo_participantesMin = request.form.get("participantesMin")
    nuevo_participantesMax = request.form.get("participantesMax")
    nueva_urlImagen = request.form.get("urlImagen")
    nuevo_urlVideo = request.form.get("urlVideo")

    # Actualización del juego-
    if catalogo.modificar_juego(codigo, nuevo_nombre, nueva_descripcion, nuevo_participantesMin, nuevo_participantesMax, nueva_urlImagen, nuevo_urlVideo):
        return jsonify({"mensaje": "Juego modificado"}), 200
    else:
        return jsonify({"mensaje": "Juego no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)
