from flask import render_template,Flask,url_for,request,session,jsonify
from decimal import Decimal
from flask_socketio import SocketIO, join_room, leave_room, emit
from modulos.gestorBaseDatos import * 

# Para generar una 'secret_key'.
import secrets

# Cifrado de contraseñas
from passlib.hash import pbkdf2_sha256

# Fecha y hora para introducir productos de carrito compra
from datetime import datetime

# Para poder subir imágenes en "agregar producto"
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key= secrets.token_hex(24)
socketio = SocketIO(app)


# Página de inicio
@app.route('/')
def index():
    if 'nombre' in session:
        session['masFrecuentes'] = obtener_MasFrecuentes(session.get('email','no encontrado'))

        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador'],
            'masFrecuentes' : session['masFrecuentes'] 
        }

        return render_template('principal.html',datos=datos)
    else:

        return render_template('principal.html')


# Página bebidas
@app.route('/bebidas')
def bebidas():
    bebidas = devuelve_bebidas()
    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador']
        }

        return render_template('bebidas.html',bebidas=bebidas,datos=datos)
    else:

        return render_template('bebidas.html',bebidas=bebidas)


# Página aperitivos
@app.route('/aperitivos')
def aperitivos():
    aperitivos = devuelve_aperitivos()
    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador']
        }

        return render_template('aperitivos.html',aperitivos=aperitivos,datos=datos)
    else:

        return render_template('aperitivos.html',aperitivos=aperitivos)
#------------------------------------------------------------------------------------------------------------


# Registro
@app.route('/formulario_Registro.html')
def formulario_Registro():
    
    return render_template('formulario_Registro.html')


# Obtiene el id para comprobar si ya existe un usuario con el correo introducido
@app.route('/obtener_Id', methods=['POST'])
def obtener_Id():
    data = request.json
    id = id_Usuario(data['email'])

    return jsonify(id)


# Cifrar contraseña
def hash_constrasenia(contrasenia):
    return pbkdf2_sha256.hash(contrasenia)


@app.route('/registra_Usuario', methods=['POST'])
def registra_Usuario():
    datos = request.json
    contrasenia = datos.get('contrasenia')
    datos['contrasenia'] = hash_constrasenia(contrasenia)
    respuesta = registar_Usuario(datos)

    return respuesta
#------------------------------------------------------------------------------------------------------------


# Inicio sesión

@app.route('/formulario_InicioSesion.html')
def formulario_InicioSesion():

    return render_template('formulario_InicioSesion.html')


def comprueba_contrasenia(contraNormal, contraCifrada):

    return pbkdf2_sha256.verify(contraNormal, contraCifrada)


@app.route('/inicia_Sesion', methods=['POST'])
def inicia_Sesion():
    datos = request.json
    contraseniaBd = sacar_Contrasenia(datos['correo'], datos['nombre'])

    if not contraseniaBd:

        return "No existe."
    elif comprueba_contrasenia(datos['contrasenia'],contraseniaBd[0]['contrasena']):
        fecha = datetime.now().strftime("%Y-%m-%d")
        datosUsuario = dame_DatosUsuario(datos['correo'], datos['nombre'], fecha)
        session['nombre'] = datosUsuario[0]['nombre']
        session['apellidos'] = datosUsuario[0]['apellidos']
        session['email'] = datosUsuario[0]['email']
        session['contrasenia'] = datos['contrasenia']
        session['es_administrador'] = datosUsuario[0]['es_administrador']
        session['carrito'] = []
        # Productos más frecuentes
        session['masFrecuentes'] = obtener_MasFrecuentes(datosUsuario[0]['email'])

        # El campo fechaNacimiento es un objeto de tipo date 'Tue, 30 Sep 1986 00:00:00 GMT'. Para que me resulte
        # más cómodo manejarlo, lo cambio a un string
        session['fecha_nacimiento'] = str(datosUsuario[0]['fecha_nacimiento'])

        # 1 administrador
        if session['es_administrador'] == 1:

            return "Sesión iniciada, admin."
        else:

            return "Sesión iniciada."
    else:

        return "No existe."
#------------------------------------------------------------------------------------------------------------


# Cierre sesión

@app.route('/cierra_Sesion', methods=['POST'])
def cerrar_Sesion():
    session.clear()

    return "Sesión finalizada."
#------------------------------------------------------------------------------------------------------------


# Modificar datos usuario

