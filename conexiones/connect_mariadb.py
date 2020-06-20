import pymysql

try:
        mydb = pymysql.connect(
                host="localhost",
                database="biometrico",
                user="administrador",
                password="manex"
        )

except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:

        print("Ocurrió un error al conectar: ", e)