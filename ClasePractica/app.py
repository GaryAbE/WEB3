from flask import Flask, abort, render_template, redirect, url_for, request, session 
from flask_mysqldb import MySQL #importar la librería para mysql
import MySQLdb.cursors #importar los cursores
from functools import wraps
from werkzeug.security import check_password_hash



app = Flask(__name__)
app.secret_key="MiClaveSegura"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas'
conexion = MySQL(app) 

def roles_required(*roles_permitidosgach):
    def deco(viewgach):
        @wraps(viewgach)
        def wrapped_viewgach(*argsgach,**kwargsgach):
            if 'user_id' not in session:
                print("iniciar sesion!!")
                return redirect(url_for('login'))
            rolgach=session.get('rol')
            if rolgach not in roles_permitidosgach:
                abort(403)
            return viewgach(*argsgach,**kwargsgach)
        return wrapped_viewgach
    return deco

@app.route("/Promedio")
@roles_required('admin')
def promediogach():
    cursorgach = conexion.connection.cursor(MySQLdb.cursors.DictCursor) 
    sqlgach = "SELECT cl.id_cliente, cl.nombre, COUNT(c.id_compra) AS total_compras, SUM(c.monto) AS total_gastado, AVG(c.monto) AS promedio_compra FROM clientes cl JOIN compras c ON cl.id_cliente = c.id_cliente GROUP BY cl.id_cliente, cl.nombre ORDER BY promedio_compra DESC;"
    cursorgach.execute(sqlgach)
    datos = cursorgach.fetchall()
    cursorgach.close()
    return render_template('promedioCompra.html', promediogach=datos)

@app.route("/comprasRegistradas")
@roles_required('operador')
def comprasgach():
    cursorgach = conexion.connection.cursor(MySQLdb.cursors.DictCursor) 
    sqlgach = "SELECT COUNT(*) AS total_compras, SUM(monto) AS total_monto FROM compras WHERE DATE(fecha) = CURDATE();"
    cursorgach.execute(sqlgach) 
    datosgach = cursorgach.fetchall()
    print(datosgach)
    return render_template('comprasRegistradas.html', comprasgach=datosgach) 



@app.route("/consulta")
@roles_required('admin')
def consulta():
    cursorgach = conexion.connection.cursor(MySQLdb.cursors.DictCursor) 
    sqlgach = "SELECT t.id_tienda, t.nombre, SUM(c.monto) AS total_ventas, COUNT(c.id_compra) AS total_compras FROM tiendas t JOIN compras c ON t.id_tienda = c.id_tienda GROUP BY t.id_tienda, t.nombre ORDER BY total_ventas DESC"
    cursorgach.execute(sqlgach)
    datos = cursorgach.fetchall()
    cursorgach.close()
    return render_template('consulta.html', consultagach=datos)

@app.route("/monto")
@roles_required('admin')
def monto():
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) 
    sqlgach = "SELECT cl.id_cliente, cl.nombre, SUM(c.monto) AS total_gastado FROM clientes cl JOIN compras c ON cl.id_cliente = c.id_cliente GROUP BY cl.id_cliente, cl.nombre ORDER BY total_gastado DESC LIMIT 10;"
    cursor.execute(sqlgach) 
    datos = cursor.fetchall()
    print(datos)
    return render_template('monto.html', montogach=datos) 

@app.route('/historial', methods=['GET', 'POST'])
@roles_required('operador')
def historial():
    datosgach=[]
    iniciogach=fingach= None
    if request.method == 'POST':
        iniciogach= request.form['iniciogach']
        fingach= request.form['fingach']
        cursorgach = conexion.connection.cursor(MySQLdb.cursors.DictCursor)
        sql= "SELECT c.id_compra, cl.nombre AS cliente, t.nombre AS tienda, c.fecha, c.monto FROM compras c JOIN clientes cl ON c.id_cliente = cl.id_cliente JOIN tiendas t ON c.id_tienda = t.id_tienda WHERE c.fecha BETWEEN %s AND %s ORDER BY c.fecha DESC"
        cursorgach.execute(sql, (iniciogach, fingach))
        datosgach= cursorgach.fetchall()
        cursorgach.close()
    return render_template('historial.html',historialgach=datosgach,iniciogach=iniciogach,fingach=fingach) 


