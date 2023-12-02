class Catalogo:
    productos= []

def agregar_producto(self, id, nombre, descripcion, urlImagen, 
participantesMin, participantesMax, urlVideo):

    if self.consultar_producto(id):
        return False

    nuevo_producto= {
        'id': id,
        'nombre': nombre,
        'descripcion': descripcion,
        'urlImagen': urlImagen,
        'participantesMin': participantesMin,
        'participantesMax': participantesMax,
        'urlVideo': urlVideo
}
    self.productos.append(nuevo_producto)
    return True
    

def consultar_producto(self, id):
    for producto in self.productos:
        if producto['id'] ==id:
            return producto
    return False
    
def modificar_producto(self, id, nuevo_nombre, nueva_descripcion, nueva_urlImagen, nuevo_participantesMin, nuevo_participantesMax, nueva_urlVideo):
    for producto in self.productos:
        if producto['id'] ==id:
           producto['nombre'] =nuevo_nombre
           producto['descripcion'] =nueva_descripcion
           producto['urlImagen'] =nueva_urlImagen
           producto['participantesMin'] =nuevo_participantesMin
           producto['participantesMax'] =nuevo_participantesMax
        return True
    return False

def listar_productos(self):
    print("-"*50)
    for producto in self.productos:
        print(f"id...................: {producto['id']}")
        print(f"nombre...............: {producto['nombre']}")
        print(f"descripcion..........: {producto['descripcion']}")
        print(f"urlImagen............: {producto['urlImagen']}")
        print(f"participantesMin.....: {producto['participantesMin']}")
        print(f"participantesMax.....: {producto['participantesMax']}")
        print("-"*50)

def eliminar_producto(self, id):
    for producto in self.productos:
        if producto['id'] ==id:
            self.productos.remove(producto)
            return True
    return False

def mostrar_producto(self, id):
    producto=self.consultar_producto(id)
    if producto:
        print("-"*50)
        print(f"id...............: {producto['id']}")
        print(f"nombre:..........: {producto['nombre']}")
        print(f"descripcion......: {producto['descripcion']}")
        print(f"urlImagen........: {producto['urlImagen']}")
        print(f"participantesMin.: {producto['participantesMin']}")
        print(f"participantesMax.: {producto['participantesMax']}")
        print("-"*50)
    else:
        print("Producto no encontrado.")
        
