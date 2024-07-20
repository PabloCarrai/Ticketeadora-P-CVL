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
def listar_espectaculos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_ESP, ID_SALA,TITULO_DEL_ESPECTACULO, FECHA, HORA, ENTRADA_NRO,PRECIO_UNITARIO FROM ESP_ESPECTACULOS")
    espectaculos = cur.fetchall()
    cur.close()
    return render_template('lista_espectaculos.html', espectaculos=espectaculos)

if __name__ == '__main__':
    app.run(debug=True)