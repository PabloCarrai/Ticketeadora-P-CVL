from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import credenciales_ticketeadora as mycreds
app = Flask(__name__)

#Guido new 22/07/24
app.secret_key = 'test123'
#Guido new 22/07/24

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = mycreds.host
app.config['MYSQL_USER'] = mycreds.user
app.config['MYSQL_PASSWORD'] = mycreds.password
app.config['MYSQL_DB'] = mycreds.database
app.config['MYSQL_PORT'] = mycreds.port

mysql = MySQL(app)

#Guido new 22/07/24 (agregue home)
@app.route('/home')
def home():
    return render_template('home.html')

 #ABRE LA PAGINA INICIAL DE INICIO DE SESION/REGISTRO
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
			if account['tipo'] == "admin":
				return render_template('home.html')
			else:
				return redirect(url_for('lista_espectaculos_compra'))			
		else:
			msg = 'usuario / contraseña Incorrectos!'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register_comprador', methods =['GET', 'POST'])
def register_comprador():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form: # and 'tipo' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		tipo = "" #request.form['tipo']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM USR_USUARIOS WHERE username = % s', (username, ))
		account = cursor.fetchone()

		# Verificar si el email ya existe
		cursor.execute('SELECT * FROM USR_USUARIOS WHERE email = %s', (email,))
		email_account = cursor.fetchone()

		if account:
			msg = 'La cuenta ya existe !'
		# Valida que el mail no esté registrado
		elif email_account:
			msg = 'El email ya está registrado !'

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
	return render_template('register_comprador.html', msg = msg)
#Guido new 22/07/24

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

# editado por Sergio Giacomini 21/07/2024
	query = ("SELECT " 
		"	  SAL.ID_SALA " +
		"	, SAL.NOMBRE_DE_LA_SALA " +
		" FROM " + 
		" 	SAL_SALAS SAL "
		)
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	salas = cursor.fetchall()

	if request.method == 'POST':
		ID_ESP = request.form['ID_ESP']
		ID_SALA = request.form['ID_SALA']
		TITULO_DEL_ESPECTACULO = request.form['TITULO_DEL_ESPECTACULO']
		FECHA = request.form['FECHA']
		HORA = request.form['HORA']
		ENTRADA_NRO = request.form['ENTRADA_NRO']
		PRECIO_UNITARIO = request.form['PRECIO_UNITARIO']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		
		if ID_ESP == "":
			cursor.execute('INSERT INTO ESP_ESPECTACULOS VALUES (NULL, % s, % s, % s, % s, % s, % s)', (ID_SALA, TITULO_DEL_ESPECTACULO, FECHA, HORA, ENTRADA_NRO, PRECIO_UNITARIO))
			msg = 'Se ha registrado exitosamente !'
			mysql.connection.commit()
			return render_template('registro_espectaculos.html', salas=salas)
		else:
			cursor.execute('UPDATE ESP_ESPECTACULOS SET ID_SALA = % s, TITULO_DEL_ESPECTACULO = % s, FECHA = % s, HORA = % s, ENTRADA_NRO = % s, PRECIO_UNITARIO = % s WHERE ID_ESP = % s', (ID_SALA, TITULO_DEL_ESPECTACULO, FECHA, HORA, ENTRADA_NRO, PRECIO_UNITARIO, ID_ESP))
			msg = 'El espectaculo se ha modificado exitosamente !'
			mysql.connection.commit()
			return redirect(url_for('lista_espectaculos'))

	if request.method == 'GET':
		return render_template('registro_espectaculos.html', salas=salas)
# fin editado por Sergio Giacomini 21/07/2024

#LISTA LOS ESPECTACULOS REGISTRADOS
@app.route('/lista_espectaculos')
def lista_espectaculos():
    cur = mysql.connection.cursor()
# editado por Sergio Giacomini 21/07/2024	
    cur.execute("SELECT ESP.ID_ESP, ESP.ID_SALA, ESP.TITULO_DEL_ESPECTACULO, ESP.FECHA, ESP.HORA, ESP.ENTRADA_NRO, ESP.PRECIO_UNITARIO, SAL.NOMBRE_DE_LA_SALA, " +
				" (SELECT COALESCE(SUM(CANT),0) FROM VEN_VENTAS WHERE ID_ESP = ESP.ID_ESP) AS CANTIDAD_VENDIDA"
				" FROM ESP_ESPECTACULOS ESP INNER JOIN SAL_SALAS SAL ON SAL.ID_SALA = ESP.ID_SALA")
# Fin editado por Sergio Giacomini 21/07/2024
    espectaculos = cur.fetchall()
    cur.close()
    return render_template('lista_espectaculos.html', espectaculos=espectaculos)

