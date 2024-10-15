import mysql.connector
from mysql.connector import Error
import hashlib
def conectar_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='Proyecto Sistema de Gestion de Usuarios',
            user='root',
            password='admin123'
        )
        if connection.is_connected():
            print("Conectado a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def validar_credenciales(nombre_usuario, contraseña):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT contraseña FROM usuarios WHERE nombre_usuario = %s AND estado = 1"
            cursor.execute(query, (nombre_usuario,))
            result = cursor.fetchone()
            
            if result:
                contraseña_en_db = result[0]

                contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()
                
                if contraseña_hash == contraseña_en_db:
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
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
