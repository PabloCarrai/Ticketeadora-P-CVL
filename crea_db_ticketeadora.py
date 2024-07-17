import mysql.connector
import credenciales_local_host


# Crea una conexión a MySQL
db_connection = mysql.connector.connect(
    host=credenciales_local_host.host,
    user=credenciales_local_host.user,
    port=credenciales_local_host.port,
    password=credenciales_local_host.password
)

# Crea una base de datos llamada "ticketeadora"
db_cursor = db_connection.cursor()
db_cursor.execute("CREATE DATABASE ticketeadora")

# Cierra la conexión
db_cursor.close()
db_connection.close()

print("Base de datos 'ticketeadora' creada correctamente.")