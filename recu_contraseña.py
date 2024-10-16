import tkinter as tk
from tkinter import messagebox
from conexion_sql import obtener_correo, obtener_contrasena_usuario
import smtplib
from config import EMAIL_ENV, EMAIL_PASS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def recuperar_contrasena(usuario_o_correo):
    if usuario_o_correo == "":
        messagebox.showwarning("Advertencia", "Por favor, ingresa tu nombre de usuario o correo electrónico")
    else:
        email = obtener_correo(usuario_o_correo)
        if email:
            contrasena = obtener_contrasena_usuario(usuario_o_correo)
            if contrasena:
                try:
                    enviar_correo(email, usuario_o_correo, contrasena)
                    messagebox.showinfo("Éxito", f"Correo enviado a {email}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")
            else:
                messagebox.showerror("Error", "No se pudo recuperar la contraseña del usuario")
        else:
            messagebox.showerror("Error", "Usuario o correo no encontrado")

def enviar_correo(destinatario, nombre_usuario, contrasena):
    remitente = EMAIL_ENV
    contraseña = EMAIL_PASS

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Recuperación de contraseña"

    body = f"Hola {nombre_usuario},\n\nTu nombre de usuario es: {nombre_usuario}\nTu contraseña es: {contrasena}\n\nPor favor, cambia tu contraseña después de iniciar sesión."
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, contraseña)
            smtp.sendmail(remitente, destinatario, mensaje.as_string())
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")