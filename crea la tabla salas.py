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

# Crear la tabla "SAL_SALAS"
db_cursor = db_connection.cursor()

db_cursor.execute("""
    CREATE TABLE SAL_SALAS (
        ID_SALA INT AUTO_INCREMENT PRIMARY KEY,
        NOMBRE_DE_LA_SALA VARCHAR(255),
        CALLE VARCHAR(255),
        NRO INT,
        LOCALIDAD VARCHAR(255),
        CAPACIDAD INT
    )
""")

# Confirmar los cambios
db_connection.commit()

# Cerrar la conexión
db_connection.close()