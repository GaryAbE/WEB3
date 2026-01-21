from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL 
import MySQLdb.cursors  #permite devolver un diccionario despues de ejecutar una consulta SQL
from datetime import date

app = Flask(__name__)

#configurar el acceso a la BD mysql
# host  user  password  BD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'ventas'

conexion = MySQL(app)

#CRUD de la tabla clientes
#Listado de clientes (lectura de la tabla clientes)
@app.route("/clientes")
def lista_clientes():
    #abrimos la conexion con la BD 
    #cursor = conexion.connection.cursor() #devuelve una lista de resultados despues de ejecutar una conuslta SQL
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) #devuelve un diccionario despues de ejecutar una consulta SQL
    #cadena sql 
    sql = "SELECT * FROM clientes"
    #ejecucion del SQL
    cursor.execute(sql)  # les devuelve una lista de resutados [...]  
    #la funcion fetchall trae todos los registros de la consulta SQL
    clientes = cursor.fetchall() #clientes es una lista
    cursor.close() #cerrar la conexion
    return render_template("clientes.html", datosClientes = clientes)


#Adicion o insercion de un nuevo cliente 
@app.route("/clientes/nuevo",methods=['GET','POST'])
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form['nombre']
        email = request.form['email']

        cursor = conexion.connection.cursor()
        sql = "INSERT INTO clientes (nombre, email) VALUES (%s, %s)"
        cursor.execute(sql,(nombre,email))
        #confirmar la accion de insertar un nuevo registro
        conexion.connection.commit()
        cursor.close()
        return redirect(url_for('lista_clientes'))
    else:
        return render_template("formulario_cliente.html")

#Eliminar a cliente
@app.route("/clientes/eliminar/<int:id_cliente>")
def elimina_cliente(id_cliente):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(sql,(id_cliente,))
        conexion.connection.commit()
        cursor.close()
        return redirect(url_for('lista_clientes'))
    except:
        return "No se puede eliminar al cliente!!!"

@app.route("/clientes/modificar/<int:id_cliente>" ,methods=['GET','POST'])
def modificar_cliente(id_cliente):
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
        return redirect(url_for('lista_clientes'))
    else:
        sql="SELECT * FROM clientes WHERE id_cliente = %s"
        cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql,(id_cliente,))
        cliente = cursor.fetchone()
        cursor.close()
        return render_template("formulario_modificar_cliente.html",cliente = cliente)

#NUEVA COMPRA (INSERT EN LA TABLA COMPRA)
def listado_clientes():
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) #devuelve un diccionario despues de ejecutar una consulta SQL
    sql = "SELECT * FROM clientes"
    #ejecucion del SQL
    cursor.execute(sql)  # les devuelve una lista de resutados [...]  
    #la funcion fetchall trae todos los registros de la consulta SQL
    clientes = cursor.fetchall() #clientes es una lista
    cursor.close() #cerrar la conexion
    return clientes

def listado_tiendas():
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) #devuelve un diccionario despues de ejecutar una consulta SQL
    sql = "SELECT * FROM tiendas"
    #ejecucion del SQL
    cursor.execute(sql)  # les devuelve una lista de resutados [...]  
    #la funcion fetchall trae todos los registros de la consulta SQL
    tiendas = cursor.fetchall() #clientes es una lista
    cursor.close() #cerrar la conexion
    return tiendas


@app.route("/compras/nuevo", methods=['GET','POST'])
def nueva_compra():
    if request.method == 'POST':
        #LOGICA PARA INSERTAR DATOS EN LA TABLA COMPRA
        id_cliente = request.form['id_cliente']
        id_tienda = request.form['id_tienda']
        monto = request.form['monto']
        fecha_compra = date.today() #aaa-mm-dd

        sql = "INSERT INTO compras (id_cliente, id_tienda, monto, fecha) VALUES (%s, %s, %s, %s)"
        cursor = conexion.connection.cursor();
        cursor.execute(sql,(id_cliente, id_tienda, monto, fecha_compra))
        conexion.connection.commit()
        return redirect(url_for('lista_clientes'))
        pass
    else:
        clientes = listado_clientes()
        tiendas = listado_tiendas()
        return render_template("formulario_compra.html", clientes = clientes, tiendas = tiendas)

@app.route("/saludo")
def saludo():
    return "Hola mundo desde Flask!!"

#ruta con parametro
@app.route("/usuario/<nombre>")
def nuevo(nombre):
    return f"Otro {nombre} saludo desde flask"

@app.route("/dato/<int:num1>/<int:num2>")
def suma(num1, num2):
    c = num1 + num2
    return f"la suma es {c} como resultado"

@app.route("/operacion/<int:num>")
def tabla_multiplicar(num):
    res = ""
    for i in range(1,11):
        res = res + f"{num} * {i} = {num*i}<br>"
    return res

@app.route("/api/info")
def api_info():
    return{"curso":"flask", "nivel":"basico", "activo": True}

@app.route("/")
def inicio():
    return "pagina de inicio"

@app.route("/about")
def acerca():
    return "Acerca de esta aplicacion"

@app.route("/html/<nombre>")
def pagina_html(nombre):
    return render_template("index.html",nombre=nombre)

@app.route("/operacionMejorada/<int:num>")
def tabla_multiplicar2(num):
    return render_template("tabla.html", numero=num)

if __name__ == "__main__":
    app.run(debug=True)
