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

# Crea un cursor
dbcursor = db_connection.cursor()

# Ejecuta la instrucción para eliminar la tabla
sql = "DROP TABLE IF EXISTS USR_USUARIOS"
dbcursor.execute(sql)

# Confirma los cambios
db_connection.commit()

print("Tabla USR_USUARIOS eliminada correctamente")