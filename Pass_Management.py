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
        messagebox.showwarning("Informacion", "Por favor, ingrese nombre de usuario o correo")
    else:
        resultado = obtener_correo(user_or_email)
        if resultado:
            email, nombre_usuario, nombres, apellidos = resultado
            contrasena = obtener_contrasena_usuario(nombre_usuario)
            if contrasena:
                try:
                    enviar_correo(email, nombre_usuario, nombres, apellidos, contrasena)
                    messagebox.showinfo("Correcto", f"Correo enviado a {email}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")
            else:
                print("No se pudo recuperar la contraseña del usuario")
        else:
            messagebox.showerror("Error", f"Usuario o correo no encontrado o inactivo")

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
            print("Correcto", f"Correo enviado a {destinatario}")
    except Exception as e:
        print("Error", f"Error al enviar el correo: {e}")

def enviar_correo_progreso(destinatario, nombre_usuario, nombres, apellidos, progreso):
    remitente = EMAIL_ENV
    contraseña = EMAIL_PASS

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Progreso Periodo Actual"

    body = f"Hola {nombres} {apellidos},\n\nTu progreso es: {progreso}\n\nPor favor, comparte esta información con tus padres."
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, contraseña)
            smtp.sendmail(remitente, destinatario, mensaje.as_string())
            print("Correcto", f"Correo enviado a {destinatario}")
    except Exception as e:
        print("Error", f"Error al enviar el correo: {e}")

def enviar_info_seleccionada(tree):
    try:
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un estudiante en la tabla.")
            return

        datos = tree.item(seleccion[0], "values")
        if len(datos) < 5:
            messagebox.showerror("Error", "No se pudo obtener la información del estudiante.")
            return
        
        id_estudiante, usuario, curso, nivel, puntos = datos

        resultado = obtener_correo(usuario)
        if resultado:
            email, nombre_usuario, nombres, apellidos = resultado
        else:
            messagebox.showerror("Error", f"No se encontró un correo para el usuario {usuario}.")
            return

        enviar_correo_progreso(
            destinatario=email,
            nombre_usuario=nombre_usuario,
            nombres=nombres,
            apellidos=apellidos,
            progreso=f"\n\nCurso: {curso}\nNivel: {nivel}\nPuntos: {puntos}"
        )
        messagebox.showinfo("Éxito", f"Información enviada al correo {email}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar la información: {e}")
