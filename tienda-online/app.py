import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
from datetime import date
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img'
# mysql conecction
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tienda_ropa'
mysql = MySQL(app)


# settings
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/foro')
def foro():
    cur = mysql.connection.cursor()
    cur.execute('SELECT tema.*, cliente.nombre, cliente.avatar FROM (tema INNER JOIN cliente ON tema.idcliente = cliente.idcliente) ORDER BY idtema desc')
    data = cur.fetchall()

    cur.execute('SELECT comentarios.*,cliente.nombre, cliente.avatar FROM (comentarios INNER JOIN cliente ON comentarios.idcliente = cliente.idcliente) ORDER BY idcomentario desc')
    data1 = cur.fetchall()

    cur.execute('SELECT avatar FROM cliente WHERE email = %s',[email_user])
    image = cur.fetchall()
    
    cur.execute('SELECT *FROM cliente WHERE email = %s',[email_user])
    usuario = cur.fetchall()
    nameC = usuario[0][1]
    direcC = usuario[0][2]
    return render_template('foro.html', correos = email_user, temas = data, comentarios = data1, imagen = image[0][0], nombre = nameC, direc = direcC)

@app.route('/avatar', methods = ['POST'])
def avatar():
    if request.method == 'POST': 
        avatar = request.files['archivo']
     
        filename =secure_filename(avatar.filename)
        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        file = "../static/img/"+filename
       
        cur = mysql.connection.cursor()
        cur.execute("UPDATE cliente SET avatar=%s WHERE email = %s",(file, email_user))
        mysql.connection.commit()
        return redirect(url_for('foro'))

@app.route('/tema', methods = ['POST'])
def tema():
    if request.method == 'POST':
        comentario = request.form['addComment']
        video = request.form['uploadMedia']
        fecha = date.today()
        if(video == ""):
            video = None
            nuevoVideo = ""
        else:    
            video_form = video.partition("watch?v=")
            nuevoVideo1 = video_form[0]+"embed/"+video_form[2]
            nuevoVideo2 = nuevoVideo1.partition("&t=")
            nuevoVideo = nuevoVideo2[0]+"?start="+nuevoVideo2[2]
          
            
        print(nuevoVideo)    
        email = email_user
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT idcliente FROM cliente WHERE email=%s',[email])
        data = cur.fetchall()
        cur.execute('INSERT INTO tema (descripcion,video,fecha,idcliente) VALUES(%s ,%s ,%s, %s)',(comentario,nuevoVideo, fecha, data[0][0]))
        mysql.connection.commit()
        return redirect(url_for('foro'))

@app.route('/comentar', methods=['POST'])
def comentar():
    if request.method == 'POST':
        comentario = request.form['addComment']
        video = request.form['uploadMedia']
        tema = request.form['tema']
        fecha = date.today()
        if(video == ""):
            video = None
            nuevoVideo = ""
        else:
            video_form = video.partition("watch?v=")
            nuevoVideo1 = video_form[0]+"embed/"+video_form[2]
            nuevoVideo2 = nuevoVideo1.partition("&t=")
            nuevoVideo = nuevoVideo2[0]+"?start="+nuevoVideo2[2]
           
            

        email = email_user
        print(nuevoVideo)
        cur = mysql.connection.cursor()
        cur.execute('SELECT idcliente FROM cliente WHERE email=%s',[email])
        data = cur.fetchall()
        cur.execute('INSERT INTO comentarios (descripcion,video,fecha,idcliente,idtema) VALUES(%s ,%s ,%s, %s, %s)',(comentario,nuevoVideo, fecha, data[0][0],tema))
        mysql.connection.commit()
        return redirect(url_for('foro'))

@app.route('/store')
def Store():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE stock > %s LIMIT %s',(0,3))
    data = cur.fetchall()
    print(data)
    
    cur.execute('SELECT *FROM categoria')
    category = cur.fetchall()
    cur.execute('SELECT *FROM categoria')
    category = cur.fetchall()
    return render_template('store.html', productos = data, correos = email_user, categorias = category)


@app.route('/anuncios')
def Anuncio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE stock > %s',[0])
    data = cur.fetchall()

    cur.execute('SELECT *FROM categoria')
    category = cur.fetchall()

    return render_template('anuncios.html', productos = data, correos = email_user,categorias = category)

