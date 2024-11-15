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
                    user_or_email = user_or_email.strip()

                    query_usuarios = """
                    SELECT email, nombre_usuario, nombres, apellidos FROM usuarios 
                    WHERE (LOWER(nombre_usuario) = LOWER(%s) OR LOWER(email) = LOWER(%s)) 
                    AND estado = 1
                    """
                    cursor.execute(query_usuarios, (user_or_email, user_or_email))
                    result = cursor.fetchone()

                    if result:
                        return result
                    else:
                        query_estudiantes = """
                        SELECT email, nombre_usuario, nombre, apellido FROM estudiantes 
                        WHERE (LOWER(nombre_usuario) = LOWER(%s) OR LOWER(email) = LOWER(%s)) 
                        AND estado = 1
                        """
                        cursor.execute(query_estudiantes, (user_or_email, user_or_email))
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
                    query_usuarios = """
                    SELECT contraseña FROM usuarios 
                    WHERE LOWER(nombre_usuario) = LOWER(%s) AND estado = 1
                    """
                    cursor.execute(query_usuarios, (nombre_usuario,))
                    result = cursor.fetchone()
                    
                    if result:
                        return result[0]
                    else:
                        query_estudiantes = """
                        SELECT contraseña FROM estudiantes 
                        WHERE LOWER(nombre_usuario) = LOWER(%s) AND estado = 1
                        """
                        cursor.execute(query_estudiantes, (nombre_usuario,))
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
                    query_usuarios = """
                    UPDATE usuarios SET contraseña = %s 
                    WHERE nombre_usuario = %s 
                    AND estado = 1
                    """
                    cursor.execute(query_usuarios, (nueva_contraseña, nombre_usuario))
                    
                    if cursor.rowcount == 0:
                        query_estudiantes = """
                        UPDATE estudiantes SET contraseña = %s 
                        WHERE nombre_usuario = %s 
                        AND estado = 1
                        """
                        cursor.execute(query_estudiantes, (nueva_contraseña, nombre_usuario))
                    
                    if cursor.rowcount > 0:
                        connection.commit()
                        return True
                    else:
                        print("Usuario no encontrado o inactivo.")
                        return False
                except Error as e:
                    print(f"Error al actualizar la contraseña: {e}")
                    return False
                
def obtener_ranking():
    connection = conectar_db()
    if connection:
        cursor = connection.cursor()
        consulta = """
        SELECT estudiantes.nombre_usuario, progreso.puntos, progreso.nivel
        FROM estudiantes
        JOIN progreso ON progreso.id_estudiantes = estudiantes.id_estudiantes
        ORDER BY progreso.puntos DESC, progreso.nivel DESC;
        """
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        cursor.close()
        connection.close()
        return resultados
    else:
        return []