@app.route('/formulario_Modificar.html')
def formulario_Modificar():
    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'apellidos': session['apellidos'],
            'email': session['email'],
            'fecha_nacimiento': session['fecha_nacimiento']
        }

        return render_template('formulario_Modificar.html',datos=datos)
    else:

        return render_template('principal.html')
    

@app.route('/obten_DatosUsuario', methods=['POST'])
def obten_DatosUsuario():
    datos = {
        'nombre' : session.get('nombre','no encontrado'),
        'apellidos' : session.get('apellidos','no encontrado'),
        'email' : session.get('email','no encontrado'),
        'contrasenia' : session.get('contrasenia','no encontrado'),
        'fechaNacimiento' : session.get('fecha_nacimiento','no encontrado')
    }

    return (datos)


@app.route('/actualiza_DatosUsuario', methods=['POST'])
def actualiza_DatosUsuario():
    datosSesion = obten_DatosUsuario()
    correoAntiguo = datosSesion['email']
    datos = request.json
    respuesta = actualizar_DatosUsuario(datos,correoAntiguo)

    if respuesta == "Usuario actualizado.":
        session.clear()

        fecha = datetime.now().strftime("%Y-%m-%d")
        datosUsuario = dame_DatosUsuario(datos['correo'], datos['nombre'], fecha)
        session['nombre'] = datosUsuario[0]['nombre']
        session['apellidos'] = datosUsuario[0]['apellidos']
        session['email'] = datosUsuario[0]['email']
        session['contrasenia'] = datosUsuario[0]['contrasena']
        session['es_administrador'] = datosUsuario[0]['es_administrador']

        # El campo fechaNacimiento es un objeto de tipo date 'Tue, 30 Sep 1986 00:00:00 GMT'. Para que me resulte
        # más cómodo manejarlo, lo cambio a un string
        session['fecha_nacimiento'] = str(datosUsuario[0]['fecha_nacimiento'])

    return respuesta
#------------------------------------------------------------------------------------------------------------


# Dar de baja usuario

@app.route('/formulario_Eliminar.html')
def formulario_Eliminar():
    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador']
        }

        return render_template('formulario_Eliminar.html',datos=datos)
    else:
        
        return render_template('principal.html')
    

@app.route('/da_deBaja', methods=['POST'])
def da_deBaja():
    contrasenia = request.json
    datosSesion = obten_DatosUsuario()

    if contrasenia['contrasenia'] == datosSesion['contrasenia']:
        session.clear()
        dar_deBaja(datosSesion)

        return "Usuario eliminado."
    else:

        return "La contraseña introducida no coincide con la contraseña del usuario con la sesión iniciada."
#------------------------------------------------------------------------------------------------------------


# Agregar producto

@app.route('/formulario_AgregarProducto.html')
def formulario_AgregarProducto():
    if session.get('es_administrador') == 1:
        nombreProductos = dime_NombreTablas()
        datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
        }
        return render_template('formulario_AgregarProducto.html',datos=datos,nombreProductos=nombreProductos)
    
    else:
        if 'nombre' in session:
            datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
            }

            return render_template('principal.html',datos=datos)
        else:

            return render_template('principal.html')


@app.route('/agregar_producto',methods=['POST'])
def agregar_producto():
    # Obtiene la imagen
    imagen = request.files['imagen']
    # Obtiene los datos, convierte el objeto json datos en un diccionario 
    datos = json.loads(request.form['datos'])
    # Comprueba que el producto no exista
    if not comprobar_producto(datos['tipoProducto1'],datos['nombreProducto']):
        # Establece la ruta donde será guardada la imagen
        nombreImagen = secure_filename(imagen.filename)
        rutaImagen = 'static/imgs/'+datos['tipoProducto1']+'/'+nombreImagen
        # Guarda la imagen
        imagen.save(rutaImagen)
        # Inserta los datos y la ruta en la base de datos
        datos['img_ruta'] = rutaImagen
        respuesta = incertar_producto(datos)

        return respuesta
    else:
        return "El producto introducido ya existe."
#------------------------------------------------------------------------------------------------------------


# Carrito compra

@app.route('/carrito_Compra.html')
def carrito_Compra():

    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador'],
            'carrito' : session['carrito']
        }

        return render_template('carrito_Compra.html',datos=datos)
    else:

        return render_template('carrito_Compra.html')


@app.route('/sesion_Iniciada',methods=['GET'])
def sesion_Iniciada():
    if 'nombre' in session:
        return 'Sesión iniciada'
    else:
        return 'Sesión no iniciada'