@app.route('/clientes')
@roles_required('admin', 'operador')
def listar_clientes():
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) 
    sqlgach = "SELECT * FROM clientes" 
    cursor.execute(sqlgach) 
    datos = cursor.fetchall() 
    print(datos)
    return render_template('clientes.html', clientesgach=datos)

@app.route("/clientes/nuevo",methods=['GET','POST'])
@roles_required('admin')
def nuevo_clientegach():
    if request.method =='POST':
        nombre = request.form['nombre']
        email = request.form['email']

        cursor = conexion.connection.cursor()
        sql = "INSERT INTO clientes (nombre,email) VALUES (%s,%s)"
        cursor.execute(sql,(nombre,email))
        conexion.connection.commit() #confirmar la adicion de insretar un nuevo registro
        cursor.close()
        return redirect(url_for('listar_clientes')) 
    else:
        return render_template("formulario_cliente.html")
    
@app.route('/clientes/eliminar/<int:id_cliente>')
@roles_required('admin')
def elimina_clientegach(id_cliente):
    cursor = conexion.connection.cursor()
    sql = "DELETE FROM clientes WHERE id_cliente = %s"
    cursor.execute(sql,(id_cliente,))
    conexion.connection.commit()
    cursor.close()
    return redirect(url_for('listar_clientes'))

def login_required(viewgach):
    @wraps(viewgach)
    def wrapped_viewgach(*argsgach,**kwargsgach):
        if 'user_id' not in session:
            print("iniciar sesion")
            return redirect(url_for('login'))
        return viewgach(*argsgach, **kwargsgach)
    return wrapped_viewgach


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #logica
        nom_usuario = request.form["usuario"]
        password =request.form["password"]

        if not nom_usuario or not password:
            print("usuario y password son obligatorios")
            return redirect(url_for("login"))
        
        cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) #crear el cursor
        sql = "SELECT id, username, password_hash, nombre, activo, rol FROM usuarios WHERE username = %s" 
        cursor.execute(sql,(nom_usuario,)) 
        usuario=cursor.fetchone()
        cursor.close()

        if not usuario  or not usuario["activo"]:
            print("Usuario no valido o inacitvo")
            return redirect(url_for("login"))
        
        if not check_password_hash(usuario["password_hash"], password):
            print("contrase;a incorrecta")
            return redirect(url_for("login"))
        

        session['user_id']=usuario['id']
        session['username']=usuario['username']
        session['rol']=usuario['rol']
        print("siiii")

        return redirect(url_for('listar_clientes'))
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logoutgach():
    session.clear()
    print("session cerrada")
    return redirect(url_for("login"))


@app.route('/')
def saludo():
    return "Hola, bienvenido a mi API con Flask"





@app.route("/clientes/modificar/<int:id_cliente>" ,methods=['GET','POST'])
def modificar_clientegach(id_cliente):
    if request.method == 'POST':
        #LOGICA PARA ACTUZALIZAR EL CLIENTE
        nombre = request.form['nombre']
        correo = request.form['correo']
        sql = "UPDATE clientes SET nombre = %s, email = %s WHERE id_cliente = %s"
        cursor = conexion.connection.cursor()
        cursor.execute(sql,(nombre, correo, id_cliente))
        conexion.connection.commit()
        cursor.close()
        #pass
        return redirect(url_for('listar_clientes'))
    else:
        sql="SELECT * FROM clientes WHERE id_cliente = %s"
        cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql,(id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        return render_template("formulario_modificar_cliente.html",cliente = cliente)

if __name__ == '__main__':
    app.run(debug=True)