import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Pass_Management import recuperar_contrasena
from Conexiones_MySQL import obtener_credenciales, actualizar_contraseña, conectar_db
from Clientes import mostrar_clientes, crear_cliente, actualizar_cliente, inhabilitar_cliente, seleccionar_cliente, buscar_cliente, mostrar_all, habilitar_cliente, limpiar_campos
from Usuarios import buscar_usuario, inhabilitar_usuario, crear_usuario, habilitar_usuario, actualizar_usuario, mostrar_usuarios, seleccionar_usuario, limpiar_campos
from Estudiantes import buscar_estudiante, habilitar_estudiante, inhabilitar_estudiante, actualizar_estudiante, mostrar_estudiante, seleccionar_estudiante, crear_estudiante, mostrar_all_estudiante, limpiar_campos
from Game_Math import iniciar_juego

def limpiar_ventana():
    for widget in window.winfo_children():
        widget.destroy()

def login_principal():
    limpiar_ventana()
    window.title("Inicio Sesion")

    img = Image.open("img/inicio_log.png")
    img = img.resize((450, 400), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=img)
    label_img.image = img
    label_img.pack(pady=10)
    
    x_centro = 500
    y_inicial = 450
    incremento_x = 150

    label_text = tk.Label(window, text="Inicio de Sesion", font=("Calibri", 25))
    label_text.place(x=x_centro, y=y_inicial, anchor="center")

    label_user = tk.Label(window, text="Usuario", font=("Arial", 12))
    label_user.place(x=x_centro - incremento_x, y=y_inicial + 50, anchor="center")
    entry_user = tk.Entry(window, width=30)
    entry_user.place(x=x_centro, y=y_inicial + 50, anchor="center")

    label_pass = tk.Label(window, text="Contraseña", font=("Arial", 12))
    label_pass.place(x=x_centro - incremento_x, y=y_inicial + 90, anchor="center")
    entry_pass = tk.Entry(window, width=30, show="*")
    entry_pass.place(x=x_centro, y=y_inicial + 90, anchor="center")

    btn_login = ttk.Button(window, text="Ingresar", width=15, bootstyle=SUCCESS, command=lambda: iniciar_sesion(entry_user.get(), entry_pass.get()))
    btn_login.place(x=x_centro, y=y_inicial + 130, anchor="center")

    label_forgot = tk.Label(window, text="¿Olvidaste tu contraseña?", fg="blue", cursor="hand2")
    label_forgot.place(x=x_centro, y=y_inicial + 180, anchor="center")
    label_forgot.bind("<Button-1>", lambda e: ventana_recuperar_contrasena())

    btn_salir = ttk.Button(window, text="Salir", width=10, command=cerrar_aplicacion, bootstyle=DANGER)
    btn_salir.place(x=x_centro, y=y_inicial + 260, anchor="center")

def cerrar_aplicacion():
    if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
        window.destroy()

def ventana_recuperar_contrasena():
    limpiar_ventana()
    window.title("Recuperar Contraseña")

    img = Image.open("img/pass_rec.png")
    img = img.resize((500, 260), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=img)
    label_img.image = img
    label_img.pack(pady=10)

    x_centro = 500
    y_inicial = 300

    label_instruccion = tk.Label(window, text="Ingresa tu usuario o correo electrónico", font=("Calibri", 25))
    label_instruccion.place(x=x_centro, y=y_inicial, anchor="center")

    entry_user_or_email = tk.Entry(window, width=30)
    entry_user_or_email.place(x=x_centro, y=y_inicial + 60, anchor="center")

    btn_recuperar = ttk.Button(window, text="Recuperar Contraseña", width=20, command=lambda: recuperar_contrasena(entry_user_or_email.get()), bootstyle=SUCCESS)
    btn_recuperar.place(x=x_centro, y=y_inicial + 120, anchor="center")

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=login_principal, bootstyle=INFO)
    btn_atras.place(x=x_centro, y=y_inicial + 220, anchor="center")

