import mysql.connector
import credenciales_ticketeadora

mydb = mysql.connector.connect(
  host=credenciales_ticketeadora.host,
  user=credenciales_ticketeadora.user,
  password=credenciales_ticketeadora.password,
  port=credenciales_ticketeadora.port,
  database=credenciales_ticketeadora.database
  )


mycursor = mydb.cursor()
sql = "SELECT * FROM USR_USUARIOS" # Reemplazar por: USR_USUARIOS, ESP_ESPECTACULOS, VEN_VENTAS, o SAL_SALAS

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
  print(x)