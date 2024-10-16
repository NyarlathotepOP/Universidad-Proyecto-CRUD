import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from recu_contraseña import recuperar_contrasena
from conexion_sql import obtener_credenciales

def limpiar_ventana():
    for widget in window.winfo_children():
        widget.destroy()

def login_principal():
    limpiar_ventana()
    window.title("Inicio Sesion")

    img = Image.open("img/inicio.png")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=img, bg="lightblue")
    label_img.image = img
    label_img.pack(pady=10)

    label_user = tk.Label(window, text="Usuario", bg="lightblue", font=("Arial", 12))
    label_user.pack(pady=5)
    entry_user = tk.Entry(window, width=30)
    entry_user.pack()

    label_pass = tk.Label(window, text="Contraseña", bg="lightblue", font=("Arial", 12))
    label_pass.pack(pady=5)
    entry_pass = tk.Entry(window, width=30, show="*")
    entry_pass.pack()

    btn_login = tk.Button(window, text="Ingresar", width=15, command=lambda: iniciar_sesion(entry_user.get(), entry_pass.get()))
    btn_login.pack(pady=20)

    label_forgot = tk.Label(window, text="¿Olvidaste tu contraseña?", bg="lightblue", fg="blue", cursor="hand2")
    label_forgot.pack()
    label_forgot.bind("<Button-1>", lambda e: ventana_recuperar_contrasena())

    btn_salir = tk.Button(window, text="Salir", width=10, command=cerrar_aplicacion)
    btn_salir.pack(pady=10)

def cerrar_aplicacion():
    if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
        window.destroy()

def ventana_recuperar_contrasena():
    limpiar_ventana()
    window.title("Recuperar Contraseña")

    label_instruccion = tk.Label(window, text="Ingresa tu usuario o correo electrónico", bg="lightblue", font=("Arial", 12))
    label_instruccion.pack(pady=5)

    entry_user_or_email = tk.Entry(window, width=30)
    entry_user_or_email.pack()

    btn_recuperar = tk.Button(window, text="Recuperar Contraseña", width=15, command=lambda: recuperar_contrasena(entry_user_or_email.get()))
    btn_recuperar.pack(pady=20)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=login_principal)
    btn_atras.pack(pady=10)

def cargar_menu_principal():
    limpiar_ventana()
    window.title("Menú Principal - Sistema de Gestión")

    label_bienvenida = tk.Label(window, text="Bienvenido al Sistema de Gestión", font=("Arial", 16), bg="lightblue")
    label_bienvenida.pack(pady=50)

    btn_salir = tk.Button(window, text="Cerrar Sesion", width=10, command=login_principal)
    btn_salir.pack(pady=10)

def iniciar_sesion(nombre_usuario, contraseña):

    if not nombre_usuario or not contraseña:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un usuario y contraseña válidos")
        return

    if obtener_credenciales(nombre_usuario, contraseña):
        print("Inicio de sesión exitoso, cargando el menú principal...")
        cargar_menu_principal()
    else:
        print("Credenciales incorrectas o usuario inactivo")
        messagebox.showerror("Error", "Credenciales incorrectas o usuario inactivo")

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("500x500")
    window.configure(bg="lightblue")
    
    login_principal()
    window.mainloop()