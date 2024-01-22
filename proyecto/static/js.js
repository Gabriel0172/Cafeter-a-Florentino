let cambiosPendientesAperitivos = false;
let cambiosPendientesBebidas = false;
$(document).ready(function() {
    
    // Funciones

    /* Establece la fecha actual como límite superior en el input de tipo date, que hay en los formularios
    de registro y modificación de usuario */
    let fechaHoy=new Date();
    let anio=formatea(fechaHoy.getFullYear());
    let mes=formatea(fechaHoy.getMonth()+1);
    let dia=formatea(fechaHoy.getDate());
    let fechaHoyFormateada = anio + "-" + mes + "-" + dia;
    
    $('[name="fechaNacimiento"]').attr('max',fechaHoyFormateada);
    
    function formatea(numero){
        if (numero<10) {
            return "0"+numero;
        }
        return numero.toString();
    }

    /* Comprueba los datos introducidos en los formularios de registro y de modificación */
    function compruebaDatos(nombre,apellidos,contrasenia){
        let patronNombres=/^([A-ZÁÉÍÓÚÑ]{1}[a-záéíóúñA-ZÁÉÍÓÚÑ]{1,25})(( |-)[a-záéíóúñA-ZÁÉÍÓÚÑ]{1,25})*$/;
        let patronContrasenia=/^(?=.*[A-ZÉÍÓÚÑ])(?=.*[0-9])[a-záéíóúñA-ZÁÉÍÓÚÑ0-9]{4,20}$/;

        $('[name="nombre"]').removeClass('is-invalid');
        $('input:eq(1)').removeClass('is-invalid');
        $('input:eq(3)').removeClass('is-invalid');
        $('#mensaje').addClass('text-danger');
        $('#mensaje').text("");

        if(!patronNombres.test(nombre)){
            $('[name="nombre"]').addClass('is-invalid');
            $('#mensaje').text("El nombre solo puede contener letras, debe tener entre 2 y 25 caracteres y no" 
            + " puede tener un espacio al final. Si es compuesto, la primera letra del primer nombre debe ir" 
            + " con mayúscula.");
        }
        else if(!patronNombres.test(apellidos)){
            $('input:eq(1)').addClass('is-invalid');
            $('#mensaje').text("Los apellidos solo pueden contener letras, la primera letra del primer" + 
            " apellido debe ir en mayúscula y cada palabra debe tener entre 2 y 25 caracteres.");
        }
        else if(!patronContrasenia.test(contrasenia)){
            $('input:eq(3)').addClass('is-invalid');
            $('#mensaje').text("La contraseña debe tener solo letras y números, entre 4 y 20 caracteres, y "+
            "una letra mayúscula o un número como mínimo.");
        }
        else{
            return 'Todo ok';
        }
    }
/* --------------------------------------------------------------------------------------------------------- */


    // Página de inicio

    function mostrar_notificacion(type,mensaje,ruta){
        $('#mostrar_alerta').css('display', 'block');
        $('#mensaje_alerta').text(mensaje);

        return new Promise((resolve, reject) => {
            if (type == "alert") {
                $('#eliminar_producto').hide();
                $('#cerrar_alerta').click(function () {
                    $('#mostrar_alerta').css('display', 'none');
                    resolve(false);  // La promesa se resuelve con false cuando se cierra la alerta
                    if(ruta != ''){
                        location.href = ruta
                    }
                });
            }
            else {
                let confirmar = false;
                $('#cerrar_alerta').text('No');
                $('#eliminar_producto').show();
            
                $('#eliminar_producto').click(function () {
                    $('#mostrar_alerta').css('display', 'none');
                    confirmar = true;
                    resolve(true);  // La promesa se resuelve con true cuando se hace clic en el botón de eliminación
                });
            
                $('#cerrar_alerta').click(function () {
                    $('#mostrar_alerta').css('display', 'none');
                    resolve(false);  // La promesa se resuelve con false cuando se cierra la alerta sin eliminar
                });
            }
        });
    }

    $('#link_logo').on('click',function(){
        window.location.href = '/'
    })

    $('#link_bebidas').on('click',function(){
        window.location.href = 'bebidas'
    })

    $('#link_aperitivos').on('click',function(){
        window.location.href = 'aperitivos'
    })
/* --------------------------------------------------------------------------------------------------------- */


    // Página de registro
    
    $('form[name=formularioRegistro]').submit(function(){
        event.preventDefault();
        
        let nombre=$('[name="nombre"]').val()
        let apellidos=$('[name="apellidos"]').val();
        let correo=$('[name="email"]').val();
        let contrasenia=$('[name="contraseña"]').val();
        let fechaNacimiento=$('[name="fechaNacimiento"]').val();

        if(compruebaDatos(nombre,apellidos,contrasenia) == 'Todo ok'){
            data = {
                "email" : correo
            }

            $.ajax({
                url: '/obtener_Id',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                    if($.isEmptyObject(response)){
                        registraUsuario(nombre,apellidos,correo,contrasenia,fechaNacimiento)
                    }
                    else{
                        $('#mensaje').text("Ya existe un usuario con el correo introducido. Inicie sesión o"+
                        " cambie el correo.");
                    }
                },
                error: function(error) {
                    console.log('Error:', error);
                }
            });
        }
    });

    function registraUsuario(nombre,apellidos,correo,contrasenia,fechaNacimiento){
        var datos = {
            nombre: nombre,
            apellidos: apellidos,
            correo: correo,
            contrasenia: contrasenia,
            fechaNacimiento: fechaNacimiento
        };

        $.ajax({
            url: '/registra_Usuario',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(datos),
            success: function(response) {
                console.log(response);

                $.ajax({
                    url: '/inicia_Sesion',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(datos),
                    success: function(response) {
                        if(response == "No existe."){
                            $('#mensaje').addClass('text-danger');
                            $('#mensaje').text("No existe un usuario con los datos introducidos.");
                        }
                        else{
                            mostrar_notificacion('alert',"Usuario registrado. "+response,'/')
                        }
                    },
                    error: function(error) {
                        console.log('Error:', error);
                    }
                });

            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }
/* --------------------------------------------------------------------------------------------------------- */


    // Página de inicio sesión
    
    $('form[name=formularioInicioSesion]').submit(function(){
        event.preventDefault();
        
        let nombre=$('[name="nombre"]').val();
        let correo=$('[name="email"]').val();
        let contrasenia=$('[name="contraseña"]').val();

        var datos = {
            nombre: nombre,
            correo: correo,
            contrasenia: contrasenia,
        };

        $.ajax({
            url: '/inicia_Sesion',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(datos),
            success: function(response) {
                if(response == "No existe."){
                    $('#mensaje').addClass('text-danger');
                    $('#mensaje').text("No existe un usuario con los datos introducidos.");
                }
                else{
                    mostrar_notificacion('alert',response,'/')
                }
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });

    });
/* --------------------------------------------------------------------------------------------------------- */


    // Cerrar sesión 

    $('[name="cerrarSesion"]').on('click',function(){
        event.preventDefault();

        $.ajax({
            url: '/cierra_Sesion',
            method: 'POST',
            contentType: 'application/json',
            success: function(response) {
                mostrar_notificacion('alert',response,'/');
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
/* --------------------------------------------------------------------------------------------------------- */


    // Modificar

    $('form[name=formularioModificar]').submit(function(){
        event.preventDefault();
            
        let nombre=$('[name="nombre"]').val()
        let apellidos=$('[name="apellidos"]').val();
        let correo=$('[name="email"]').val();
        let contrasenia="123Aa";
        let fechaNacimiento=$('[name="fechaNacimiento"]').val();

        if(compruebaDatos(nombre,apellidos,contrasenia)=='Todo ok'){
            let datos = {
                nombre : nombre,
                apellidos : apellidos,
                correo : correo,
                fechaNacimiento : fechaNacimiento,
            }
            
            $.ajax({
                url: '/actualiza_DatosUsuario',
                method: 'POST',
                contentType: 'application/json',
                data : JSON.stringify(datos),
                success: function(response) {
                    if(response == "Usuario actualizado."){
                        mostrar_notificacion('alert',response,'/');
                    }
                    else{
                        mostrar_notificacion('alert',"Error: existe otro usuario con el correo introducido.",'/formulario_Modificar.html');
                    }
                },
                error: function(error) {
                    console.log('Error:', error);
                }
            });

        }
    });
/* --------------------------------------------------------------------------------------------------------- */


    // Dar de baja

    $('form[name=formularioEliminar]').submit(function(){
        event.preventDefault();
        
        if(confirm("¿Está seguro de querer eliminar el usuario?")){
            let contrasenia = $('[name="contraseña"]').val();

            let data = {
                contrasenia : contrasenia
            }

            $.ajax({
                url: '/da_deBaja',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                    if(response == "Usuario eliminado."){
                        mostrar_notificacion('alert',response,'/')
                    }
                    else{
                        $('#mensaje').addClass('text-danger');
                        $('#mensaje').text(response);
                    }
                    
                },
                error: function(error) {
                    console.log('Error:', error);
                }
            });
        }
    });
/* --------------------------------------------------------------------------------------------------------- */


    // Agregar producto
    
    // Muestra diferentes tipos de productos dependiendo de si se ha escogido un aperitivo o una bebida 
    $('#categoria1').hide();
    $('#categoria2').hide();
    $('#tipoProducto1').on('input',function(){
        let producto = $('#tipoProducto1').val();
        
        if(producto == "aperitivos"){
            $('#categoria2').hide();
            $('#categoria1').show();
        }
        else{
            $('#categoria1').hide();
            $('#categoria2').show();
        }
    });

    $('#formularioAgregarProducto').submit(function(event){
        event.preventDefault();
    
        let tipoProducto1 = $('#tipoProducto1').val();
        let nombreProducto = $('#nombreProducto').val();
        let descripcionProducto = $('#descripcionProducto').val();
        let estado = $('#estado').val();
        let precio = $('#precio').val();

        // Obtener imagen
        let imagenInput = $("#imagen")[0];
        let imagenFile = imagenInput.files[0];

        // Obtener terminación imagen
        let nombreImagen = imagenFile.name;
        let terminacionImagen = '';
        for(i=nombreImagen.length-1;i>=1;i--){
            if(nombreImagen[i] == '.'){
                break
            }
            terminacionImagen = nombreImagen[i] + terminacionImagen;
        }

        // Para garantizar la mayor compatibilidad con diferentes navegadores, se admiten solo los siquientes
        // formatos de imágnes:
        let encaja = false; 
        let terminacionesImagenes = ['jpg','jpeg','png','gif','svg','webp']; 
        for(i=0;i<terminacionesImagenes.length;i++){
            // Si la terminación encaja, agrega el producto
            if(terminacionImagen == terminacionesImagenes[i]){
                encaja = true;
                let formData = new FormData();
                formData.append("imagen", imagenFile);
        
                let tipoProducto2 = (tipoProducto1 == 'aperitivos') ? $('[name="tipoAperitivo"]').val() : $('[name="tipoBebida"]').val();
                
                if(tipoProducto1 == '' || estado == '' || tipoProducto2 == ''){
                    mostrar_notificacion('alert','Debe rellenar todos los campos','');
                }
                else{
                    let datos = {
                        tipoProducto1: tipoProducto1,
                        nombreProducto: nombreProducto,
                        descripcionProducto: descripcionProducto,
                        estado: estado,
                        precio: precio,
                        tipoProducto2: tipoProducto2,
                    };
                
                    formData.append("datos", JSON.stringify(datos));
                
                    $.ajax({
                        method: "POST",
                        url: "/agregar_producto",
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            mostrar_notificacion('alert',response,'/admin_principal');
                        },
                        error: function (error) {
                            console.error(error);
                        }
                    });
                }
            }
        }
        // Si la terminación no encaja informa
        if (!encaja){
            mostrar_notificacion('alert','Archivo/imagen no valido','');
        }
    });
/* --------------------------------------------------------------------------------------------------------- */


    // Carrito compra 
    
    // Añade producto a la sesión

    $('.producto').submit(function(){
        event.preventDefault();

        // Guarda la ruta relativa de la imagen no la absoluta
        let rutaImg = this.children[0].src;
        var inicio = rutaImg.indexOf("static");
        let nuevaRutaImg = rutaImg.substring(inicio);

        let nombreProducto = this.children[1].children[0].textContent;
        let precioProducto = this.children[1].children[2].textContent;
        let boton = this.children[1].children[3];
        $.ajax({
            method: "GET",
            url: "/sesion_Iniciada",
            contentType: 'application/json',
            success: function (response) {
                if(response == 'Sesión iniciada'){
                    boton.value = 'Añadido a la cesta';
                    boton.type = 'text';
                    boton.setAttribute('readonly','');
                    let cantidad = 1;

                    añadeProducto(nuevaRutaImg,nombreProducto,precioProducto,cantidad);
                }
                else{
                    mostrar_notificacion('alert',"Inicie sesión para continuar.",'/formulario_InicioSesion.html');
                }
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
    
    function añadeProducto(rutaImg,nombreProducto,precioProducto,cantidad){
        datos = {
            rutaImg : rutaImg,
            nombreProducto : nombreProducto,
            precioProducto : precioProducto,
            cantidad : cantidad
        }

        $.ajax({
            method: "POST",
            url: "/añade_Producto",
            contentType: 'application/json',
            data: JSON.stringify(datos),
            success: function (response) {
                console.log(response);
                comportamientoCirculo();
            },
            error: function (error) {
                console.error(error);
            }
        });

    }

    // Comportamiento del círculo que indica el número de productos que hay en el carrito 

    comportamientoCirculo();

    function comportamientoCirculo(){
        $.ajax({
            url: 'dame_CarritoCompra',
            type: 'GET',
            success: function (response) {
                // Si no hay productos en session['carrito'] se oculta el circulo
                if(response.length != 0){
                    $('.circulo').show();
                    $('.textoCirculo').text(response.length);
                    $('.textoCirculo').text(response.length);
                }
            },
            error: function () {
                console.error('Error en la petición');
            }
        });
    }

    // Impide que se pueda seleccionar el producto añadido a la sesión en la interfaz y establece el precio 
    // total de los productos que hay en la sesión

    $.ajax({
        url: 'dame_CarritoCompra',
        type: 'GET',
        success: function (response) {
            console.log(response)

            let carritoCompra = response;
            let precioTotal = 0;
            Array.from($('form')).forEach(function(element){
                let elementoLegend = $(element).find('legend');
                if (elementoLegend.length > 0) {
                    let contenidoLegend = elementoLegend.text();

                    Array.from(carritoCompra).forEach(function(element2){
                        if(element2.nombreProducto == contenidoLegend){
                            let elementoInput = $(element).find('input');
                            elementoInput.attr('value','Añadido a la cesta');
                            elementoInput.attr('type','text');
                            elementoInput.attr('readonly','');
                        }
                    });
                }
            });

            Array.from(carritoCompra).forEach(function(element2){
                precioTotal += parseFloat(element2.precioTotalProducto);
            });
            $('#precioTotal').text(precioTotal.toFixed(2) + " €");
        },
        error: function () {
            console.error('Error en la petición');
        }
    });

    // Si la cantidad del producto es igual a cero el producto se elimina del carrito, sino se muestra el 
    // nuevo precio total de los productos
    $('.cantidad').change(function(){
        let elementoPadre = $(this).parent();
        let nombreProducto = elementoPadre.children().eq(1).val();
        let cantidad = this.value;
        // Elimina producto
        if(cantidad == 0){
            elementoPadre.text("");
            
            let datos = {
                nombreProducto : nombreProducto
            }

            $.ajax({
                method: "POST",
                url: "/elimina_ProductoSesion",
                contentType: 'application/json',
                data: JSON.stringify(datos),
                success: function (response) {
                    console.log(response);
                    location.reload();
                },
                error: function (error) {
                    console.error(error);
                }
            });
        }
        // Modifica producto
        else{
            let datos = {
                nombreProducto : nombreProducto,
                cantidad : cantidad
            }
            
            $.ajax({
                method: "POST",
                url: "/modifica_ProductoSesion",
                contentType: 'application/json',
                data: JSON.stringify(datos),
                success: function (response) {
                    console.log(response);
                    location.reload();
                },
                error: function (error) {
                    console.error(error);
                }
            });
        }
    });

    // Finalizar compra

    $('#finalizarCompra').on('click',function(){
        event.preventDefault();

        $.ajax({
            method: "POST",
            url: "/haz_Compra",
            contentType: 'application/json',
            success: function (response) {
                mostrar_notificacion('alert',response,'/');
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
/* --------------------------------------------------------------------------------------------------------- */


    // Productos más frecuentes

    $('#botonCerrar').on('click', function() {
        $('#productosMasFrecuentes').empty();
    }); 
/* --------------------------------------------------------------------------------------------------------- */

    // Botones atrás

    // Botón 'atrás' en los formularios de registro, inicio sesión, modificar y eliminar
    $('#atras').on('click', function () {
        window.location.href = '/';
    });

    // Botón 'atrás' en los formularios de agregar producto, modificar/eliminar bebida y modificar/eliminar 
    // aperitivo
    $('#atras2').on('click', function (event) {
        event.preventDefault();
        window.location.href = '/admin_principal';
    }); 
/* --------------------------------------------------------------------------------------------------------- */


     ////////MODIFICAR BEBIDA
    $(".modificar_bebida").click(function(){
        $(".dialog").hide();
        console.log("Click  en modificar");
        let idDialog = $(this).data('id')
        let id = '#'+idDialog
        let editable = '.editable_bebidas'+idDialog
        let boton_guardar = '#guardar_cambios_bebidas'+idDialog
        console.log("Mostrando el cuadro de diálogo con ID:", id);
        $(id).show();
        $(id).focus();
        $(editable).on('input', function () {
            cambiosPendientesBebidas = true; 
            habilitarDeshabilitarBotonGuardarCambiosBebidas(); 
        });

        function habilitarDeshabilitarBotonGuardarCambiosBebidas() {
            let botonGuardarCambios = $(boton_guardar); 
        
            if (cambiosPendientesBebidas) {
                botonGuardarCambios.prop('disabled', false); 
            } else {
                botonGuardarCambios.prop('disabled', true); 
            }
        }

        function obtenerCambiosPendientesBebidas() {
            let cambios = [];
    
            $(editable).each(function () {
                let input = $(this);
                let id = input.data('id');
                let field = input.data('field');
                let newValue = input.val();
                let originalValue = input.data('original-value');
    
                if (field == 'estado') {
                    let selectedOption = input.find('option:selected');
                    newValue = selectedOption.val();
                }
                if (newValue != originalValue) {
                    cambios.push({ id: id, field: field, value: newValue, producto: 'bebida' });
                }
    
            });
    
            return cambios;
        }

        $(boton_guardar).on('click', function () {
            if (cambiosPendientesBebidas) {
        
                let cambios = obtenerCambiosPendientesBebidas();
        
                $.ajax({
                    method: "POST",
                    url: "/modificar_bebida",
                    contentType: 'application/json',
                    data: JSON.stringify(cambios),
                    success: function (data) {
                        console.log('Cambios guardados: ' + data);
                        cambiosPendientesBebidas = false; 
                        habilitarDeshabilitarBotonGuardarCambiosBebidas(); // Deshabilita el botón
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            } else {
                // No hay cambios pendientes, no es necesario realizar la solicitud Ajax.
                console.log('No hay cambios pendientes.');
            } 
        });

    });
    
    $(".cerrar_dialog_bebida").click(function(){
        console.log("Clic en cerrar_dialog");
        let idDialog = $(this).data('id')
        let id = '#'+idDialog
        console.log("Cerrando el cuadro de diálogo con ID:", id);
        $(id).hide();
    });

    ////////MODIFICAR APERITIVO
    $(".modificar_aperitivo").click(function(){
        $(".dialog").hide();
        console.log("Clic en modificar");
        let idDialog = $(this).data('id')
        let id = '#'+idDialog
        let editable = '.editable_aperitivos'+idDialog
        let boton_guardar = '#guardar_cambios_aperitivos'+idDialog
        console.log("Mostrando el cuadro de diálogo con ID:", id);
        $(id).show();
        $(id).focus();
        $(editable).on('input', function () {
            cambiosPendientesAperitivos = true; 
            habilitarDeshabilitarBotonGuardarCambiosAperitivos(); 
        });


        function habilitarDeshabilitarBotonGuardarCambiosAperitivos() {
            let botonGuardarCambios = $(boton_guardar); 
        
            if (cambiosPendientesAperitivos) {
                botonGuardarCambios.prop('disabled', false); 
            } else {
                botonGuardarCambios.prop('disabled', true); 
            }
        }

        function obtenerCambiosPendientesAperitivos() {
            let cambios = [];
    
            $(editable).each(function () {
                let input = $(this);
                let id = input.data('id');
                let field = input.data('field');
                let newValue = input.val();
                let originalValue = input.data('original-value');
    
                if (field == 'estado') {
                    let selectedOption = input.find('option:selected');
                    newValue = selectedOption.val();
                }
                if (newValue != originalValue) {
                    cambios.push({ id: id, field: field, value: newValue, producto: 'aperitivo' });
                }
    
            });
    
            return cambios;
        }

        $(boton_guardar).on('click', function () {
   
            if (cambiosPendientesAperitivos) {
                let cambios = obtenerCambiosPendientesAperitivos();
                console.log(cambios);
        
                $.ajax({
                    method: "POST",
                    url: "/modificar_aperitivo",
                    contentType: 'application/json',
                    data: JSON.stringify(cambios),
                    success: function (data) {
                        console.log(data);
                        console.log('Cambios guardados: ' + data);
                        cambiosPendientesAperitivos = false;
                        habilitarDeshabilitarBotonGuardarCambiosAperitivos();
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            } else {
                // No hay cambios pendientes, no es necesario realizar la solicitud Ajax.
                console.log('No hay cambios pendientes.');
            } 
        });  

    });

    $(".cerrar_dialog_aperitivo").click(function(){
        console.log("Clic en cerrar_dialog");
        let idDialog = $(this).data('id')
        let id = '#'+idDialog
        console.log("Cerrando el cuadro de diálogo con ID:", id);
        $(id).hide();
    });

    ////////ELIMINAR PRODUCTO   
    $(".eliminar").click(function(){
        let idProducto = $(this).data('id');
        let producto = $(this).data('producto');
        
        mostrar_notificacion('confirm', '¿Estás seguro de que deseas eliminar este producto?').then((confirmar) => {
            console.log(confirmar); // Este console.log se ejecuta cuando la promesa se resuelve
    
            let datos = [{id: idProducto, producto: producto}];
            console.log(datos);
            if (confirmar) {
                $.ajax({
                    method: "POST",
                    url: "/eliminar_"+encodeURIComponent(producto),
                    contentType: 'application/json',
                    data: JSON.stringify(datos),
                    success: function (data) {
                        console.log('Producto eliminado: ' + data);
                        location.reload();
                    },
                    error: function (error) {
                        console.error(error);
                    }
                });
            }
        });
    });

       
    // Busqueda de productos

    $("#buscador").on("input", function () {
        var consulta = $(this).val();

        $.ajax({
            type: "POST",
            url: "/busca_producto",
            data: { producto: consulta },
            success: function (data) {
               // Obtengo todas las conincidencias con la letra o palabra que ingresa el usuario

                let listaDatalist = $("#listaProEncontrados");
                console.log(data)
                // Limpia el datalist antes de agregar nuevas opciones
                listaDatalist.empty();
                // Itero data con un forEach para obtener el nombre del producto
                data.forEach(function(producto) {
                    // Agrego con append() en listadatalist la etiqueta option con el nombre del porducto como valor
                    let opcion = $("<option>").attr("value", producto);
                    listaDatalist.append(opcion);
                });
            },
            error: function (error) {
                console.error(error);
            }
        });

    });


    //ENTREGAR Y CANCELAR PEDIDO    

    $('.entregado').on('click',function(){
        let id = $(this).data('id')
        $.ajax({
            type: "POST",
            url: "/entregar_pedido",
            data: { idUsuario: id },
            success: function (data) {
               $(`.${id}`).text('Entregado');
               $(`.${id}`).css("color", "blue");

               mostrar_notificacion('alert','Pedido entregado.','/vista_pedido_admin');
            },
            error: function (error) {
                console.error(error);
            }
        });
    });

    $('.cancelar').on('click',function(){
        let id = $(this).data('id')
        $.ajax({
            type: "POST",
            url: "/cancelar_pedido",
            data: { idUsuario: id },
            success: function (data) {
               $(`.${id}`).text('Cancelado');
               $(`.${id}`).css("color", "red");

               mostrar_notificacion('alert','Pedido cancelado','/vista_pedido_admin');
            },
            error: function (error) {
                console.error(error);
            }
        });
    });
});