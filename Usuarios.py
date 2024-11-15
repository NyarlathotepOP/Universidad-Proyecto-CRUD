import tkinter as tk
from tkinter import messagebox
import random
import string
from mysql.connector import Error
from Conexiones_MySQL import conectar_db
from Pass_Management import enviar_correo
from contextlib import closing

def limpiar_campos_usuarios(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil):
    entry_cedula.delete(0, tk.END)
    entry_nombre1.delete(0, tk.END)
    entry_nombre2.delete(0, tk.END)
    entry_apellido1.delete(0, tk.END)
    entry_apellido2.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)

def validar_campos(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario):
    if not entry_nombre1.get() or not entry_nombre2.get() or not entry_apellido2.get() or not entry_apellido1.get() or not entry_email.get() or not entry_cedula.get() or not entry_usuario.get():
        messagebox.showwarning("Error", f"Todos los campos son requeridos.")
        return False
    return True

def generar_contrasena(longitud=8):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contrasena

def crear_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree):
    if validar_campos(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario):
        cedula = entry_cedula.get()
        nombre = entry_nombre1.get()
        nombre2 = entry_nombre2.get()
        apellido = entry_apellido1.get()
        apellido2 = entry_apellido2.get()
        email = entry_email.get()
        usuario = entry_usuario.get()
        perfil_seleccionado = combobox_perfil.get()
        id_perfil = 1 if perfil_seleccionado == 'Administrador' else 2

        contrasena = generar_contrasena()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        INSERT INTO usuarios (cedula, nombres, nombres2, apellidos, apellidos2, email, nombre_usuario, contraseña, id_perfil, estado) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                        """
                        cursor.execute(query, (cedula, nombre, nombre2, apellido, apellido2, email, usuario, contrasena, id_perfil))
                        connection.commit()
                        messagebox.showinfo("Correcto", "Usuario creado con éxito.")
                        enviar_correo(email, usuario, nombre, apellido, contrasena)
                        limpiar_campos_usuarios(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario)
                        mostrar_usuarios(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo crear el cliente: {e}")

def actualizar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree):
    if validar_campos(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario):
        cedula = entry_cedula.get()
        nombre = entry_nombre1.get()
        nombre2 = entry_nombre2.get()
        apellido = entry_apellido1.get()
        apellido2 = entry_apellido2.get()
        email = entry_email.get()
        usuario = entry_usuario.get()
        perfil_seleccionado = combobox_perfil.get()
        id_perfil = 1 if perfil_seleccionado == 'Administrador' else 2

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        UPDATE usuarios 
                        SET nombres=%s, nombres2=%s, apellidos=%s, apellidos2=%s, email=%s, nombre_usuario=%s, id_perfil=%s
                        WHERE cedula=%s
                        """
                        cursor.execute(query, (nombre, nombre2, apellido, apellido2, email, usuario, id_perfil, cedula))
                        connection.commit()

                        messagebox.showinfo("Correcto", f"Usuario actualizado con éxito.")
                        limpiar_campos_usuarios(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario)
                        mostrar_usuarios(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")

def inhabilitar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree):
    cedula = entry_cedula.get()

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE usuarios 
                    SET estado=0 
                    WHERE cedula=%s
                    """
                    cursor.execute(query, (cedula,))
                    connection.commit()
                    messagebox.showinfo("Correcto", f"Usuario inhabilitado con éxito.")
                    limpiar_campos_usuarios(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil)
                    mostrar_usuarios(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo inhabilitar al usuario: {e}")

def seleccionar_usuario(tree, entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil):
    selected_item = tree.focus()
    if selected_item:
        usuario = tree.item(selected_item, 'values')
        entry_cedula.delete(0, tk.END)
        entry_cedula.insert(0, usuario[0])
        entry_nombre1.delete(0, tk.END)
        entry_nombre1.insert(0, usuario[1])
        entry_nombre2.delete(0, tk.END)
        entry_nombre2.insert(0, usuario[2])
        entry_apellido1.delete(0, tk.END)
        entry_apellido1.insert(0, usuario[3])
        entry_apellido2.delete(0, tk.END)
        entry_apellido2.insert(0, usuario[4])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, usuario[5])
        entry_usuario.delete(0, tk.END)
        entry_usuario.insert(0, usuario[6])

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        SELECT id_perfil 
                        FROM usuarios 
                        WHERE cedula = %s
                        """
                        cursor.execute(query, (usuario[0],))
                        result = cursor.fetchone()
                        if result:
                            id_perfil = result[0]
                            if id_perfil == 1:
                                combobox_perfil.set('Administrador')
                            else:
                                combobox_perfil.set('Usuario')
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo obtener el perfil del usuario: {e}")

def buscar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario):
    cedula = entry_cedula.get()
    if not cedula:
        messagebox.showwarning("Error", "Por favor, ingrese una cédula para buscar.")
        return
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT cedula, nombres, nombres2, apellidos, apellidos2, email, nombre_usuario 
                    FROM usuarios WHERE cedula=%s 
                    """
                    cursor.execute(query, (cedula,))
                    result = cursor.fetchone()
                    
                    if result:
                        entry_cedula.delete(0, tk.END)
                        entry_cedula.insert(0, result[0])
                        entry_nombre1.delete(0, tk.END)
                        entry_nombre1.insert(0, result[1])
                        entry_nombre2.delete(0, tk.END)
                        entry_nombre2.insert(0, result[2])
                        entry_apellido1.delete(0, tk.END)
                        entry_apellido1.insert(0, result[3])
                        entry_apellido2.delete(0, tk.END)
                        entry_apellido2.insert(0, result[4])
                        entry_email.delete(0, tk.END)
                        entry_email.insert(0, result[5])
                        entry_usuario.delete(0, tk.END)
                        entry_usuario.insert(0, result[6])
                    else:
                        messagebox.showinfo("Información", "No se encontró ningún usuario con esa cédula.")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

def mostrar_usuarios(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT cedula, nombres, nombres2, apellidos, apellidos2, nombre_usuario, email
                    FROM usuarios 
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
                    tree.update()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de usuarios: {e}")

def habilitar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_email, entry_usuario, tree):
    cedula = entry_cedula.get()

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE usuarios
                    SET estado=1
                    WHERE cedula=%s
                    """
                    cursor.execute(query, (cedula,))
                    connection.commit()
                    messagebox.showinfo("Información", "El usuario ha sido habilitado con éxito.")
                    limpiar_campos_usuarios(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_email, entry_usuario)
                    mostrar_usuarios(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo habilitar el usuario: {e}")