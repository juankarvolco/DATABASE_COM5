self.conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Constructor: def __init__(self, host, user, password, database):
# Este método es el constructor de la clase. Inicializa una instancia de Catalogo y crea una
# conexión a la base de datos. Toma cuatro argumentos: `host`, `user`, `password`, y `database`,
# que se utilizan para establecer una conexión con la base de datos.

import mysql.connector
class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
)
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
id INT(2),
nombre VARCHAR(20) NOT NULL,
descripcion VARCHAR(150)
urlImagen VARCHAR(40) NOT NULL,
participantesMin INT(2) NOT NULL,
participantesMax INT(2),
urlVideo VARCHAR(40),
PRIMARY KEY ('id')''')
        self.conn.commit()

# Método Agregar Producto: def agregar_producto(self, id, nombre, descripcion, urlImagen, participantesMin,
# participantesMax, urlVideo)
# Este método tiene como objetivo principal agregar un nuevo producto a una base de datos.

def agregar_producto(self, id, nombre, descripcion, urlImagen, participantesMin,
participantesMax, urlVideo):
#Verificamos si ya existe un producto con el mismo id
    self.cursor.execute(f"SELECT * FROM productos WHERE id =
    {id}")
    producto_existe = self.cursor.fetchone()
    if producto_existe:
        return False
#Si no existe, agregamos el nuevo producto a la tabla
    sql = f"INSERT INTO productos (id, nombre, descripcion, urlImagen, participantesMin,
participantesMax, urlVideo) VALUES ({id}, '{nombre}, '{descripcion}',
    {urlImagen}, {participantesMin}, '{participantesMax}', {urlVideo})"
    self.cursor.execute(sql)
    self.conn.commit()
    return True

# Método Consultar Producto: def consultar_producto(self, id):
# Este método tiene como propósito principal consultar un producto específico en la base de datos
# a partir de su id.

def consultar_producto(self, id):

# Consultamos un producto a partir de su id
    
    self.cursor.execute(f"SELECT * FROM productos WHERE id =
    {id}")
    return self.cursor.fetchone()

# Método Modificar Producto: def modificar_producto(self, id, nuevo_nombre,
# nueva_descripcion, nueva_urlImagen, nuevo_participantesMin, nuevo_participantes_Max, nuevo_urlVideo):
# Este método tiene la función de actualizar los datos de un producto específico en la base de
# datos a partir de su id.

def modificar_producto(self, id, nuevo_nombre, nueva_descripcion, nueva_urlImagen, 
nuevo_participantesMin, nuevo_participantesMax, nuevo_urlVideo):
    sql = f"UPDATE productos SET nombre='{nuevo_nombre}', descripcion = '{nueva_descripcion}',
    urlImagen='{nueva_urlImagen}', paticipantesMin = {nuevo_participantesMin}, participantesMax = {nuevo_participantesMax}, 
    urlVideo = '{nuevo_urlVideo}', WHERE id = {id}"
    self.cursor.execute(sql)
    self.conn.commit()
    return self.cursor.rowcount > 0

# Método Mostrar Producto: def mostrar_producto(self, id):
# Este método tiene como objetivo mostrar en la consola los datos de un producto a partir de su
# id.

def mostrar_producto(self, id):

# Mostramos los datos de un producto a partir de su id
    
    producto = self.consultar_producto(id)
    if producto:
        print("-" * 40)
        print(f"Id...............: {producto['id']}")
        print(f"Nombre...........: {producto['nombre']}")
        print(f"Descripcion......: {producto['descripcion']}")
        print(f"urlImagen........: {producto['urlImagen']}")
        print(f"participantesMin.: {producto['participantesMin']}")
        print(f"participantesMax.: {producto['participantesMax']}")
        print(f"urlVideo.........: {producto['urlVideo']}")
        print("-" * 40)
    else:
        print("Producto no encontrado.")

# Método Listar Productos: def listar_productos(self):
# Este método tiene la finalidad de mostrar en pantalla un listado de todos los productos
# almacenados en la tabla de la base de datos.

def listar_productos(self):

# Mostramos en pantalla un listado de todos los productos en la
# tabla
    
    self.cursor.execute("SELECT * FROM productos")
    productos = self.cursor.fetchall()
    print("-" * 40)
    for producto in productos:
        print(f"Id...............: {producto['id']}")
        print(f"Nombre...........: {producto['nombre']}")
        print(f"Descripcion......: {producto['descripcion']}")
        print(f"urlImagen........: {producto['urlImagen']}")
        print(f"participantesMin.: {producto['participantesMin']}")
        print(f"participantesMax.: {producto['participantesMax']}")
        print(f"urlVideo.........: {producto['urlVideo']}")
        print("-" * 40)

# Método Eliminar Producto: def eliminar_producto(self, id):
# Este método tiene como objetivo eliminar un producto de la tabla de la base de datos a partir
# de su id.

def eliminar_producto(self, id):

# Eliminamos un producto de la tabla a partir de su id
    
    self.cursor.execute(f"DELETE FROM productos WHERE id =
    {id}")
    self.conn.commit()
    return self.cursor.rowcount > 0

