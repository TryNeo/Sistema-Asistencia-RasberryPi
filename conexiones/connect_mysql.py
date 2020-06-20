import mysql.connector as mysql
try:
        mydb = mysql.connect(
                host="localhost",
                port=3306,
                database="biometrico",
                user="root",
                password="root"
        )

except (mysql.err.OperationalError, mysql.err.InternalError) as e:

        print("Ocurrió un error al conectar: ", e)
