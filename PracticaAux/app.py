
from flask import Flask, render_template, request,redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = ''
app.config ['MYSQL_DB'] = 'ventas'
conexion = MySQL(app) 
#MySQL -u root
#create database ventas;
#exit
#mysql -u root ventas < ventas.sql
@app.route("/")
def home():
    return "Hola mundo desde flask!"

@app.route("/about")
def about():
    return "Ruta de informacion"

@app.route("/contact")
def contact():
    return "Ruta de contacto"

@app.route("/usuarios/<nombre>")
def usuarios(nombre):
    return f"Hola {nombre}, bienvenido"

@app.route("/suma/<int:a>/<int:b>")
def suma(a, b):
    return f"La suma de {a} + {b} es {a + b}"

@app.route("/float/<float:a>")
def float_route(a):
    return f"El precio es {a}"

@app.route("/api/info")
def info():
    return {
        "app": "Flask",
        "version": "x.x",
        "author": "Yio"
    }

@app.route("/lista_clientes")
def lista_clientes():
    cursor =conexion.connection.cursor() #c[0]
    sql="SELECT id_cliente, nombre, email FROM clientes Order BY 1 DESC"
    cursor.execute(sql) #ejecutar la consulta --> sql

    datos=cursor.fetchall() #traer los datos de la consulta
    cursor.close() #cerrar la conexion
    print("lista_clientes", datos)
    return render_template("clientes.html", clientes=datos, title="Clientes array")

@app.route("/clientes-lista")
def lista_clientes():
     cursor =conexion.connection.cursor(MySQLdb.cursors.dictcursors) #c[0]
     sql="SELECT id_cliente, nombre, email FROM clientes Order BY 1 DESC"
     cursor.execute(sql) #ejecutar la consulta --> sql

     datos=cursor.fetchall() #traer los datos de la consulta
     cursor.close() #cerrar la conexion
     print("lista_Clientes (Diccionario)", datos)
     return render_template("clientes-json.html", clientes=datos, total=len(datos), title="Clientes JSON")

if __name__ == "__main__":
    app.run(debug=True)