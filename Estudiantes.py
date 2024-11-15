import tkinter as tk
from tkinter import messagebox
import random
import string
from mysql.connector import Error
from Conexiones_MySQL import conectar_db
from Pass_Management import enviar_correo
from contextlib import closing

def limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario):
    entry_ID.delete(0, tk.END)
    entry_nombre1.delete(0, tk.END)
    entry_nombre2.delete(0, tk.END)
    entry_apellido1.delete(0, tk.END)
    entry_apellido2.delete(0, tk.END)
    entry_curso.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)

def validar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario):
    if not entry_nombre1.get() or not entry_nombre2.get() or not entry_apellido1.get() or not entry_apellido2.get() or not entry_email.get() or not entry_ID.get() or not entry_usuario.get() or not entry_curso.get():
        messagebox.showwarning("Error", f"Todos los campos son requeridos.")
        return False
    return True

def generar_contrasena(longitud=8):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

def crear_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree):
    if validar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario):
        ID = entry_ID.get()
        nombre = entry_nombre1.get()
        nombre2 = entry_nombre2.get()
        apellido = entry_apellido1.get()
        apellido2 = entry_apellido2.get()
        curso = entry_curso.get()
        email = entry_email.get()
        usuario = entry_usuario.get()

        contrasena = generar_contrasena()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        INSERT INTO estudiantes (ID, nombre, nombre2, apellido, apellido2, curso, email, nombre_usuario, contraseña, estado) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                        """
                        cursor.execute(query, (ID, nombre, nombre2, apellido, apellido2, curso, email, usuario, contrasena))
                        connection.commit()
                        messagebox.showinfo("Correcto", "Estudiante creado con éxito.")
                        enviar_correo(email, usuario, nombre, apellido, contrasena)
                        limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario)
                        mostrar_estudiante(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo crear el estudiante: {e}")

def actualizar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree):
    if validar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario):
        ID = entry_ID.get()
        nombre = entry_nombre1.get()
        nombre2 = entry_nombre2.get()
        apellido = entry_apellido1.get()
        apellido2 = entry_apellido2.get()
        curso = entry_curso.get()
        email = entry_email.get()
        usuario = entry_usuario.get()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        UPDATE estudiantes 
                        SET nombre=%s, nombre2=%s, apellido=%s, apellido2=%s, curso=%s, email=%s, nombre_usuario=%s
                        WHERE ID=%s
                        """
                        cursor.execute(query, (nombre, nombre2, apellido, apellido2, curso, email, usuario, ID))
                        connection.commit()

                        messagebox.showinfo("Correcto", f"Estudiante actualizado con éxito.")
                        limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario)
                        mostrar_estudiante(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el estudiante: {e}")

def inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree):
    ID = entry_ID.get()

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE estudiantes 
                    SET estado=0 
                    WHERE ID=%s
                    """
                    cursor.execute(query, (ID,))
                    connection.commit()
                    messagebox.showinfo("Correcto", f"Estudiante inhabilitado con éxito.")
                    limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario)
                    mostrar_estudiante(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo inhabilitar al estudiante: {e}")

def seleccionar_estudiante(tree, entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2,  entry_curso, entry_usuario, entry_email):
    selected_item = tree.focus()
    if selected_item:
        estudiante = tree.item(selected_item, 'values')
        entry_ID.delete(0, tk.END)
        entry_ID.insert(0, estudiante[0])
        entry_nombre1.delete(0, tk.END)
        entry_nombre1.insert(0, estudiante[1])
        entry_nombre2.delete(0, tk.END)
        entry_nombre2.insert(0, estudiante[2])
        entry_apellido1.delete(0, tk.END)
        entry_apellido1.insert(0, estudiante[3])
        entry_apellido2.delete(0, tk.END)
        entry_apellido2.insert(0, estudiante[4])
        entry_curso.delete(0, tk.END)
        entry_curso.insert(0, estudiante[5])
        entry_usuario.delete(0, tk.END)
        entry_usuario.insert(0, estudiante[6])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, estudiante[7])

def buscar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario):
    ID = entry_ID.get()
    if not ID:
        messagebox.showwarning("Error", "Por favor, ingrese un ID para buscar.")
        return
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT ID, nombre, nombre2, apellido, apellido2, curso, email, nombre_usuario 
                    FROM estudiantes WHERE ID=%s 
                    """
                    cursor.execute(query, (ID,))
                    result = cursor.fetchone()
                    
                    if result:
                        entry_ID.delete(0, tk.END)
                        entry_ID.insert(0, result[0])
                        entry_nombre1.delete(0, tk.END)
                        entry_nombre1.insert(0, result[1])
                        entry_nombre2.delete(0, tk.END)
                        entry_nombre2.insert(0, result[2])
                        entry_apellido1.delete(0, tk.END)
                        entry_apellido1.insert(0, result[3])
                        entry_apellido2.delete(0, tk.END)
                        entry_apellido2.insert(0, result[4])
                        entry_curso.delete(0, tk.END)
                        entry_curso.insert(0, result[5])
                        entry_email.delete(0, tk.END)
                        entry_email.insert(0, result[6])
                        entry_usuario.delete(0, tk.END)
                        entry_usuario.insert(0, result[7])
                    else:
                        messagebox.showinfo("Información", "No se encontró ningún estudiante con ese ID.")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

