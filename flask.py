#--------------------------------------------------------------------
# Instalar con pip install Flask
from click import INT
from flask import Flask, request, jsonify
from flask import request
# Instalar con pip install flask-cors
from flask_cors import CORS
# Instalar con pip install mysql-connector-python
import mysql.connector
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------
app = Flask(__name__)
CORS(app) # Esto habilitará CORS para todas las rutas

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
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor INT)''')
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
    #----------------------------------------------------------------
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        return productos
    
    #----------------------------------------------------------------
    def consultar_producto(self, codigo):
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo}")
        return self.cursor.fetchone()
    
    #----------------------------------------------------------------
    def mostrar_producto(self, codigo):
        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción: {producto['descripcion']}")
            print(f"Cantidad...: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
            print(f"Imagen.....: {producto['imagen_url']}")
            print(f"Proveedor..: {producto['proveedor']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")
    #---------------------------------------------------------------


    def agregar_producto(self, id, nombre, descripcion, urlImagen, participantesMin, participantesMax, urlVideo):
        self.cursor.execute(f"SELECT * FROM juegos WHERE id = {id}")
        juego_existe = self.cursor.fetchone()
        if juego_existe:
            return False
        
        sql = "INSERT INTO juegos (id, nombre, descripcion, urlImagen, participantesMin, participantesMax, urlVideo) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (id, nombre, descripcion, urlImagen, participantesMin, participantesMax, urlVideo)
        self.cursor.execute(sql,valores)
        self.conn.commit()
        return True
    
    def eliminar_juego(self, id):
        self.cursor.execute(f"DELETE FROM juegos WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def modificar_juego(self, id, nuevo_nombre, nueva_descripcion, nueva_urlImagen, nuevo_participantesMin, nuevo_participantesMax, nuevo_urlVideo):
        sql = "UPDATE juegos SET nombre = %s, descripcion = %s, urlImagen = %s,  = %s, participantesMin = %s, participantesMax = %s, urlVideo = %s WHERE id = %s"
        valores = (id, nuevo_nombre, nueva_descripcion, nueva_urlImagen, nuevo_participantesMin, nuevo_participantesMax, nuevo_urlVideo)
        self.cursor.execute(sql, valores)
        self.conn. commit()
        return self.cursor.rowcount > 0
#----------------------------------------------------------------
# Cuerpo del programa
#----------------------------------------------------------------
# Crear una instancia de la clase Catalogo
catalogo = Catalogo(host='localhost', user='root', password='', 
database='miapp')

# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'

#----------------------------------------------------------------
@app.route("/juegos", methods=["GET"])
def listar_juegos():
    juegos = catalogo.listar_juegos()
    return jsonify(juegos)

#----------------------------------------------------------------
@app.route("/juegos/<int:codigo>", methods=["GET"])
def mostrar_juego(codigo):
    catalogo.mostrar_juego(codigo)
    juego = catalogo.consultar_juego(codigo)
    if juego:
        return jsonify(juego)
    else:
        return "Juego no encontrado", 404
#----------------------------------------------------------------
    
@app.route("/juegos", methods=["POST"])
def agregar_juego():
    id = request.form['id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion'] 
    urlImagen = request.files['urlImagen']
    nombre_imagen = secure_filename(urlImagen.filename)
    particpantesMin = request.form['participantesMin']
    participantesMax = request.form['participantesMax']
    urlVideo = request.form['urlVideo']

    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    urlImagen.save(os.path.join(ruta_destino, nombre_imagen))

    if catalogo.agregar_juego(id, nombre, descripcion, nombre_imagen, particpantesMin, participantesMax, urlVideo):
        return jsonify({"mensaje": "Juego agregado"}), 201
    else:
        return jsonify({"mensaje": "Juego ya existe"}), 400
    
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_juego(id):
    # Primero, obtén la información del juego para encontrar la imagen
    juego = catalogo.consultar_juego(id)
    if juego:
        # Eliminar la imagen asociada si existe
        ruta_imagen = os.path.join(ruta_destino, juego['urlImagen'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)
        # Luego, elimina el juego del catálogo
        if catalogo.eliminar_juego(id):
            return jsonify({"mensaje": "Juego eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el juego"}), 500
    else:
        return jsonify({"mensaje": "Juego no encontrado"}), 404


@app.route("/juegos/<int:id>", methods=["PUT"])
def modificar_juego(id):
    # Recojo los datos del form
    nuevo_nombre = request.form.get("nombre")
    nueva_descripcion = request.form.get("descripcion")
    nueva_urlImagen = request.form.get("urlImagen")
    nuevo_participantesMin = request.form.get("participantesMin")
    nuevo_participantesMax = request.form.get("participantesMax")
    nuevo_urlVideo = request.form.get("urlVideo")

    # Procesamiento de la imagen
    urlImagen = request.files['urlImagen']
    nombre_imagen = secure_filename(urlImagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    urlImagen.save(os.path.join(ruta_destino, nombre_imagen))

    # Actualización del juego-
    if catalogo.modificar_juego(id, nuevo_nombre, nueva_descripcion, nueva_urlImagen, nuevo_participantesMin, nuevo_participantesMax, nuevo_urlVideo):
       return jsonify({"mensaje": "Juego modificado"}), 200
    else:
       return jsonify({"mensaje": "Juego no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