@app.route('/añade_Producto', methods=['POST'])
def añade_Producto():
    datos = request.json
    rutaImg = datos['rutaImg']
    nombreProducto = datos['nombreProducto']
    partes = datos['precioProducto'].split(' ')
    precio_str = partes[1]
    precio_str = precio_str.replace('€', '')
    precioProducto = float(precio_str)
    cantidad = datos['cantidad']
    precioTotalProducto = precioProducto * float(cantidad)

    carrito = session.get('carrito', [])
    producto = {
        'rutaImg' : rutaImg,
        'nombreProducto': nombreProducto,
        'precioProducto': precioProducto,
        'cantidad' : cantidad,
        'precioTotalProducto': precioTotalProducto
    }
    carrito.append(producto)
    session['carrito'] = carrito

    return "Añadido"


@app.route('/dame_CarritoCompra')
def dame_CarritoCompra():
    carrito = session.get('carrito', [])

    return carrito


@app.route('/elimina_ProductoSesion', methods=['POST'])
def elimina_ProductoSesion():
    datos = request.json
    carrito = session.get('carrito', [])
    
    for i in range(len(carrito) - 1, -1, -1):
        if carrito[i]['nombreProducto'] == datos['nombreProducto']:
            del carrito[i]
    
    session['carrito'] = carrito

    return carrito


@app.route('/modifica_ProductoSesion', methods=['POST'])
def modifica_ProductoSesion():
    datos = request.json
    carrito = session.get('carrito', [])

    for i in range(len(carrito) - 1, -1, -1):
        if carrito[i]['nombreProducto'] == datos['nombreProducto']:
            carrito[i]['cantidad'] = datos['cantidad']
            carrito[i]['precioTotalProducto'] = float(carrito[i]['precioProducto']) * float(carrito[i]['cantidad'])
    
    session['carrito'] = carrito

    return carrito


@app.route('/haz_Compra', methods=['POST'])
def haz_Compra():
    datos = {
        'correo' : session.get('email'),
        'carrito' : session.get('carrito', []),
        'fecha' : datetime.now().strftime("%Y-%m-%d"),
        'hora' : datetime.now().strftime("%H:%M:%S")
    }

    respuesta = hacer_Compra(datos)

    session['carrito'] = []

    destinatario = session.get('email')
    asunto = 'Compra realizada'
    cuerpo = ''
    precioTotalCompra = 0
    print(datos['carrito'])
    for producto in datos['carrito']:
        precioTotalCompra += producto['precioTotalProducto']
        cuerpo += "Nombre del producto: " + producto['nombreProducto'] + ", Precio unitario producto: " + str(producto['precioProducto']) + "€" + ", Cantidad: " + str(producto['cantidad']) + ", Precio total: " + str(producto['precioTotalProducto']) + "€\n"
    
    cuerpo += "Precio total compra: " + str(round(precioTotalCompra, 2)) + "€"

    enviarCorreo(destinatario, asunto, cuerpo)

    return respuesta
#------------------------------------------------------------------------------------------------------------


# Enviar correo electrónico

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviarCorreo(destinatario, asunto, cuerpo):    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'cafeteriaflorentino@gmail.com'
    smtp_password = 'epnt nvba mjip sfbz'

    remitente = 'cafeteriaflorentino@gmail.com'
    destinatario = destinatario

    asunto = asunto
    cuerpo = cuerpo

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            
            # Intenta iniciar sesión con las credenciales
            server.login(smtp_username, smtp_password)

            # Intenta enviar el correo electrónico
            server.sendmail(remitente, destinatario, mensaje.as_string())

        print('Correo electrónico enviado con éxito.')

    except smtplib.SMTPAuthenticationError as auth_error:
        print(f'Error de autenticación: {auth_error}')

    except smtplib.SMTPException as smtp_error:
        print(f'Error SMTP: {smtp_error}')

    except Exception as e:
        print(f'Ocurrió un error inesperado: {e}')
#------------------------------------------------------------------------------------------------------------


# Clic en perfil

@app.route('/perfil')
def perfil():
    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador']
        }

        return render_template('perfil.html', datos=datos)
    else:

        return render_template('perfil.html')
#------------------------------------------------------------------------------------------------------------    

# Buscador de productos

@app.route('/busca_producto',methods=['POST'])
def busca_producto():

    busqueda = request.form['producto']
    resultado = busca_productosBD(busqueda)

    return jsonify(resultado)