# editado por Sergio Giacomini 21/07/2024
# MODIFICAR ESPECTACULO
@app.route('/modificar_espectaculo', methods =['POST'])
def modificar_espectaculo():
	ID_ESPECTACULO = request.form['ID_ESPECTACULO']

	query = ("SELECT " 
		"	  * " +
		" FROM " + 
		" 	ESP_ESPECTACULOS "
		" 	WHERE ID_ESP = " + ID_ESPECTACULO
		)

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	espectaculo = cursor.fetchall()

	query = ("SELECT " 
		"	  SAL.ID_SALA " +
		"	, SAL.NOMBRE_DE_LA_SALA " +
		" FROM " + 
		" 	SAL_SALAS SAL "
		)
	
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	salas = cursor.fetchall()

	return render_template('registro_espectaculos.html', espectaculo=espectaculo, salas=salas)

#ELIMINA ESPECTACULOS - (Consulta previa)
@app.route('/consulta_elimina_espectaculo', methods =['POST'])
def consulta_elimina_espectaculo():
	ID_ESPECTACULO = request.form['ID_ESPECTACULO']

	query = ("SELECT " +
		"	  * " +
		" FROM " + 
		" 	ESP_ESPECTACULOS "
		" 	WHERE ID_ESP = " + ID_ESPECTACULO
	)

	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute(query)
	espectaculo = cursor.fetchall()

	return render_template('consulta_elimina_espectaculo.html', espectaculo=espectaculo)

#ELIMINA ESPECTACULOS
@app.route('/elimina_espectaculo', methods =['POST'])
def elimina_espectaculo():
		ID_ESPECTACULO = request.form['ID_ESPECTACULO']

		query = ("DELETE " 
			" FROM " + 
			" 	ESP_ESPECTACULOS "
			" 	WHERE ID_ESP = " + ID_ESPECTACULO
			)

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(query)
		mysql.connection.commit()

		return redirect(url_for('lista_espectaculos'))
# Fin editado por Sergio Giacomini 21/07/2024

#GUIDO new 22/07/24
#LISTA LOS ESPECTACULOS PARA EL COMPRADOR
@app.route('/lista_espectaculos_compra')
def lista_espectaculos_compra():
	cur = mysql.connection.cursor()
# editado por Sergio Giacomini 23/07/2024
	cur.execute("SELECT ESP.ID_ESP, ESP.ID_SALA, ESP.TITULO_DEL_ESPECTACULO, ESP.FECHA, ESP.HORA, ESP.ENTRADA_NRO, ESP.PRECIO_UNITARIO, SAL.NOMBRE_DE_LA_SALA, " +
				" (SELECT COALESCE(SUM(CANT),0) FROM VEN_VENTAS WHERE ID_ESP = ESP.ID_ESP) AS CANTIDAD_VENDIDA"
				" FROM ESP_ESPECTACULOS ESP INNER JOIN SAL_SALAS SAL ON SAL.ID_SALA = ESP.ID_SALA"
				" WHERE ENTRADA_NRO > 0 AND STR_TO_DATE(FECHA, '%d/%m/%Y') > NOW()")
# editado por Sergio Giacomini 23/07/2024
	espectaculos = cur.fetchall()
	cur.close()
	return render_template('lista_espectaculos_compra.html', espectaculos=espectaculos)
#GUIDO new 22/07/24

# editado por Sergio Giacomini 23/07/2024
@app.route('/espectaculo_compra', methods =['POST'])
def espectaculo_compra():
	ID_ESPECTACULO = request.form['ID_ESPECTACULO']
	cur = mysql.connection.cursor()
	query = ("SELECT ESP.ID_ESP, ESP.ID_SALA, ESP.TITULO_DEL_ESPECTACULO, ESP.FECHA, ESP.HORA, ESP.ENTRADA_NRO, ESP.PRECIO_UNITARIO, SAL.NOMBRE_DE_LA_SALA, "
			" (SELECT COALESCE(SUM(CANT),0) FROM VEN_VENTAS WHERE ID_ESP = ESP.ID_ESP) AS CANTIDAD_VENDIDA" 
			" FROM ESP_ESPECTACULOS ESP INNER JOIN SAL_SALAS SAL ON SAL.ID_SALA = ESP.ID_SALA" 
			" WHERE ESP.ID_ESP = " + ID_ESPECTACULO)
	
	cur.execute(query)
	
	espectaculo = cur.fetchall()
	cur.close()
	return render_template('espectaculo_compra.html', espectaculo=espectaculo[0])

@app.route('/espectaculo_compra_confirmada', methods =['POST'])
def espectaculo_compra_confirmada():
	ID_ESPECTACULO = request.form['ID_ESPECTACULO']
	ENTRADA_NRO = request.form['ENTRADA_NRO']
	
	cur = mysql.connection.cursor()
	query = ("UPDATE ESP_ESPECTACULOS SET ENTRADA_NRO = ENTRADA_NRO - " + ENTRADA_NRO + " WHERE ID_ESP = " + ID_ESPECTACULO)
	cur.execute(query)

	query = 'INSERT INTO VEN_VENTAS (ID_ESP, ID_USR, CANT, FECHA) VALUES (' + ID_ESPECTACULO + ',' + str(session['id']) + ',' + ENTRADA_NRO + ', NOW())' 
	cur.execute(query)

	mysql.connection.commit()
	cur.close()

	return render_template('espectaculo_compra_confirmada.html')
# editado por Sergio Giacomini 23/07/2024

if __name__ == '__main__':
    app.run(debug=True)