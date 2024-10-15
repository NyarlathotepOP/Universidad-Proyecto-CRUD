import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conexion_sql import obtener_credenciales, obtener_correo, obtener_contrasena_usuario
from menu_principal import cargar_menu_principal
from config import EMAIL_ENV, EMAIL_PASS

def login_principal():
    window = tk.Tk()
    window.title("Inicio Sesion")

    window.geometry("500x500")
    window.configure(bg="lightblue")

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
    label_forgot.bind("<Button-1>", lambda e: recuperar_contrasena(entry_user.get()))

    window.mainloop()

def iniciar_sesion(nombre_usuario, contraseña):
    if obtener_credenciales(nombre_usuario, contraseña):
        print("Inicio de sesión exitoso, cargando el menú principal...")
        cargar_menu_principal()
    else:
        print("Credenciales incorrectas o usuario inactivo")
        messagebox.showerror("Error", "Credenciales incorrectas o usuario inactivo")

def recuperar_contrasena(usuario):
    if usuario == "":
        print("Por favor, ingresa tu nombre de usuario")
    else:
        email = obtener_correo(usuario)
        if email:
            contrasena = obtener_contrasena_usuario(usuario)
            if contrasena:
                try:
                    enviar_correo(email, contrasena)
                    print(f"Correo enviado a {email}")
                except Exception as e:
                    print(f"No se pudo enviar el correo. Intenta más tarde: {e}")
            else:
                print("No se pudo recuperar la contraseña del usuario")
        else:
            print("Usuario no encontrado o no tiene un correo asociado")

def enviar_correo(destinatario, contrasena):
    remitente = EMAIL_ENV
    contraseña = EMAIL_PASS

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Recuperación de contraseña"

    body = f"Tu contraseña es: {contrasena}"
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, contraseña)
            smtp.sendmail(remitente, destinatario, mensaje.as_string())
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

if __name__ == "__main__":
    login_principal()