@app.route('/Search', methods = ['POST'])
def Search():
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        categoria = request.form['categoria']
        print("ESTA ES LA CATEGORIA",categoria)
        if busqueda == '':
            if categoria == "0":
                cur = mysql.connection.cursor()
                cur.execute('SELECT *FROM productos')
                data = cur.fetchall()
                print("1")
            elif categoria =="a":
                cur = mysql.connection.cursor()
                cur.execute('SELECT *FROM productos')
                data = cur.fetchall()
            else:
                cur = mysql.connection.cursor()
                cur.execute('SELECT *FROM productos WHERE idcategoria = %s',[categoria])
                data = cur.fetchall()
                print("2")
        else:
            if categoria == "0" or categoria == "a":
                cur = mysql.connection.cursor()
                sql='SELECT *FROM productos WHERE nombre LIKE %s'
                args=['%'+busqueda+'%']
                cur.execute(sql,args)
                data = cur.fetchall()
                print("3")
            elif categoria !="0":
                cur = mysql.connection.cursor()
                sql='SELECT *FROM productos WHERE nombre LIKE %s AND idcategoria =%s'
                args=['%'+busqueda+'%']
                cur.execute(sql,(args,categoria))
                data = cur.fetchall()
                print("4")
            else:
                cur.execute('SELECT *FROM productos')
                data = cur.fetchall()
                print("5")
            
        cur.execute('SELECT *FROM categoria')
        category = cur.fetchall()

        return render_template('anuncios.html', productos = data, correos = email_user, categorias = category)    
              
@app.route('/history')
def history():
    cur = mysql.connection.cursor()
    cur.execute('SELECT idcliente FROM cliente WHERE email =%s',[email_user])
    data = cur.fetchall()
    identificador = data[0][0]
    cur.execute('SELECT * FROM ventas WHERE idcliente = %s order by fecha desc',[identificador])
    ventana = cur.fetchall()
    cur.execute('SELECT detalle_pedido.cantidad, detalle_pedido.subtotal, productos.nombre,productos.imagen,productos.precio_u, detalle_pedido.idhistorial FROM (ventas INNER JOIN cliente ON ventas.idcliente = cliente.idcliente) INNER JOIN detalle_pedido ON ventas.idhistorial = detalle_pedido.idhistorial INNER JOIN productos ON detalle_pedido.idproducto = productos.idproducto WHERE ventas.idcliente =%s',[identificador])
    pasado = cur.fetchall()

    return render_template('foros.html', ventas = ventana, pasados = pasado,correos=email_user)
@app.route('/datos')
def Datos():
    cur = mysql.connection.cursor()
    dato = email_user
    cur.execute('SELECT *FROM cliente WHERE email LIKE %s', [dato])
    data = cur.fetchall()
    print (data[0])
    return render_template('datos.html', correos = email_user, infos = data[0])

@app.route('/datos_change', methods = ['POST'])
def Datos_change():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        email = request.form['email']
        cur = mysql.connection.cursor()
        global email_user
        verificacion = email_user
        cur.execute('SELECT idcliente FROM cliente WHERE email = %s', [verificacion])

        global id_cli 
        id_cli = cur.fetchall()
       
        cur.execute('UPDATE cliente SET nombre = %s, email = %s, direccion = %s WHERE email = %s', (nombre, email, direccion, verificacion))
        mysql.connection.commit()
        
        email_user = email
        return redirect(url_for('Datos'))

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html', correos = email_user)

@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        global email_user
        email_user = request.form['email']
        password = request.form['password']
        try:  
            cur = mysql.connection.cursor()
            cur.execute('SELECT email, contraseña, idcliente FROM cliente WHERE email LIKE %s AND contraseña LIKE %s', (email_user, password))
            confirmN = cur.fetchall()
            
            if confirmN[0][0] == email_user and confirmN[0][1] == password:
                global id_cliente
                id_cliente = confirmN[0][2]
                print(id_cliente)
                return redirect(url_for('Store'))
        except :
            return redirect(url_for('Index'))
   

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['mail']
        password = request.form['pass']
        cpassword = request.form['cpass']
        name = request.form['nombre']
        if password == cpassword:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO cliente (nombre,email, contraseña) VALUES(%s ,%s ,%s)',(name,username, password))
            mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/cart')
