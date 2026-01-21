from flask import Flask, render_template, request, redirect, url_for, request   
from flask_mysqldb import MySQL #importar la librería para mysql
import MySQLdb.cursors #importar los cursores

app = Flask(__name__)

@app.route('/')
def saludo():
    return "Hola, bienvenido a mi API con Flask"

#configuracion de las variables para la bd mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ventas'
conexion = MySQL(app) #crear la conexión a la bd

@app.route('/clientes')
def listar_clientes():
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor) #crear el cursor
    sql = "SELECT * FROM clientes" #consulta sql
    cursor.execute(sql) #ejecutar la consulta
    datos = cursor.fetchall() #obtener los resultados
     #datos es una lista
     #datos wa un dicccionario con el uso de MySQLdb.cursors.DictCursor
    print(datos)
    return render_template('clientes.html', clientes=datos) #enviar los datos a la plantilla

@app.route("/clientes/nuevo",methods=['GET','POST'])
def nuevo_cliente():
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
def elimina_cliente(id_cliente):
    cursor = conexion.connection.cursor()
    sql = "DELETE FROM clientes WHERE id_cliente = %s"
    cursor.execute(sql,(id_cliente,))
    conexion.connection.commit()
    cursor.close()
    return redirect(url_for('listar_clientes'))

if __name__ == '__main__':
    app.run(debug=True)