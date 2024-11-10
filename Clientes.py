import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from Conexiones_MySQL import conectar_db
from contextlib import closing

def limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
    entry_cedula.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)

def validar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
    if not entry_nombre.get() or not entry_apellido.get() or not entry_telefono.get() or not entry_cedula.get() or not entry_direccion.get():
        messagebox.showwarning("Error", f"Todos los campos son requeridos.")
        return False
    return True

def crear_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree):
    if validar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
        cedula = entry_cedula.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = "INSERT INTO clientes (cedula, nombre, apellido, direccion, telefono, estado) VALUES (%s, %s, %s, %s, %s, 1)"
                        cursor.execute(query, (cedula, nombre, apellido, direccion, telefono))
                        connection.commit()
                        messagebox.showinfo("Correcto", f"Cliente creado con éxito.")
                        limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono)
                        mostrar_clientes(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo crear el cliente: {e}")

def actualizar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree):
    if validar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
        cedula = entry_cedula.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        UPDATE clientes 
                        SET nombre=%s, apellido=%s, direccion=%s, telefono=%s 
                        WHERE cedula=%s
                        """
                        cursor.execute(query, (nombre, apellido, direccion, telefono, cedula))
                        connection.commit()

                        messagebox.showinfo("Correcto", f"Cliente actualizado con éxito.")
                        limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono)
                        mostrar_clientes(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")

def inhabilitar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree):
    cedula = entry_cedula.get()

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE clientes 
                    SET estado=0 
                    WHERE cedula=%s
                    """
                    cursor.execute(query, (cedula,))
                    connection.commit()
                    messagebox.showinfo("Correcto", f"Cliente inhabilitado con éxito.")
                    limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono)
                    mostrar_clientes(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo inhabilitar el cliente: {e}")

def mostrar_clientes(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT cedula, nombre, apellido, telefono, direccion 
                    FROM clientes 
                    WHERE estado=1
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de clientes: {e}")

def seleccionar_cliente(tree, entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
    selected_item = tree.focus()
    if selected_item:
        cliente = tree.item(selected_item, 'values')
        entry_cedula.delete(0, tk.END)
        entry_cedula.insert(0, cliente[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, cliente[1])
        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, cliente[2])
        entry_direccion.delete(0, tk.END)
        entry_direccion.insert(0, cliente[3])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, cliente[4])

def buscar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono):
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
                    SELECT cedula, nombre, apellido, direccion, telefono 
                    FROM clientes WHERE cedula=%s 
                    AND estado=1
                    """
                    cursor.execute(query, (cedula,))
                    result = cursor.fetchone()
                    
                    if result:
                        entry_cedula.delete(0, tk.END)
                        entry_cedula.insert(0, result[0])
                        entry_nombre.delete(0, tk.END)
                        entry_nombre.insert(0, result[1])
                        entry_apellido.delete(0, tk.END)
                        entry_apellido.insert(0, result[2])
                        entry_direccion.delete(0, tk.END)
                        entry_direccion.insert(0, result[3])
                        entry_telefono.delete(0, tk.END)
                        entry_telefono.insert(0, result[4])
                    else:
                        messagebox.showinfo("Información", "No se encontró ningún cliente con esa cédula.")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

def mostrar_all(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT cedula, nombre, apellido, telefono, direccion
                    FROM clientes 
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de clientes: {e}")

def habilitar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree):
    cedula = entry_cedula.get()

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    UPDATE clientes
                    SET estado=1
                    WHERE cedula=%s
                    """
                    cursor.execute(query, (cedula,))
                    connection.commit()
                    messagebox.showinfo("Información", "El usuario ha sido habilitado con éxito.")
                    limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono)
                    mostrar_all(tree)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo habilitar el usuario: {e}")