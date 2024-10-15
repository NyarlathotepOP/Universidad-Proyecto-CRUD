import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import smtplib
from conexion_sql import validar_credenciales
from menu_principal import cargar_menu_principal

def login_principal():
    window = tk.Tk()
    window.title("sistemas de Gestion de Usuarios")

    window.geometry("400x500")
    window.configure(bg="lightblue")

    img = Image.open("img/inicio.png")
    img = img.resize((150, 150), Image.Resampling.LANCZOS)
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
    if validar_credenciales(nombre_usuario, contraseña):
        print("Inicio de sesión exitoso, cargando el menú principal...")
        cargar_menu_principal()
    else:
        print("Credenciales incorrectas o usuario inactivo")
        messagebox.showerror("Error", "Credenciales incorrectas o usuario inactivo")

def recuperar_contrasena(usuario):
    if usuario == "":
        messagebox.showerror("Error", "Por favor, ingresa tu nombre de usuario")
    else:
        # consulta a la base de datos para obtener el correo
        email_cliente = "cliente@ejemplo.com"  # Email de ejemplo

        # Enviar el correo
        try:
            enviar_correo(email_cliente)
            messagebox.showinfo("Éxito", f"Correo enviado a {email_cliente}")
        except:
            messagebox.showerror("Error", "No se pudo enviar el correo. Intenta más tarde.")

# smtp
def enviar_correo(destinatario):
    remitente = "tuemail@gmail.com"
    contraseña = "tucontraseña"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(remitente, contraseña)
        subject = "Recuperación de contraseña"
        body = "Esta es tu contraseña: 1234"  #consulta en la BD
        msg = f"Subject: {subject}\n\n{body}"
        smtp.sendmail(remitente, destinatario, msg)

if __name__ == "__main__":
    login_principal()
