import pymysql
from datetime import datetime, timedelta

# Base de datos florentino
def conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="florentino",
        charset="utf8",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )


def devuelve_bebidas():
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT id,nombre,descripcion,estado,precio,tipo,img_ruta FROM bebidas;"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


def devuelve_aperitivos():
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT id,nombre,descripcion,estado,precio,tipo,img_ruta FROM aperitivos;"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


# Registro
def id_Usuario(correo):
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = "SELECT id FROM usuarios WHERE email = %s;"
                cursor.execute(comando, (correo,))
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


def registar_Usuario(datos):
    nombre = datos.get('nombre')
    apellidos = datos.get('apellidos')
    correo = datos.get('correo')
    contrasenia = datos.get('contrasenia')
    fechaNacimiento = datos.get('fechaNacimiento')
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = "INSERT INTO usuarios (nombre, apellidos, email, contrasena, es_administrador, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(comando, (nombre, apellidos, correo, contrasenia, 0, fechaNacimiento,))
                conn.commit()

                return("Usuario registrado.")
            
    except Exception as err:
        return(err)
#------------------------------------------------------------------------------------------------------------


# Inicio sesión
def sacar_Contrasenia(correo, nombre):
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = "SELECT `contrasena` FROM `usuarios` WHERE email = %s AND nombre = %s;"
                cursor.execute(comando, (correo, nombre,))
                data = cursor.fetchall()

                return data
            
    except Exception as err:
        return(err)


def dame_DatosUsuario(correo, nombre, fecha):
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                # Actualizar la última conexión
                comando_update = "UPDATE `usuarios` SET `ultima_conexion` = %s WHERE `email` = %s AND nombre = %s;"
                cursor.execute(comando_update, (fecha, correo, nombre,))
                conn.commit()

                # Datos usuario
                comando_select = "SELECT `nombre`, `apellidos`, `email`, `contrasena`, `es_administrador`, `fecha_nacimiento` FROM `usuarios` WHERE `email` = %s AND nombre = %s;"
                cursor.execute(comando_select, (correo, nombre,))
                data = cursor.fetchall()

                return data

    except Exception as err:
        return str(err)
#------------------------------------------------------------------------------------------------------------


# Modificar datos usuario
def actualizar_DatosUsuario(datos, correoAntiguo):
    nombre = datos.get('nombre')
    apellidos = datos.get('apellidos')
    correo = datos.get('correo')
    fechaNacimiento = datos.get('fechaNacimiento')
    correoAntiguo = correoAntiguo

    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = "UPDATE `usuarios` SET `nombre`= %s,`apellidos`= %s,`email`= %s,`fecha_nacimiento`= %s WHERE `email` = %s;"
                cursor.execute(comando, (nombre, apellidos, correo, fechaNacimiento, correoAntiguo,))

                return "Usuario actualizado."
            
    except Exception as err:
        return f"Error: {err}"
#------------------------------------------------------------------------------------------------------------


# Dar de baja usuario 
def dar_deBaja(datosSesion):
    correo = datosSesion.get('email')
    idUsuario = id_Usuario(correo)
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando1 = "DELETE FROM `compras` WHERE idUsuario = %s;"
                cursor.execute(comando1, (idUsuario[0]['id'],))

                comando2 = "DELETE FROM `usuarios` WHERE email = %s;"
                cursor.execute(comando2, (correo,))

    except pymysql.Error as err:
        print(f"Error: {err}")
        return str(err)
#------------------------------------------------------------------------------------------------------------


# Agregar producto
def dime_NombreTablas():
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SHOW TABLES;"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


def incertar_producto(datos):
    tipoProducto1 = datos.get('tipoProducto1')
    nombreProducto = datos.get('nombreProducto')
    descripcionProducto = datos.get('descripcionProducto')
    estado = datos.get('estado')
    tipoProducto2 = datos.get('tipoProducto2')
    precio = datos.get('precio')
    img_ruta = datos.get('img_ruta')

    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = "INSERT INTO {} (nombre, descripcion, estado, tipo, precio, img_ruta) VALUES (%s, %s, %s, %s, %s, %s);".format(tipoProducto1)
                cursor.execute(comando, (nombreProducto, descripcionProducto, estado, tipoProducto2, precio, img_ruta))
                conn.commit()

                return "Producto registrado."
            
    except Exception as err:
        print(err)

        return "No se ha podido resgistrar el producto."
    

