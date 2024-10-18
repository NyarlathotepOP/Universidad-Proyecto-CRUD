import tkinter as tk
from tkinter import messagebox
from Conexiones_MySQL import obtener_correo, obtener_contrasena_usuario, obtener_credenciales, actualizar_contraseña
import smtplib
from config import EMAIL_ENV, EMAIL_PASS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def recuperar_contrasena(user_or_email):
    user_or_email = user_or_email.strip()
    if user_or_email == "":
        messagebox.showwarning("Por favor, ingrese nombre de usuario o correo")
    else:
        resultado = obtener_correo(user_or_email)
        if resultado:
            email, nombre_usuario, nombres, apellidos = resultado
            contrasena = obtener_contrasena_usuario(nombre_usuario)
            if contrasena:
                try:
                    enviar_correo(email, nombre_usuario, nombres, apellidos, contrasena)
                    messagebox.showinfo(f"Correo enviado a {email}")
                except Exception as e:
                    messagebox.showerror(f"No se pudo enviar el correo: {e}")
            else:
                print("No se pudo recuperar la contraseña del usuario")
        else:
            messagebox.showerror("Usuario o correo no encontrado o inactivo")

def enviar_correo(destinatario, nombre_usuario, nombres, apellidos, contrasena):
    remitente = EMAIL_ENV
    contraseña = EMAIL_PASS

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Usuario y Contraseña"

    body = f"Hola {nombres} {apellidos},\n\nTu usuario es: {nombre_usuario}\nTu contraseña es: {contrasena}\n\nPor favor, cambia tu contraseña después de iniciar sesión."
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, contraseña)
            smtp.sendmail(remitente, destinatario, mensaje.as_string())
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")