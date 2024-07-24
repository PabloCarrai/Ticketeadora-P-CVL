from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import credenciales_ticketeadora as mycreds
app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = mycreds.host
app.config['MYSQL_USER'] = mycreds.user
app.config['MYSQL_PASSWORD'] = mycreds.password
app.config['MYSQL_DB'] = mycreds.database
app.config['MYSQL_PORT'] = mycreds.port

mysql = MySQL(app)

@app.route('/')
@app.route('/lista_salas', methods =['GET', 'POST'])
def lista_salas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_SALA, NOMBRE_DE_LA_SALA,CALLE, NRO, LOCALIDAD, CAPACIDAD FROM SAL_SALAS")
    salas = cur.fetchall()
    cur.close()
    return render_template('lista_salas.html', salas=salas)

if __name__ == '__main__':
    app.run(debug=True)