def comprobar_producto(tipoProducto,nombreProducto):
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = "SELECT * FROM {} WHERE nombre = %s;".format(tipoProducto)
                cursor.execute(comando, (nombreProducto,))
                data = cursor.fetchall()

                return data
            
    except Exception as err:

        return err
#------------------------------------------------------------------------------------------------------------


# Compra
def hacer_Compra(datos):
    idUsuario = id_Usuario(datos.get('correo'))[0]['id']
    carrito = datos.get('carrito')
    fecha = datos.get('fecha')
    hora = datos.get('hora')
    
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                for item in carrito:
                    nombreProducto = item['nombreProducto']
                    cantidad = item['cantidad']
                    precioProducto = item['precioProducto']
                    precioTotalProducto = item['precioTotalProducto']
                    img_ruta = item['rutaImg']

                    comando = "INSERT INTO `compras`(`idUsuario`, `nombreProducto`, `cantidad`, `precio`, `precioTotal`, `fecha`, `hora`,`estado`, `img_ruta`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s);"
                    cursor.execute(comando, (idUsuario, nombreProducto, cantidad, precioProducto, precioTotalProducto, fecha, hora,'Pendiente', img_ruta))
                    
                return "Compra añadida"

    except Exception as err:
        print(err)
        return "Error"
#------------------------------------------------------------------------------------------------------------


# Productos más frecuentes
def obtener_MasFrecuentes(correo):
    idUsuario = id_Usuario(correo)[0]['id']
    try:
        with conexion2() as conn:
            with conn.cursor() as cursor:
                comando = """
                    SELECT nombreProducto, precio, img_ruta, totalCantidad
                    FROM (
                        SELECT nombreProducto, precio, img_ruta,
                        SUM(cantidad) OVER (PARTITION BY nombreProducto) as totalCantidad
                        FROM compras
                        WHERE estado = 'Entregado' AND idUsuario = %s AND fecha >= DATE_SUB(CURDATE(), INTERVAL 1 WEEK)
                    ) as subquery
                    GROUP BY nombreProducto
                    ORDER BY totalCantidad DESC
                    LIMIT 3;
                    """
                cursor.execute(comando, (idUsuario,))
                data = cursor.fetchall()
                return data

    except Exception as err:
        print(f"Error al obtener productos más frecuentes: {err}")

# La subconsulta selecciona el nombre, el precio, la ruta de la imagen y la cantidad como totalCantidad 
# sumando todas las cantidades de los productos con el mismo nombre de la tabla compras, que tengan estado 
# igual a entregado, el id de un usuario concreto y una fecha de subida no menor a una semana.
# Sobre esta consulta, hay otra consulta que selecciona todo lo anterior agrupando por el nombre del producto
# y ordenando en orden descendente por el totalCantidad y limitando a 3 los seleccionados. 

# SUM() es una función de agregación que opera sobre una "ventana". Estas funciones permiten realizar cálculos 
# y operaciones analíticas en un conjunto de datos específico definido por la cláusula OVER. Para las 
# funciones de ventana se recomineda usar subsconsultas.
#------------------------------------------------------------------------------------------------------------


# Modificar producto
def modificar_producto_bd(infos):
    print(infos)
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                productos_actualizados = []
                print(infos)
                for info in infos:
                    print(info)
                    if info['producto'] == 'bebida':
                        tabla = 'bebidas'
                    else:
                        tabla = 'aperitivos'

                    comando = f"UPDATE `{tabla}` SET `{info['field']}`='{info['value']}' WHERE `id` = '{info['id']}';"
                    cursor.execute(comando)
                    productos_actualizados.append(info['producto'].title())
                return f"{', '.join(productos_actualizados)} actualizad@."
    except Exception as err:
        print(err)
        return ('No se ha podido modificar el producto')