def menu_principal_admin():
    limpiar_ventana()
    window.title("Sistema Principal Administrador")

    background_img = Image.open("img/fondo_next.png")
    background_img = background_img.resize((window.winfo_width(), window.winfo_height()), Image.Resampling.LANCZOS)
    background_img = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(window, image=background_img)
    background_label.image = background_img
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_bienvenida = tk.Label(window, text="Sistema Principal Administrador", font=("Calibri", 25))
    label_bienvenida.pack(pady=(180,50))

    btn_gestion_clientes = ttk.Button(window, text="Gestion Clientes", width=25, command=admin_gestion_clientes, bootstyle=WARNING)
    btn_gestion_clientes.pack(pady=20)

    btn_gestion_usuario = ttk.Button(window, text="Gestion Usuarios", width=25, command=admin_gestion_usuarios, bootstyle=WARNING)
    btn_gestion_usuario.pack(pady=20)

    btn_gestion_estudiante = ttk.Button(window, text="Gestion Estudiantes", width=25, command=admin_gestion_estudiantes, bootstyle=WARNING)
    btn_gestion_estudiante.pack(pady=(20,70))

    btn_salir = ttk.Button(window, text="Cerrar Sesion", width=15, command=login_principal, bootstyle=DANGER)
    btn_salir.pack(pady=15)

def menu_principal_usuario():
    limpiar_ventana()
    window.title("Menú Principal - Sistema de Gestión")

    background_img = Image.open("img/fondo_next.png")
    background_img = background_img.resize((window.winfo_width(), window.winfo_height()), Image.Resampling.LANCZOS)
    background_img = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(window, image=background_img)
    background_label.image = background_img
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_bienvenida = tk.Label(window, text="Bienvenido al Sistema de Gestión", font=("Calibri", 25))
    label_bienvenida.pack(pady=(180,50))

    btn_gestion_clientes = ttk.Button(window, text="Gestion Clientes", width=25, command=ventana_gestion_clientes, bootstyle=WARNING)
    btn_gestion_clientes.pack(pady=20)

    btn_gestion_estudiante = ttk.Button(window, text="Gestion Estudiantes", width=25, command=ventana_gestion_estudiantes, bootstyle=WARNING)
    btn_gestion_estudiante.pack(pady=20)

    btn_cambiar_contraseña = ttk.Button(window, text="Cambiar Contraseña", width=20, command=lambda: ventana_cambiar_contraseña(menu_principal_usuario), bootstyle=INFO)
    btn_cambiar_contraseña.pack(pady=(70,15))

    btn_salir = ttk.Button(window, text="Cerrar Sesion", width=15, command=login_principal, bootstyle=DANGER)
    btn_salir.pack(pady=15)

def menu_principal_estudiante(id_estudiante):
    limpiar_ventana()
    window.title("Menú Principal Estudiante")

    background_img = Image.open("img/fondo_next.png")
    background_img = background_img.resize((window.winfo_width(), window.winfo_height()), Image.Resampling.LANCZOS)
    background_img = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(window, image=background_img)
    background_label.image = background_img
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_bienvenida = tk.Label(window, text="Bienvenido Estudiante", font=("Calibri", 25))
    label_bienvenida.pack(pady=(180,50))

    def game_matematicas():
        window.withdraw()
        iniciar_juego(id_estudiante)
        window.deiconify()

    btn_matematicas = ttk.Button(window, text="Matematicas", width=25, command=game_matematicas, bootstyle=WARNING)
    btn_matematicas.pack(pady=20)

    btn_ciencias = ttk.Button(window, text="Ciencias", width=25, command="***********", bootstyle=WARNING)
    btn_ciencias.pack(pady=20)

    btn_geografia = ttk.Button(window, text="Geografia", width=25, command="***********", bootstyle=WARNING)
    btn_geografia.pack(pady=20)

    btn_cambiar_contraseña = ttk.Button(window, text="Cambiar Contraseña", width=20, command=lambda: ventana_cambiar_contraseña(lambda: menu_principal_estudiante(id_estudiante_actual)), bootstyle=INFO)
    btn_cambiar_contraseña.pack(pady=(70,15))

    btn_salir = ttk.Button(window, text="Cerrar Sesion", width=15, command=login_principal, bootstyle=DANGER)
    btn_salir.pack(pady=15)