def mostrar_estudiante(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT ID, nombre, nombre2, apellido, apellido2, curso, nombre_usuario, email
                    FROM estudiantes 
                    WHERE estado=1
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
                    tree.update()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes: {e}")

def habilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree):
    ID = entry_ID.get()

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE estudiantes
                    SET estado=1
                    WHERE ID=%s
                    """
                    cursor.execute(query, (ID,))
                    connection.commit()
                    messagebox.showinfo("Información", "El estudiante ha sido habilitado con éxito.")
                    limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario)
                    mostrar_estudiante(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo habilitar el estudiante: {e}")

def mostrar_all_estudiante(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT ID, nombre, nombre2, apellido, apellido2, curso, nombre_usuario, email
                    FROM estudiantes 
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
                    tree.update()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes: {e}")

def mostrar_progreso_all(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT estudiantes.ID, estudiantes.nombre_usuario, estudiantes.curso, progreso.nivel, progreso.puntos
                    FROM estudiantes
                    LEFT JOIN progreso ON estudiantes.id_estudiantes = progreso.id_estudiantes
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
                    tree.update()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes con progreso: {e}")

def seleccionar_progreso(tree, entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos):
    selected_item = tree.focus()
    if selected_item:
        progreso = tree.item(selected_item, 'values')
        entry_ID.delete(0, tk.END)
        entry_ID.insert(0, progreso[0])
        entry_usuario.delete(0, tk.END)
        entry_usuario.insert(0, progreso[1])
        entry_curso.delete(0, tk.END)
        entry_curso.insert(0, progreso[2])
        entry_nivel.delete(0, tk.END)
        entry_nivel.insert(0, progreso[3])
        entry_puntos.delete(0, tk.END)
        entry_puntos.insert(0, progreso[4])

def buscar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos):
    ID = entry_ID.get()
    if not ID:
        messagebox.showwarning("Error", "Por favor, ingrese un ID para buscar.")
        return
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT estudiantes.ID, estudiantes.nombre_usuario, estudiantes.curso, progreso.nivel, progreso.puntos
                    FROM estudiantes
                    LEFT JOIN progreso ON estudiantes.id_estudiantes = progreso.id_estudiantes
                    WHERE estudiantes.ID = %s
                    """
                    cursor.execute(query, (ID,))
                    result = cursor.fetchone()
                    
                    if result:
                        entry_ID.delete(0, tk.END)
                        entry_ID.insert(0, result[0])
                        entry_usuario.delete(0, tk.END)
                        entry_usuario.insert(0, result[1])
                        entry_curso.delete(0, tk.END)
                        entry_curso.insert(0, result[2])
                        entry_nivel.delete(0, tk.END)
                        entry_nivel.insert(0, result[3])
                        entry_puntos.delete(0, tk.END)
                        entry_puntos.insert(0, result[4])
                    else:
                        messagebox.showinfo("Información", "No se encontró ningún estudiante con ese ID.")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

def validar_campos_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos):
    if not entry_nivel.get() or not entry_puntos.get() or not entry_usuario.get() or not entry_ID.get() or not entry_curso.get():
        messagebox.showwarning("Error", f"Todos los campos son requeridos.")
        return False
    return True

def actualizar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos, tree):
    if validar_campos_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos):
        ID = entry_ID.get()
        nivel = entry_nivel.get()
        puntos = entry_puntos.get()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        UPDATE progreso 
                        SET nivel = %s, puntos = %s
                        WHERE id_estudiantes = (
                            SELECT id_estudiantes 
                            FROM estudiantes 
                            WHERE ID = %s
                        );
                        """
                        cursor.execute(query, (nivel, puntos, ID))
                        connection.commit()

                        messagebox.showinfo("Correcto", "Progreso actualizado con éxito.")
                        limpiar_progreso(entry_ID, entry_usuario, entry_nivel, entry_puntos, entry_curso)
                        mostrar_progreso_all(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el progreso: {e}")

def limpiar_progreso(entry_ID, entry_usuario, entry_nivel, entry_puntos, entry_curso):
    entry_ID.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)
    entry_nivel.delete(0, tk.END)
    entry_puntos.delete(0, tk.END)
    entry_curso.delete(0, tk.END)

def borrar_progreso():
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE progreso
                    SET nivel = 0, puntos = 0
                    """
                    cursor.execute(query)
                    connection.commit()

                    messagebox.showinfo("Correcto", "Los valores de 'nivel' y 'puntos' han sido establecidos a 0.")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo borrar el progreso: {e}")