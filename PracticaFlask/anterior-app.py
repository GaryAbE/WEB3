from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL #importar la librería para mysql
import MySQLdb.cursors #permite devolver un diccionario despues de ejecutar una consulta sql


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']= '' 
app.config['MYSQL_DB']= 'ventas'

conexion =MySQL(app)

#CRUD de kla tabla de clientes
#listado de clientes

@app.route("/clientes")
def lista_clientes():
    #abrimos la conexion con la BD
    #MySQL.cursors.DictCursors devuelve una lista de resultados 
    cursor = conexion.connection.cursor(MySQL.cursors.DictCursors) 
    #cadena sql
    sql = 'SELECT * FROM clientes'
    #ejecucion del sql
    cursor.execute(sql)#les devuelbe una lista de resultados [...] cuando se utilaiza execute
    #la funcioon fechall trae todos los registros de la consulta SQL
    clientes= cursor.fetchall() #clientes es una lista
    cursor.close() # cerrrar la conexion
    return render_template("clientes.html", clientes=clientes)

@app.route('/')
def saludo():
    return "Hola, bienvenido a mi API con Flask"

@app.route('/suma/<int:a>/<int:b>')
def suma(a,b):
    return f"La suma es {a + b}"

@app.route('/calc/<int:a>/<int:b>/<op>')
def calcula(a,b, op):
    if op== 'suma':
        return f"La suma es {a+b}"
    if op=='resta':
        return f"La resta es {a-b}"
    if op=='multiplicacion':
        return f"La multiplicacion es {a*b}"
    if op=='division':
        return f"La division es {a/b}"
    
@app.route('/tabla/<int:n>')
def tabla(n):
    return render_template("tabla.html",num=n)

@app.route('/usuario/<nombre>/<int:edad>')
def api(nombre, edad):
    return {"nombre": nombre, "edad": edad, "estado": "activo"}

@app.route('/estudiantes/<materia>')
def estudiantes(materia):
    lista= ["Emmanuel", "Rodrigo", "Marcelo", "Sofía", "Ana"]
    return render_template('estudiant.html', materia=materia, estudiantes=lista)

if __name__ == '__main__':
    app.run(debug=True)


