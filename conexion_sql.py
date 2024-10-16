import mysql.connector
from mysql.connector import Error
from contextlib import closing 
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def conectar_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        if connection.is_connected():
            print("Conectado a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    
def obtener_credenciales(nombre_usuario, contraseña):
    connection = conectar_db()
    if connection:
        with closing(connection):
            with connection.cursor() as cursor:
                try:
                    query = "SELECT contraseña FROM usuarios WHERE nombre_usuario = %s AND estado = 1"
                    cursor.execute(query, (nombre_usuario,))
                    result = cursor.fetchone()
                    
                    if result:
                        contraseña_en_db = result[0]
                        if contraseña == contraseña_en_db:
                            print("Inicio de sesión exitoso")
                            return True
                        else:
                            print("Contraseña incorrecta")
                            return False
                    else:
                        print("Usuario no encontrado o inactivo")
                        return False
                except Error as e:
                    print(f"Error al validar las credenciales: {e}")
                    return False

def obtener_correo(user_or_email):
    connection = conectar_db()
    if connection:
        with closing(connection):
            with connection.cursor() as cursor:
                try:
                    query = """
                    SELECT email, nombre_usuario FROM usuarios 
                    WHERE (LOWER(nombre_usuario) = LOWER(%s) OR LOWER(email) = LOWER(%s)) 
                    AND estado = 1
                    """
                    cursor.execute(query, (user_or_email, user_or_email))
                    result = cursor.fetchone()
                    
                    if result:
                        return result
                    else:
                        print("Usuario o correo no encontrado o inactivo")
                        return None
                except Error as e:
                    print(f"Error al obtener el correo: {e}")
                    return None

def obtener_contrasena_usuario(nombre_usuario):
    connection = conectar_db()
    if connection:
        with closing(connection):
            with connection.cursor() as cursor:
                try:
                    query = """
                    SELECT contraseña FROM usuarios 
                    WHERE LOWER(nombre_usuario) = LOWER(%s) AND estado = 1
                    """
                    cursor.execute(query, (nombre_usuario,))
                    result = cursor.fetchone()
                    
                    if result:
                        return result[0]
                    else:
                        print("Usuario no encontrado o inactivo")
                        return None
                except Error as e:
                    print(f"Error al obtener la contraseña: {e}")
                    return None