def confirm_inhabilitar_cliente(entry_cedula, tree):
    confirm_window = tk.Toplevel(window)
    confirm_window.title("Ventana de Confirmacion")
    confirm_window.geometry("300x150")
    confirm_window.grab_set()

    label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este cliente?", font=("Calibri", 13))
    label_confirmar.pack(pady=(20, 10))

    btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_cliente(entry_cedula, tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
    btn_confirmar.pack(side="left", padx=30, pady=20)

    btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
    btn_cancelar.pack(side="right", padx=30, pady=20)

def confirm_inhabilitar_usuario(entry_cedula, tree):
    confirm_window = tk.Toplevel(window)
    confirm_window.title("Ventana de Confirmacion")
    confirm_window.geometry("300x150")
    confirm_window.grab_set()

    label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este usuario?", font=("Calibri", 13))
    label_confirmar.pack(pady=(20, 10))

    btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_usuario(entry_cedula, tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
    btn_confirmar.pack(side="left", padx=30, pady=20)

    btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
    btn_cancelar.pack(side="right", padx=30, pady=20)

def confirm_inhabilitar_estudiante(entry_ID, tree):
    confirm_window = tk.Toplevel(window)
    confirm_window.title("Ventana de Confirmacion")
    confirm_window.geometry("300x150")
    confirm_window.grab_set()

    label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este estudiante?", font=("Calibri", 13))
    label_confirmar.pack(pady=(20, 10))

    btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_estudiante(entry_ID, tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
    btn_confirmar.pack(side="left", padx=30, pady=20)

    btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
    btn_cancelar.pack(side="right", padx=30, pady=20)

def admin_gestion_clientes():
    limpiar_ventana()
    window.title("Gestion Clientes - Administrador")

    label_bienvenida = tk.Label(window, text="Gestion Clientes - Administrador", font=("Calibri", 25))
    label_bienvenida.pack(pady=(30,30))

    label_cedula = tk.Label(window, text="Cedula:")
    label_cedula.pack()
    entry_cedula = tk.Entry(window)
    entry_cedula.pack()

    label_nombre = tk.Label(window, text="Nombre:")
    label_nombre.pack()
    entry_nombre = tk.Entry(window)
    entry_nombre.pack()

    label_apellido = tk.Label(window, text="Apellido:")
    label_apellido.pack()
    entry_apellido = tk.Entry(window)
    entry_apellido.pack()

    label_direccion = tk.Label(window, text="Direccion:")
    label_direccion.pack()
    entry_direccion = tk.Entry(window)
    entry_direccion.pack()

    label_telefono = tk.Label(window, text="Telefono:")
    label_telefono.pack()
    entry_telefono = tk.Entry(window)
    entry_telefono.pack()

    btn_buscar = tk.Button(window, text="Buscar Cliente", command=lambda: buscar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono))
    btn_buscar.pack(pady=5)

    btn_crear = tk.Button(window, text="Crear Cliente", command=lambda: crear_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree))
    btn_crear.pack(pady=5)

    btn_actualizar = tk.Button(window, text="Actualizar Cliente", command=lambda: actualizar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree))
    btn_actualizar.pack(pady=5)

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Cliente", command=lambda: confirm_inhabilitar_cliente(entry_cedula, tree), state="disabled")
    btn_inhabilitar.pack(pady=5)

    btn_habilitar = tk.Button(window, text="Habilitar Cliente", command=lambda: habilitar_cliente(entry_cedula, tree))
    btn_habilitar.pack(pady=5)

    btn_limpiar = tk.Button(window, text="Limpiar", command=lambda: [limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.pack(pady=5)

    columns = ('Cedula', 'Nombre', 'Apellido','Direccion', 'Telefono')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('Cedula', text='Cedula')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Direccion', text='Direccion')
    tree.heading('Telefono', text='Telefono')
    tree.pack(pady=10)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_cliente(tree, entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono)
        else:
            btn_inhabilitar.config(state="disabled")


    tree.bind("<<TreeviewSelect>>", select)

    mostrar_all(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_admin)
    btn_atras.pack(pady=10)
    
def admin_gestion_usuarios():
    limpiar_ventana()
    window.title("Gestion Usuarios - Administrador")

    label_bienvenida = tk.Label(window, text="Gestion Usuarios - Administrador", font=("Calibri", 25))
    label_bienvenida.pack(pady=(30,30))

    label_cedula = tk.Label(window, text="Cedula:")
    label_cedula.pack()
    entry_cedula = tk.Entry(window)
    entry_cedula.pack()

    label_nombre = tk.Label(window, text="Nombre:")
    label_nombre.pack()
    entry_nombre = tk.Entry(window)
    entry_nombre.pack()

    label_apellido = tk.Label(window, text="Apellido:")
    label_apellido.pack()
    entry_apellido = tk.Entry(window)
    entry_apellido.pack()

    label_email = tk.Label(window, text="Email:")
    label_email.pack()
    entry_email = tk.Entry(window)
    entry_email.pack()

    label_usuario = tk.Label(window, text="Usuario:")
    label_usuario.pack()
    entry_usuario = tk.Entry(window)
    entry_usuario.pack()

    label_perfil = tk.Label(window, text="Perfil de Usuario:")
    label_perfil.pack()
    opciones_perfil = ['Administrador', 'Usuario']
    combobox_perfil = ttk.Combobox(window, values=opciones_perfil)
    combobox_perfil.pack()
    combobox_perfil.current(1) 

    btn_buscar = tk.Button(window, text="Buscar Usuario", command=lambda: buscar_usuario(entry_cedula, entry_nombre, entry_apellido, entry_email, entry_usuario))
    btn_buscar.pack(pady=5)

    btn_crear = tk.Button(window, text="Crear Usuario", command=lambda: crear_usuario(entry_cedula, entry_nombre, entry_apellido, entry_email, entry_usuario, combobox_perfil, tree))
    btn_crear.pack(pady=5)

    btn_actualizar = tk.Button(window, text="Actualizar Usuario", command=lambda: actualizar_usuario(entry_cedula, entry_nombre, entry_apellido, entry_email, entry_usuario, combobox_perfil, tree))
    btn_actualizar.pack(pady=5)

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Usuario", command=lambda: confirm_inhabilitar_usuario(entry_cedula, tree), state="disabled")
    btn_inhabilitar.pack(pady=5)

    btn_habilitar = tk.Button(window, text="Habilitar Usuario", command=lambda: habilitar_usuario(entry_cedula, tree))
    btn_habilitar.pack(pady=5)

    btn_limpiar = tk.Button(window, text="Limpiar", command=lambda: [limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_email, entry_usuario), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.pack(pady=5)

    columns = ('Cedula', 'Nombre', 'Apellido', 'Email', 'Usuario')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('Cedula', text='Cedula')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Email', text='Email')
    tree.heading('Usuario', text='Usuario')
    tree.pack(pady=10)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_usuario(tree, entry_cedula, entry_nombre, entry_apellido, entry_email, entry_usuario, combobox_perfil)
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_usuarios(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_admin)
    btn_atras.pack(pady=10)

def admin_gestion_estudiantes():
    limpiar_ventana()
    window.title("Gestion Estudiantes - Administrador")

    label_bienvenida = tk.Label(window, text="Gestion Estudiantes - Administrador", font=("Calibri", 25))
    label_bienvenida.pack(pady=(30,30))

    label_ID = tk.Label(window, text="ID:")
    label_ID.pack()
    entry_ID = tk.Entry(window)
    entry_ID.pack()

    label_nombre = tk.Label(window, text="Nombre:")
    label_nombre.pack()
    entry_nombre = tk.Entry(window)
    entry_nombre.pack()

    label_apellido = tk.Label(window, text="Apellido:")
    label_apellido.pack()
    entry_apellido = tk.Entry(window)
    entry_apellido.pack()

    label_email = tk.Label(window, text="Email:")
    label_email.pack()
    entry_email = tk.Entry(window)
    entry_email.pack()

    label_usuario = tk.Label(window, text="Usuario:")
    label_usuario.pack()
    entry_usuario = tk.Entry(window)
    entry_usuario.pack()

    btn_buscar = tk.Button(window, text="Buscar Usuario", command=lambda: buscar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario))
    btn_buscar.pack(pady=5)

    btn_crear = tk.Button(window, text="Crear Usuario", command=lambda: crear_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree))
    btn_crear.pack(pady=5)

    btn_actualizar = tk.Button(window, text="Actualizar Usuario", command=lambda: actualizar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree))
    btn_actualizar.pack(pady=5)

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Usuario", command=lambda: confirm_inhabilitar_estudiante(entry_ID, tree), state="disabled")
    btn_inhabilitar.pack(pady=5)

    btn_habilitar = tk.Button(window, text="Habilitar Usuario", command=lambda: habilitar_estudiante(entry_ID, tree))
    btn_habilitar.pack(pady=5)

    btn_limpiar = tk.Button(window, text="Limpiar", command=lambda: [limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.pack(pady=5)

    columns = ('ID', 'Nombre', 'Apellido', 'Email', 'Usuario')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Email', text='Email')
    tree.heading('Usuario', text='Usuario')
    tree.pack(pady=10)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_estudiante(tree, entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario)
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_all_estudiante(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_admin)
    btn_atras.pack(pady=10)

def ventana_gestion_clientes():
    limpiar_ventana()
    window.title("Gestion Clientes")

    label_bienvenida = tk.Label(window, text="Gestion Clientes", font=("Calibri", 25))
    label_bienvenida.pack(pady=(30,30))

    label_cedula = tk.Label(window, text="Cedula:")
    label_cedula.pack()
    entry_cedula = tk.Entry(window)
    entry_cedula.pack()

    label_nombre = tk.Label(window, text="Nombre:")
    label_nombre.pack()
    entry_nombre = tk.Entry(window)
    entry_nombre.pack()

    label_apellido = tk.Label(window, text="Apellido:")
    label_apellido.pack()
    entry_apellido = tk.Entry(window)
    entry_apellido.pack()

    label_direccion = tk.Label(window, text="Direccion:")
    label_direccion.pack()
    entry_direccion = tk.Entry(window)
    entry_direccion.pack()

    label_telefono = tk.Label(window, text="Telefono:")
    label_telefono.pack()
    entry_telefono = tk.Entry(window)
    entry_telefono.pack()

    btn_buscar = tk.Button(window, text="Buscar Cliente", command=lambda: buscar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono))
    btn_buscar.pack(pady=5)

    btn_crear = tk.Button(window, text="Crear Cliente", command=lambda: crear_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree))
    btn_crear.pack(pady=5)

    btn_actualizar = tk.Button(window, text="Actualizar Cliente", command=lambda: actualizar_cliente(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono, tree))
    btn_actualizar.pack(pady=5)

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Cliente", command=lambda: confirm_inhabilitar_cliente(entry_cedula, tree), state="disabled")
    btn_inhabilitar.pack(pady=5)

    btn_limpiar = tk.Button(window, text="Limpiar", command=lambda: [limpiar_campos(entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.pack(pady=5)

    columns = ('Cedula', 'Nombre', 'Apellido','Direccion', 'Telefono')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('Cedula', text='Cedula')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Direccion', text='Direccion')
    tree.heading('Telefono', text='Telefono')
    tree.pack(pady=10)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_cliente(tree, entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono)
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_clientes(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_usuario)
    btn_atras.pack(pady=10)

def ventana_gestion_estudiantes():
    limpiar_ventana()
    window.title("Gestion Estudiantes")

    label_bienvenida = tk.Label(window, text="Gestion Estudiantes", font=("Calibri", 25))
    label_bienvenida.pack(pady=(30,30))

    label_ID = tk.Label(window, text="ID:")
    label_ID.pack()
    entry_ID = tk.Entry(window)
    entry_ID.pack()

    label_nombre = tk.Label(window, text="Nombre:")
    label_nombre.pack()
    entry_nombre = tk.Entry(window)
    entry_nombre.pack()

    label_apellido = tk.Label(window, text="Apellido:")
    label_apellido.pack()
    entry_apellido = tk.Entry(window)
    entry_apellido.pack()

    label_email = tk.Label(window, text="Email:")
    label_email.pack()
    entry_email = tk.Entry(window)
    entry_email.pack()

    label_usuario = tk.Label(window, text="Usuario:")
    label_usuario.pack()
    entry_usuario = tk.Entry(window)
    entry_usuario.pack()

    btn_buscar = tk.Button(window, text="Buscar Usuario", command=lambda: buscar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario))
    btn_buscar.pack(pady=5)

    btn_crear = tk.Button(window, text="Crear Usuario", command=lambda: crear_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree))
    btn_crear.pack(pady=5)

    btn_actualizar = tk.Button(window, text="Actualizar Usuario", command=lambda: actualizar_estudiante(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario, tree))
    btn_actualizar.pack(pady=5)

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Usuario", command=lambda: confirm_inhabilitar_estudiante(entry_ID, tree), state="disabled")
    btn_inhabilitar.pack(pady=5)

    btn_limpiar = tk.Button(window, text="Limpiar", command=lambda: [limpiar_campos(entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.pack(pady=5)

    columns = ('ID', 'Nombre', 'Apellido', 'Email', 'Usuario')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Email', text='Email')
    tree.heading('Usuario', text='Usuario')
    tree.pack(pady=10)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_estudiante(tree, entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario)
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_estudiante(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_usuario)
    btn_atras.pack(pady=10)

def ventana_cambiar_contraseña(ventana_anterior):
    limpiar_ventana()
    window.title("Cambiar Contraseña")

    background_img = Image.open("img/fondo_next.png")
    background_img = background_img.resize((window.winfo_width(), window.winfo_height()), Image.Resampling.LANCZOS)
    background_img = ImageTk.PhotoImage(background_img)

    background_label = tk.Label(window, image=background_img)
    background_label.image = background_img
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    x_centro = 500
    y_inicial = 220

    label_instruccion = tk.Label(window, text="Ingresa tu contraseña actual y la nueva contraseña", font=("Arial", 18))
    label_instruccion.place(x=x_centro, y=y_inicial, anchor="center")

    label_actual = tk.Label(window, text="Contraseña actual", font=("Arial", 12))
    label_actual.place(x=x_centro, y=y_inicial + 60, anchor="center")
    entry_actual = tk.Entry(window, width=35, show="*")
    entry_actual.place(x=x_centro, y=y_inicial + 90, anchor="center")

    label_nueva = tk.Label(window, text="Nueva contraseña", font=("Arial", 12))
    label_nueva.place(x=x_centro, y=y_inicial + 135, anchor="center")
    entry_nueva = tk.Entry(window, width=35, show="*")
    entry_nueva.place(x=x_centro, y=y_inicial + 175, anchor="center")

    label_confirmar = tk.Label(window, text="Confirmar nueva contraseña", font=("Arial", 12))
    label_confirmar.place(x=x_centro, y=y_inicial + 220, anchor="center")
    entry_confirmar = tk.Entry(window, width=35, show="*")
    entry_confirmar.place(x=x_centro, y=y_inicial + 250, anchor="center")

    btn_actualizar = ttk.Button(window, text="Actualizar Contraseña", width=25, command=lambda: cambiar_contraseña(entry_actual.get(), entry_nueva.get(), entry_confirmar.get()), bootstyle=SUCCESS)
    btn_actualizar.place(x=x_centro, y=y_inicial + 300, anchor="center")

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=ventana_anterior, bootstyle=DANGER)
    btn_atras.place(x=x_centro, y=y_inicial + 400, anchor="center")

def cambiar_contraseña(contraseña_actual, nueva_contraseña, confirmar_contraseña):
    nombre_usuario = usuario_actual  

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
            messagebox.showinfo("Contraseña actualizada correctamente.")
            if id_estudiante_actual:
                menu_principal_estudiante(id_estudiante_actual)
            else:
                menu_principal_usuario()
        else:
            messagebox.showerror("Hubo un problema al actualizar la contraseña.")
    else:
        messagebox.showerror("La contraseña actual es incorrecta.")

usuario_actual = None
id_estudiante_actual = None
def iniciar_sesion(nombre_usuario, contraseña):
    global usuario_actual, id_estudiante_actual

    if not nombre_usuario or not contraseña:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un usuario y contraseña válidos")
        return

    credenciales = obtener_credenciales(nombre_usuario, contraseña)

    if credenciales:
        id_perfil, estado = credenciales

        if estado == 1:
            usuario_actual = nombre_usuario

            if id_perfil == 1:
                menu_principal_admin()
            elif id_perfil == 2:
                menu_principal_usuario()
            elif id_perfil == 4:
                conexion = conectar_db()
                if conexion:
                    cursor = conexion.cursor()
                    query = "SELECT ID FROM estudiantes WHERE nombre_usuario = %s"
                    cursor.execute(query, (nombre_usuario,))
                    resultado = cursor.fetchone()
                    cursor.close()
                    conexion.close()
                    
                    if resultado:
                        id_estudiante_actual = resultado[0]
                        menu_principal_estudiante(id_estudiante_actual)
                    else:
                        print("Error: Estudiante no encontrado.")
        else:
            print("Usuario inactivo")
            messagebox.showerror("Error", "El usuario está inhabilitado")
    else:
        print("Credenciales incorrectas")
        messagebox.showerror("Error", "Credenciales incorrectas")


def obtener_usuario_actual():
    return usuario_actual, id_estudiante_actual

if __name__ == "__main__":
    window = ttk.Window(themename="superhero")
    window.geometry("1000x800")
    window.configure(bg="#2C3E50")

    login_principal()
    window.mainloop()