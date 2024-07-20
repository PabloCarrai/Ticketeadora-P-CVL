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
def listar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, email, tipo FROM USR_USUARIOS")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('lista_usuarios.html', usuarios=usuarios)


if __name__ == '__main__':
    app.run(debug=True)
