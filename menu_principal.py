import tkinter as tk
from tkinter import messagebox

def cargar_menu_principal():
    global window
    window = tk.Tk()
    window.title("Menú Principal - Sistema de Gestión")

    window.geometry("600x400")
    window.configure(bg="lightblue")

    menu_bar = tk.Menu(window)

    window.config(menu=menu_bar)

    label_bienvenida = tk.Label(window, text="Bienvenido al Sistema de Gestión", font=("Arial", 16), bg="lightblue")
    label_bienvenida.pack(pady=50)

    window.mainloop()