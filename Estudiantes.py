import tkinter as tk
from tkinter import messagebox
import random
import string
from mysql.connector import Error
from Conexiones_MySQL import conectar_db
from Pass_Management import enviar_correo
from contextlib import closing

def limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario):
    entry_ID.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)

def validar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario):
    if not entry_nombre.get() or not entry_apellido.get() or not entry_email.get() or not entry_ID.get() or not entry_usuario.get():
        messagebox.showwarning("Error", f"Todos los campos son requeridos.")
        return False
    return True

def generar_contrasena(longitud=8):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

def crear_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree):
    if validar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario):
        ID = entry_ID.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        email = entry_email.get()
        usuario = entry_usuario.get()

        contrasena = generar_contrasena()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        INSERT INTO estudiantes (ID, nombre, apellido, email, nombre_usuario, contraseña, estado) 
                        VALUES (%s, %s, %s, %s, %s, %s, 1)
                        """
                        cursor.execute(query, (ID, nombre, apellido, email, usuario, contrasena))
                        connection.commit()
                        messagebox.showinfo("Correcto", "Estudiante creado con éxito.")
                        enviar_correo(email, usuario, nombre, apellido, contrasena)
                        limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario)
                        mostrar_estudiante(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo crear el estudiante: {e}")

def actualizar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree):
    if validar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario):
        ID = entry_ID.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        email = entry_email.get()
        usuario = entry_usuario.get()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        UPDATE estudiantes 
                        SET nombre=%s, apellido=%s, email=%s, nombre_usuario=%s
                        WHERE ID=%s
                        """
                        cursor.execute(query, (nombre, apellido, email, usuario, ID))
                        connection.commit()

                        messagebox.showinfo("Correcto", f"Estudiante actualizado con éxito.")
                        limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario)
                        mostrar_estudiante(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el estudiante: {e}")

def inhabilitar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree):
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
                    limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario)
                    mostrar_estudiante(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo inhabilitar al estudiante: {e}")

def seleccionar_estudiante(tree, entry_ID, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
    selected_item = tree.focus()
    if selected_item:
        estudiante = tree.item(selected_item, 'values')
        entry_ID.delete(0, tk.END)
        entry_ID.insert(0, estudiante[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, estudiante[1])
        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, estudiante[2])
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, estudiante[3])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, estudiante[4])

def buscar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario):
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
                    SELECT ID, nombre, apellido, email, nombre_usuario 
                    FROM estudiantes WHERE ID=%s 
                    """
                    cursor.execute(query, (ID,))
                    result = cursor.fetchone()
                    
                    if result:
                        entry_ID.delete(0, tk.END)
                        entry_ID.insert(0, result[0])
                        entry_nombre.delete(0, tk.END)
                        entry_nombre.insert(0, result[1])
                        entry_apellido.delete(0, tk.END)
                        entry_apellido.insert(0, result[2])
                        entry_email.delete(0, tk.END)
                        entry_email.insert(0, result[3])
                        entry_usuario.delete(0, tk.END)
                        entry_usuario.insert(0, result[4])
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
                    SELECT ID, nombre, apellido, nombre_usuario, email
                    FROM estudiantes 
                    WHERE estado=1
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes: {e}")

def habilitar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree):
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
                    limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario)
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
                    SELECT ID, nombre, apellido, nombre_usuario, email
                    FROM estudiantes 
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de estudiantes: {e}")