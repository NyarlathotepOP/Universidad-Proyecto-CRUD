import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from recu_contraseña import recuperar_contrasena
from conexion_sql import obtener_credenciales, actualizar_contraseña

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
    
    btn_cambiar_contraseña = tk.Button(window, text="Cambiar Contraseña", width=15, command=ventana_cambiar_contraseña)
    btn_cambiar_contraseña.pack(pady=10)

def ventana_cambiar_contraseña():
    limpiar_ventana()
    window.title("Cambiar Contraseña")

    label_instruccion = tk.Label(window, text="Ingresa tu contraseña actual y la nueva contraseña", bg="lightblue", font=("Arial", 12))
    label_instruccion.pack(pady=5)

    label_actual = tk.Label(window, text="Contraseña actual", bg="lightblue", font=("Arial", 12))
    label_actual.pack(pady=5)
    entry_actual = tk.Entry(window, width=30, show="*")
    entry_actual.pack()

    label_nueva = tk.Label(window, text="Nueva contraseña", bg="lightblue", font=("Arial", 12))
    label_nueva.pack(pady=5)
    entry_nueva = tk.Entry(window, width=30, show="*")
    entry_nueva.pack()

    label_confirmar = tk.Label(window, text="Confirmar nueva contraseña", bg="lightblue", font=("Arial", 12))
    label_confirmar.pack(pady=5)
    entry_confirmar = tk.Entry(window, width=30, show="*")
    entry_confirmar.pack()

    btn_actualizar = tk.Button(window, text="Actualizar Contraseña", width=15, command=lambda: cambiar_contraseña(entry_actual.get(), entry_nueva.get(), entry_confirmar.get()))
    btn_actualizar.pack(pady=20)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=cargar_menu_principal)
    btn_atras.pack(pady=10)

def cambiar_contraseña(contraseña_actual, nueva_contraseña, confirmar_contraseña):
    nombre_usuario = obtener_usuario_actual()

    if not contraseña_actual or not nueva_contraseña or not confirmar_contraseña:
        messagebox.showwarning("Por favor, completa todos los campos.")
        return

    if nueva_contraseña != confirmar_contraseña:
        messagebox.showerror("La nueva contraseña y la confirmación no coinciden.")
        return

    if len(nueva_contraseña) < 6:
        messagebox.showerror("La contraseña debe tener al menos 6 caracteres.")
        return

    if obtener_credenciales(nombre_usuario, contraseña_actual):
        if actualizar_contraseña(nombre_usuario, nueva_contraseña):
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            cargar_menu_principal()
        else:
            messagebox.showerror("Error", "Hubo un problema al actualizar la contraseña.")
    else:
        messagebox.showerror("Error", "La contraseña actual es incorrecta.")

usuario_actual = None
def iniciar_sesion(nombre_usuario, contraseña):
    global usuario_actual

    if not nombre_usuario or not contraseña:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un usuario y contraseña válidos")
        return

    if obtener_credenciales(nombre_usuario, contraseña):
        usuario_actual = nombre_usuario
        print("Inicio de sesión exitoso, cargando el menú principal...")
        cargar_menu_principal()
    else:
        print("Credenciales incorrectas o usuario inactivo")
        messagebox.showerror("Credenciales incorrectas o usuario inactivo")

def obtener_usuario_actual():
    return usuario_actual

if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("500x500")
    window.configure(bg="lightblue")
    
    login_principal()
    window.mainloop()