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

# Crear la tabla "VEN_VENTAS"
db_cursor = db_connection.cursor()

db_cursor.execute("""
    CREATE TABLE VEN_VENTAS (
        ID_VTA INT AUTO_INCREMENT PRIMARY KEY,
        ID_ESP INT,
        ID_USR INT,
        CANT INT,
        CONSTRAINT ID_ESP
        FOREIGN KEY (ID_ESP)
        REFERENCES ESP_ESPECTACULOS (ID_ESP)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
    )
""")

# Confirmar los cambios
db_connection.commit()

# Cerrar la conexión
db_connection.close()
print("Tabla creada correctamente")