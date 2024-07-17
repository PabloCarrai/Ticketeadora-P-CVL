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
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