@app.route('/busqueda',methods=['POST'])
def busqueda():
    busqueda = request.form['producto']
    bebidas = devuelve_bebidas_conTipo(busqueda)
    aperitivos = devuelve_aperitivos_conTipo(busqueda)
    if 'nombre' in session:
        datos = {
            'nombre': session['nombre'],
            'es_administrador' : session['es_administrador'],
            'masFrecuentes' : session['masFrecuentes'] 
        }

        return render_template('vista_busqueda.html',datos=datos,bebidas=bebidas,aperitivos=aperitivos)
    else:

        return render_template('vista_busqueda.html',bebidas=bebidas,aperitivos=aperitivos)



# Administradores

@app.route('/admin_principal',methods=['GET','POST'])
def admin_principal():
    if session.get('es_administrador') == 1:
        datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
        }
        return render_template('admin_principal.html',datos=datos)
    
    else:
        if 'nombre' in session:
            datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
            }
            return render_template('principal.html',datos=datos)
        
        else:

            return render_template('principal.html')


# Modificar bebida.
@app.route('/modificar_eliminar_bebidas',methods=['POST','GET'])
def pagina_modificar_bebida():
    if session.get('es_administrador') == 1:
        bebidas = devuelve_bebidas()
        datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
        }

        return render_template('modificar_eliminar_bebidas.html',datos=datos,bebidas = bebidas)
    else:
        if 'nombre' in session:
            datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
            }

            return render_template('principal.html',datos=datos)
        else:

            return render_template('principal.html')


    


@app.route('/modificar_bebida',methods=['POST'])
def modificar_bebida():
    info = request.json

    return modificar_producto_bd(info)

@app.route('/eliminar_bebida',methods=['POST'])
def eliminar_bebida():
    info = request.json

    return eliminar_producto_bd(info)


# Modificar aperitivo
@app.route('/modificar_eliminar_aperitivos',methods=['POST','GET'])
def pagina_modificar_aperitivos():
    if session.get('es_administrador') == 1:
        aperitivos = devuelve_aperitivos()
        datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
        }

        return render_template('modificar_eliminar_aperitivos.html',datos=datos,aperitivos = aperitivos)
    else:
        if 'nombre' in session:
            datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
            }

            return render_template('principal.html',datos=datos)
        else:

            return render_template('principal.html')



@app.route('/modificar_aperitivo',methods=['POST'])
def modificar_aperitivo():
    info = request.json

    return modificar_producto_bd(info)

@app.route('/eliminar_aperitivo',methods=['POST'])
def eliminar_aperitivo():
    info = request.json
    print(info)
    return eliminar_producto_bd(info)


@app.route('/vista_pedido_admin')
def vista_pedido_admin():
    if session.get('es_administrador') == 1:
        pedidos = devuelve_pedidos_activos()
        datosUsuario = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
        }

        # Nuevo diccionario
        result = {}

        # Recorre la lista original y construye el nuevo diccionario
        for entry in pedidos:
            nombre = entry['nombre']
            datos = {k: v for k, v in entry.items() if k != 'nombre'}
            if nombre not in result:
                result[nombre] = [datos]
            else:
                result[nombre].append(datos)
                
        print(result)

        # Imprime el resultado
        return render_template('pagina_pedidos.html',datos=datosUsuario,pedidos=result)

    else:
        if 'nombre' in session:
            datos = {
                'nombre': session['nombre'],
                'es_administrador' : session['es_administrador']
            }

            return render_template('principal.html',datos=datos)
        else:
            
            return render_template('principal.html')


@app.route('/entregar_pedido',methods=['POST'])
def entregar_pedido():
    id = request.form['idUsuario']
    entrega_pedidoBD(id)
    return 'done'

@app.route('/cancelar_pedido',methods = ['POST'])
def cancelar_pedido():
    id = request.form['idUsuario']
    cancelar_pedidoBD(id)
    return 'done'





### SOCKET
@socketio.on('connect')
def handle_connect():
    print(f'Usuario conectado: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Usuario desconectado: {request.sid}')

@socketio.on('mensaje_del_cliente')
def handle_message(data):
    user_sid = data['user_sid']
    message = data
    print(message)

    cantidad = cuantos_en_esperaBD()[0]['count(*)']
    res = ''
    if cantidad <= 5:
        res = '10 minutos.'
    elif cantidad <=15:
        res = '20 minutos.'
    else:
        res = '25 - 30 minutos.' 
    


    # # Enviar el mensaje al usuario específico
    emit('respuesta_del_servidor', res, room=user_sid)
    emit('respuesta_del_servidor', 'admin', broadcast=True)




if __name__ == '__main__':
    # app.run(
    #     host= "0.0.0.0",
    #     port = 5000,
    #     threaded = True
    # )
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        
        debug=True
    )