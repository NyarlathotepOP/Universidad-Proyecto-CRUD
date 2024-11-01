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
                    query = """
                    SELECT id_perfil, estado FROM usuarios 
                    WHERE nombre_usuario = %s 
                    AND contraseña = %s
                    """
                    cursor.execute(query, (nombre_usuario, contraseña))
                    result = cursor.fetchone()
                    
                    if not result:
                        query_estudiantes = """
                        SELECT 4 AS id_perfil, estado FROM estudiantes 
                        WHERE nombre_usuario = %s 
                        AND contraseña = %s
                        """
                        cursor.execute(query_estudiantes, (nombre_usuario, contraseña))
                        result = cursor.fetchone()

                    if result:
                        id_perfil, estado = result
                        print("Inicio de sesión exitoso")
                        return (id_perfil, estado)
                    else:
                        print("Usuario no encontrado o inactivo")
                        return None
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
                    SELECT email, nombre_usuario, nombres, apellidos FROM usuarios 
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

def actualizar_contraseña(nombre_usuario, nueva_contraseña):
    connection = conectar_db()
    if connection:
        with closing(connection):
            with connection.cursor() as cursor:
                try:
                    query = """
                    UPDATE usuarios SET contraseña = %s 
                    WHERE nombre_usuario = %s 
                    AND estado = 1
                    """
                    cursor.execute(query, (nueva_contraseña, nombre_usuario))
                    connection.commit()
                    return True
                except Error as e:
                    print(f"Error al actualizar la contraseña: {e}")
                    return False
