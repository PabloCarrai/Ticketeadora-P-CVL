import mysql.connector
import credenciales_ticketeadora
# Conectarse a la base de datos
db_connection = mysql.connector.connect(
    host=credenciales_ticketeadora.host,
    user=credenciales_ticketeadora.user,
    password=credenciales_ticketeadora.password,
    port=credenciales_ticketeadora.port,
    database=credenciales_ticketeadora.database
)

# Crear la tabla "USR_USUARIOS"
db_cursor = db_connection.cursor()

db_cursor.execute("""
    CREATE TABLE USR_USUARIOS (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(60),
        password VARCHAR(60),
        email VARCHAR(60),
        tipo VARCHAR(10)
    )
""")

# Confirmar los cambios
db_connection.commit()

# Cerrar la conexión
db_connection.close()