def cart ():
    cur = mysql.connection.cursor()
    cliente = id_cliente
    cur.execute('SELECT productos.nombre, productos.precio_u, productos.imagen, carrito.cantidad, carrito.cantidad * productos.precio_u as Subtotal, id_carrito, productos.stock FROM (productos INNER JOIN carrito ON productos.idproducto = carrito.idproducto) WHERE carrito.idcliente = %s',[cliente])
    data = cur.fetchall()
    suma = 0
    

    for x in range(len(data)):
        suma = suma + data[x][4]
        
    
    print (data)
    return render_template('carrito.html', correos = email_user, productos = data, total = suma)

@app.route('/carrito', methods = ['POST'])
def carrito():
    if request.method == 'POST':
        global id_producto
        id_producto = request.form['id_producto']
        cliente = id_cliente
        cur = mysql.connection.cursor()
        cur.execute('SELECT idproducto FROM carrito WHERE idproducto = %s AND idcliente = %s',(id_producto,cliente))
        duplicado = cur.fetchall()
        cur.execute('SELECT stock FROM productos WHERE idproducto = %s',[id_producto])
        stock = cur.fetchall()
        
        if int(stock[0][0]) > 0 :
            print('ESTE ES EL STOCK')
    
            print(stock[0][0])
            if duplicado:
                cur.execute('SELECT cantidad FROM carrito WHERE idproducto =%s AND idcliente = %s',(id_producto,cliente))
                data = cur.fetchall()
                
                if int(data[0][0]) < int(stock[0][0]):
                    cantidad = data[0][0] + 1
                    
                    cur.execute('UPDATE carrito SET cantidad = %s WHERE idproducto =%s AND idcliente = %s ',(cantidad, id_producto, id_cliente))
                    mysql.connection.commit()
                
                
            else:
                cur.execute('INSERT INTO carrito (idcliente, idproducto, cantidad)VALUES(%s,%s,%s)',(cliente, id_producto, 1) )
                mysql.connection.commit()
            
            
        return redirect(url_for('cart'))

@app.route('/cancelar_compra', methods=['POST'])
def cancelar_compra():
    if request.method == 'POST':
        carrito = request.form['carrito1']
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM carrito WHERE id_carrito = %s',[carrito])
        mysql.connection.commit()
        flash('El carrito fue Actualizado Correctamente')
        return redirect(url_for('cart'))

@app.route('/editar_compra', methods=['POST'])
def editar_compra():
    if request.method == 'POST':
        carrito = request.form['carrito']
        cantidad = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE carrito SET cantidad = %s WHERE id_carrito = %s',(cantidad, carrito))
        mysql.connection.commit()
        flash('El carrito fue Actualizado Correctamente')
        return redirect(url_for('cart'))

@app.route('/comprar',methods = ['POST'])
def comprar():
    if request.method == 'POST':
        total = request.form['total']
        cliente = id_cliente
        fhora = datetime.now()
        estado = "Espera"
        if total == '0':
            return redirect(url_for('Anuncio'))
        else:
            
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO ventas (fecha, total, idcliente, estado) VALUES(%s,%s,%s,%s)',(fhora,total, cliente,estado))
            mysql.connection.commit()
            cur.execute('SELECT MAX(fecha) FROM ventas WHERE idcliente =%s',[cliente])
            fecha = cur.fetchall()
            cur.execute('SELECT idhistorial FROM ventas WHERE fecha = %s AND idcliente = %s',(fecha, cliente))
            historial = cur.fetchall()


        
            
            cur.execute('SELECT carrito.idproducto,precio_u, carrito.cantidad , stock FROM (productos INNER JOIN carrito ON productos.idproducto = carrito.idproducto) WHERE carrito.idcliente = %s ',[cliente])
            migrar = cur.fetchall()

            x = 0
            for x in range(len(migrar)):

                subtotal = int(migrar[x][1])* int(migrar[x][2])

                cur.execute('INSERT INTO detalle_pedido (idhistorial, idproducto, cantidad, subtotal) VALUES(%s,%s,%s,%s)',(historial,migrar[x][0],migrar[x][2],subtotal ))
                mysql.connection.commit()

                newStock = int(migrar[x][3])-int(migrar[x][2])
                print('es el nuevo stock')
                print(newStock)
                
                cur.execute('UPDATE productos SET stock = %s WHERE idproducto =%s ', (newStock,migrar[x][0]))
                mysql.connection.commit()
            
            cur.execute('DELETE FROM carrito WHERE idcliente =%s ',[cliente])
            mysql.connection.commit()

            return redirect(url_for('Store'))

