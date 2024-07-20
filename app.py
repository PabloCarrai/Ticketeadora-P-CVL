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

#ABRE LA PAGINA INICIAL DE ADMINISTRACION
@app.route('/')
def home():
    return render_template('home.html')

# REGISTRO DE USUARIOS QUE PERMITE INCORPORAR ADMINISTRADORES
@app.route('/')
@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'tipo' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		tipo = request.form['tipo']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM USR_USUARIOS WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'La cuenta ya existe !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'email Invalido !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'El Usuario debe iniciar con caracteres o numeros !'
		elif not username or not password or not email:
			msg = 'Por favor complete el formulario !'
		else:
			cursor.execute('INSERT INTO USR_USUARIOS VALUES (NULL, % s, % s, % s, % s)', (username, password, email, tipo ))
			mysql.connection.commit()
			msg = 'Se ha registrado exitosamente !'
	elif request.method == 'POST':
		msg = 'Por favor complete el formulario !'
	return render_template('register.html', msg = msg)

# LISTA LOS USUARIOS REGISTRADOS
@app.route('/')
@app.route('/lista_usuarios')
def lista_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password, email, tipo FROM USR_USUARIOS")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('lista_usuarios.html', usuarios=usuarios)

#ALTA DE SALAS
@app.route('/')
@app.route('/registro_salas', methods =['GET', 'POST'])
def registro_salas():
	msg = ''
	if request.method == 'POST':
		NOMBRE_DE_LA_SALA = request.form['NOMBRE_DE_LA_SALA']
		CALLE = request.form['CALLE']
		NRO = request.form['NRO']
		LOCALIDAD = request.form['LOCALIDAD']
		CAPACIDAD = request.form['CAPACIDAD']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO SAL_SALAS VALUES (NULL, % s, % s, % s, % s, % s)', (NOMBRE_DE_LA_SALA, CALLE, NRO, LOCALIDAD, CAPACIDAD))
		mysql.connection.commit()
		msg = 'Se ha registrado exitosamente !'
	return render_template('registro_salas.html')

#LISTA LAS SALAS REGISTRADAS
@app.route('/')
@app.route('/lista_salas')
def lista_salas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_SALA, NOMBRE_DE_LA_SALA,CALLE, NRO, LOCALIDAD, CAPACIDAD FROM SAL_SALAS")
    salas = cur.fetchall()
    cur.close()
    return render_template('lista_salas.html', salas=salas)

#ALTA DE ESPECTACULOS
@app.route('/')
@app.route('/registro_espectaculos', methods =['GET', 'POST'])
def registro_espectaculos():
	msg = ''
	if request.method == 'POST':
		ID_SALA = request.form['ID_SALA']
		TITULO_DEL_ESPECTACULO = request.form['TITULO_DEL_ESPECTACULO']
		FECHA = request.form['FECHA']
		HORA = request.form['HORA']
		ENTRADA_NRO = request.form['ENTRADA_NRO']
		PRECIO_UNITARIO = request.form['PRECIO_UNITARIO']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO ESP_ESPECTACULOS VALUES (NULL, % s, % s, % s, % s, % s, % s)', (ID_SALA, TITULO_DEL_ESPECTACULO, FECHA, HORA, ENTRADA_NRO, PRECIO_UNITARIO))
		mysql.connection.commit()
		msg = 'Se ha registrado exitosamente !'
	return render_template('registro_espectaculos.html')

#LISTA LOS ESPECTACULOS REGISTRADOS
@app.route('/')
@app.route('/lista_espectaculos')
def lista_espectaculos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_ESP, ID_SALA,TITULO_DEL_ESPECTACULO, FECHA, HORA, ENTRADA_NRO,PRECIO_UNITARIO FROM ESP_ESPECTACULOS")
    espectaculos = cur.fetchall()
    cur.close()
    return render_template('lista_espectaculos.html', espectaculos=espectaculos)

if __name__ == '__main__':
    app.run(debug=True)
    
