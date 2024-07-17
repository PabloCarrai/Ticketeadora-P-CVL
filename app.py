# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import credenciales_ticketeadora as mycreds

app = Flask(__name__)

app.secret_key = 'test123'

app.config['MYSQL_HOST'] = mycreds.host
app.config['MYSQL_USER'] = mycreds.user
app.config['MYSQL_PASSWORD'] = mycreds.password
app.config['MYSQL_DB'] = mycreds.database
app.config['MYSQL_PORT'] = mycreds.port
#logint = mycreds.login

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM USR_USUARIOS WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			#msg = 'Acceso Exitoso !'
			#return render_template('index.html', msg = msg)
			#return render_template('registro_salas.html', msg = msg)
			return render_template('index.html')

		else:
			msg = 'usuario / contraseña Incorrectos!'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

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
	
	return render_template('index.html', msg = msg)

@app.route('/consulta_usuarios', methods = ['GET', 'POST'])
def consulta_usuarios():
	query = 'SELECT usuario, password, mail FROM USR_USUARIOS'
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	usuarios = cursor.fetchall()
	return render_template('consulta_usuarios.html', usuarios=usuarios)

@app.route('/alta_salas')
def alta_salas():
    return render_template('alta_salas.html')

@app.route('/baja_salas')
def baja_salas():
    return render_template('baja_salas.html')

@app.route('/baja_salas')
def modificacion_salas():
    return render_template('modificacion_salas.html')

@app.route('/baja_salas')
def consulta_salas():
    return render_template('consulta_salas.html')


if __name__ == '__main__':  
    app.run(debug = True)