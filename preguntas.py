import tkinter as tk
from tkinter import messagebox
import random
import string
from mysql.connector import Error
from Conexiones_MySQL import conectar_db
from contextlib import closing

def limpiar_campos_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta):
    entry_pregunta.delete(0, tk.END)
    entry_opcion1.delete(0, tk.END)
    entry_opcion2.delete(0, tk.END)
    entry_opcion3.delete(0, tk.END)
    entry_opcion4.delete(0, tk.END)
    entry_correcta.delete(0, tk.END)

def validar_campos(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta):
    if not entry_pregunta.get() or not entry_opcion1.get() or not entry_opcion2.get() or not entry_opcion3.get() or not entry_opcion4.get() or not entry_correcta.get():
        messagebox.showwarning("Error", f"Todos los campos son requeridos.")
        return False
    return True

def mostrar_preguntas(tree):
    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT preguntas, opcion_1, opcion_2, opcion_3, opcion_4, respuesta_correcta 
                    FROM preguntas 
                    """
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    for row in tree.get_children():
                        tree.delete(row)

                    for row in rows:
                        tree.insert("", tk.END, values=row)
                    tree.update()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo obtener la lista de clientes: {e}")

def seleccionar_preguntas(tree, entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta):
    selected_item = tree.focus()
    if selected_item:
        cliente = tree.item(selected_item, 'values')
        entry_pregunta.delete(0, tk.END)
        entry_pregunta.insert(tk.END, cliente[0])
        entry_opcion1.delete(0, tk.END)
        entry_opcion1.insert(tk.END, cliente[1])
        entry_opcion2.delete(0, tk.END)
        entry_opcion2.insert(tk.END, cliente[2])
        entry_opcion3.delete(0, tk.END)
        entry_opcion3.insert(tk.END, cliente[3])
        entry_opcion4.delete(0, tk.END)
        entry_opcion4.insert(tk.END, cliente[4])
        entry_correcta.delete(0, tk.END)
        entry_correcta.insert(tk.END, cliente[5])

def buscar_pregunta(tree, entry_pregunta):
        for item in tree.get_children():
            tree.delete(item)
        
        preguntas_filtradas = []
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            consulta = """SELECT preguntas, opcion_1, opcion_2, opcion_3, opcion_4, respuesta_correcta 
                          FROM preguntas 
                          WHERE preguntas LIKE %s"""
            cursor.execute(consulta, (f"%{entry_pregunta.get()}%",))
            preguntas_filtradas = cursor.fetchall()
            conexion.close()
        except Exception as e:
            print(f"Error al buscar preguntas: {e}")

        for pregunta in preguntas_filtradas:
            tree.insert("", "end", values=pregunta)
        tree.update()

def crear_pregunta(usuario_actual, entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta, tree):
    if validar_campos(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta):
        pregunta = entry_pregunta.get()
        opcion1 = entry_opcion1.get()
        opcion2 = entry_opcion2.get()
        opcion3 = entry_opcion3.get()
        opcion4 = entry_opcion4.get()
        respuesta_correcta = entry_correcta.get()

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                            INSERT INTO preguntas 
                            (preguntas, opcion_1, opcion_2, opcion_3, opcion_4, respuesta_correcta, nombre_usuario) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (pregunta, opcion1, opcion2, opcion3, opcion4, respuesta_correcta, usuario_actual))
                        connection.commit()
                        messagebox.showinfo("Correcto", "Pregunta creada con éxito.")
                        limpiar_campos_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta)
                        mostrar_preguntas(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo crear la pregunta: {e}")

def actualizar_pregunta(usuario_actual, entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta, tree):
    if validar_campos(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta):
        pregunta = entry_pregunta.get()
        opcion1 = entry_opcion1.get()
        opcion2 = entry_opcion2.get()
        opcion3 = entry_opcion3.get()
        opcion4 = entry_opcion4.get()
        respuesta_correcta = entry_correcta.get()
        
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una pregunta para actualizar.")
            return
        
        pregunta_anterior = tree.item(selected_item, "values")[0]

        connection = conectar_db()
        if connection:
            with closing(connection):
                try:
                    with connection.cursor() as cursor:
                        query = """
                        UPDATE preguntas 
                        SET preguntas=%s, opcion_1=%s, opcion_2=%s, opcion_3=%s, opcion_4=%s, respuesta_correcta=%s, nombre_usuario=%s
                        WHERE preguntas=%s
                        """
                        cursor.execute(query, (pregunta, opcion1, opcion2, opcion3, opcion4, respuesta_correcta, usuario_actual, pregunta_anterior))
                        connection.commit()

                        messagebox.showinfo("Correcto", f"Pregunta actualizada con éxito.")
                        limpiar_campos_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta)
                        mostrar_preguntas(tree)
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo actualizar la pregunta: {e}")

def borrar_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta):
    pregunta = entry_pregunta.get()
    if not pregunta:
        messagebox.showwarning("Advertencia", "Debe seleccionar una pregunta para borrar.")
        return

    connection = conectar_db()
    if connection:
        with closing(connection):
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_preguntas_5to FROM preguntas WHERE preguntas = %s", (pregunta,))
                    result = cursor.fetchone()
                    if not result:
                        messagebox.showerror("Error", "La pregunta no existe en la base de datos.")
                        return

                    id_pregunta = result[0]

                    query = "DELETE FROM preguntas WHERE id_preguntas_5to = %s"
                    cursor.execute(query, (id_pregunta,))
                    connection.commit()

                    messagebox.showinfo("Éxito", "La pregunta se ha eliminado correctamente.")
                    limpiar_campos_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta)
            except Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar la pregunta: {e}")
