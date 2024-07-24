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

if __name__ == '__main__':
    app.run(debug=True)