# Eliminar producto
def eliminar_producto_bd(infos):
    print(infos)
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                for info in infos:
                    if info['producto'] == 'bebida':
                        tabla = 'bebidas'
                    else:
                        tabla = 'aperitivos'
                    comando = f"DELETE FROM `{tabla}` WHERE `id` = '{info['id']}';"
                    cursor.execute(comando)
                    return f"{', '.join(info['producto'].title())} eliminado@."
    except Exception as err:
        print(err)
        return ('No se ha podido eliminar el producto')


# Búsqueda de productos
def busca_productosBD(producto):
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT nombre FROM bebidas WHERE nombre like '%{producto}%';"
                cursor.execute(comando)
                data = [fila['nombre'] for fila in cursor.fetchall()]

                comando = f"SELECT nombre FROM aperitivos WHERE nombre like '%{producto}%';"
                cursor.execute(comando)
                data_aperitivos = [fila['nombre'] for fila in cursor.fetchall()]



                data.extend(data_aperitivos)

                return data

    except pymysql.MySQLError as err:
        print(err)


def devuelve_bebidas_conTipo(producto):
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT id,nombre,descripcion,estado,precio,tipo,img_ruta FROM bebidas WHERE nombre like '%{producto}%';"
                cursor.execute(comando)
                data = cursor.fetchall()
                print(data)
                return data

    except Exception as err:
        print(err)
    

def devuelve_aperitivos_conTipo(producto):
    try:
        conn = conexion()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT id,nombre,descripcion,estado,precio,tipo,img_ruta FROM aperitivos WHERE nombre like '%{producto}%';"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


# Base de datos users
def conexion2():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="users",
        charset="utf8",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )


# Eliminar usuarios que llevan dos años o más sin iniciar sesión en el sistema
def eliminar_usuarios_inactivos():
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:

                # Calcular la fecha actual menos dos años
                fecha_limite = datetime.now() - timedelta(days=365 * 2)

                # Borra las compras de los usuarios con dos o más tiempo de inactividad
                comando = "SELECT id FROM usuarios WHERE `ultima_conexion` <= %s;"
                cursor.execute(comando, (fecha_limite,))
                data = cursor.fetchall()
                for elemento in data:
                    comando_delete = "DELETE FROM `compras` WHERE `idUsuario` = %s;"
                    cursor.execute(comando_delete, (elemento['id'],))
                
                # Consulta para eliminar usuarios inactivos
                comando_delete = "DELETE FROM `usuarios` WHERE `ultima_conexion` < %s;"
                cursor.execute(comando_delete, (fecha_limite,))
                conn.commit()

                print("Usuarios inactivos eliminados")

    except Exception as err:
        print(f"Error: {err}")


# Llama a la función 
eliminar_usuarios_inactivos()
#------------------------------------------------------------------------------------------------------------
   

def devuelve_pedidos_activos():
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT a.nombre,a.id,b.nombreProducto,b.cantidad,b.precio,b.estado FROM usuarios a, compras b WHERE a.id=b.idUsuario AND b.estado='Pendiente';"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


def entrega_pedidoBD(id):
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = f"UPDATE compras SET `estado`='Entregado' WHERE `idUsuario` = '{id}' AND estado = 'Pendiente';"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


def cancelar_pedidoBD(id):
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = f"UPDATE compras SET `estado`='Cancelado' WHERE `idUsuario` = '{id}' AND estado = 'Pendiente';"
                cursor.execute(comando)
                data = cursor.fetchall()

                return data

    except Exception as err:
        print(err)


def cuantos_en_esperaBD():
    try:
        conn = conexion2()
        with conn:
            with conn.cursor() as cursor:
                comando = f"SELECT count(*) FROM compras WHERE estado = 'Pendiente'"
                cursor.execute(comando)
                data = cursor.fetchall()
                
                return data

    except Exception as err:
        print(err)