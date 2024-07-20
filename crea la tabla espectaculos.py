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

# Crear la tabla "ESP_ESPECTACULOS"
db_cursor = db_connection.cursor()

db_cursor.execute("""
    CREATE TABLE ESP_ESPECTACULOS (
        ID_ESP INT AUTO_INCREMENT PRIMARY KEY,
        ID_SALA INT,
        TITULO_DEL_ESPECTACULO VARCHAR(255),
        FECHA VARCHAR(10),
        HORA VARCHAR(5),
        ENTRADA_NRO INT,
        PRECIO_UNITARIO DECIMAL(10, 2) NOT NULL,
        CONSTRAINT ID_SALA
        FOREIGN KEY (ID_SALA)
        REFERENCES SAL_SALAS (ID_SALA)
        ON DELETE CASCADE
        ON UPDATE RESTRICT
    )
""")

# Confirmar los cambios
db_connection.commit()

# Cerrar la conexión
db_connection.close()