# ADMINISTRACION --- TIENDA ROPA
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')
@app.route('/validar_adm', methods=['POST'])
def validar_adm():
    if request.method == 'POST':
        nombreUsuario = request.form['usuario']
        passUsuario = request.form['password']
        if nombreUsuario == "" or passUsuario == "":
            return redirect(url_for('admin_login'))
        try:  
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM administrador WHERE username = %s AND password = %s', (nombreUsuario, passUsuario))
            confirmN = cur.fetchall()
            
            if confirmN[0][1] == nombreUsuario and confirmN[0][2] == passUsuario:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('admin_login')) 
        except :
            return redirect(url_for('admin_login'))

@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute('SELECT productos.*, categoria.nombre FROM productos INNER JOIN categoria ON productos.idcategoria = categoria.idcategoria')
    data= cur.fetchall()
    cur.execute('SELECT *FROM categoria')
    category = cur.fetchall()
    return render_template('admin.html', productos = data, categorias = category)
@app.route('/ventas')
def ventas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ventas.*,cliente.nombre,cliente.direccion FROM ventas INNER JOIN cliente ON ventas.idcliente = cliente.idcliente ORDER BY ventas.fecha desc")
    data = cur.fetchall()
    
    cur.execute('SELECT detalle_pedido.cantidad, detalle_pedido.subtotal, productos.nombre,productos.imagen,productos.precio_u, detalle_pedido.idhistorial FROM (ventas INNER JOIN cliente ON ventas.idcliente = cliente.idcliente) INNER JOIN detalle_pedido ON ventas.idhistorial = detalle_pedido.idhistorial INNER JOIN productos ON detalle_pedido.idproducto = productos.idproducto')
    perUser = cur.fetchall()
    return render_template('ventas.html', ventas = data, articulos = perUser)
    
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT *FROM productos WHERE idproducto = %s', [id])
    data = cur.fetchall()
    print (data)
    return render_template('edit_producto.html', producto = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        stock = request.form['stock']
        precio = request.form['precio']
        imagen = request.files['archivo']
        descripcion = request.form['descripcion']
        if not imagen:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE productos
                SET nombre = %s,
                    stock = %s,
                    precio_u = %s,
                    descripcion = %s
                WHERE idproducto = %s
            """, (nombre,stock ,precio,descripcion , id))
            mysql.connection.commit()
            flash('Contact Updated Successfully')
        else:
            filename =secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            file = "../static/img/"+filename
            
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE productos
                SET nombre = %s,
                    stock = %s,
                    precio_u = %s,
                    imagen = %s,
                    descripcion = %s
                WHERE idproducto = %s
            """, (nombre,stock ,precio, file,descripcion , id))
            mysql.connection.commit()
            flash('Contact Updated Successfully')
        return redirect(url_for('admin'))
@app.route('/categorias')
def categorias():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    return render_template('categorias.html', categorias = data)
@app.route('/add_categoria',methods = ['POST'])
def add_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if nombre or nombre != "":
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO categoria(nombre) VALUES(%s) ',[nombre])
            mysql.connection.commit()
            flash('Categoria Agregada Satisfactoriamente')
        return redirect(url_for('categorias'))
@app.route('/edit_categoria', methods = ['POST'])
def edit_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE categoria SET nombre = %s WHERE idcategoria = %s',(nombre,categoria))
        mysql.connection.commit()
        flash('Categoria Editada Satisfactoriamente')
    return redirect(url_for('categorias'))

@app.route('/add_product', methods = ['POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        stock = request.form['stock']
        precio = request.form['precio']
        imagen = request.files['archivo']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        filename =secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        file = "../static/img/"+filename

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos(nombre,stock,precio_u,imagen,descripcion,idcategoria) VALUES(%s,%s,%s,%s,%s,%s)',(nombre,stock,precio,file,descripcion,categoria))
        mysql.connection.commit()
        flash('Producto Agregado Satisfactoriamente')
    return redirect(url_for('admin'))
@app.route('/edit_estado', methods=['POST'])
def edit_estado():
    if request.method == "POST":
        estado = request.form['estado']
        venta = request.form['venta']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE ventas SET estado = %s WHERE idhistorial = %s",(estado, venta))
        mysql.connection.commit()
        flash('Estado de la venta editado Satisfactoriamente')
    return redirect(url_for('ventas'))
if __name__ == '__main__':
    app.run(port = 3000, debug = True )

