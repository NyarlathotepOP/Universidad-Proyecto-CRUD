import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Pass_Management import recuperar_contrasena, enviar_info_seleccionada
from Conexiones_MySQL import obtener_credenciales, actualizar_contraseña, conectar_db, obtener_ranking
from Clientes import mostrar_clientes, crear_cliente, actualizar_cliente, inhabilitar_cliente, seleccionar_cliente, buscar_cliente, mostrar_all, habilitar_cliente, limpiar_campos_clientes
from Usuarios import buscar_usuario, inhabilitar_usuario, crear_usuario, habilitar_usuario, actualizar_usuario, mostrar_usuarios, seleccionar_usuario, limpiar_campos_usuarios
from Estudiantes import buscar_estudiante, habilitar_estudiante, inhabilitar_estudiante, actualizar_estudiante, mostrar_estudiante, seleccionar_estudiante, crear_estudiante, mostrar_all_estudiante, limpiar_campos, mostrar_progreso_all, seleccionar_progreso, buscar_progreso, limpiar_progreso, actualizar_progreso, borrar_progreso
from Preguntas import limpiar_campos_pregunta, mostrar_preguntas, seleccionar_preguntas, buscar_pregunta, crear_pregunta, actualizar_pregunta, borrar_pregunta
from Game import iniciar_juego

def limpiar_ventana():
    for widget in window.winfo_children():
        widget.destroy()

def login_principal():
    limpiar_ventana()
    window.title("Inicio Sesión")

    img = Image.open("img/inicio_log.png")
    img = img.resize((450, 400), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=img)
    label_img.image = img
    label_img.pack(pady=10)
    
    x_centro = 500
    y_inicial = 450
    incremento_x = 150

    label_text = tk.Label(window, text="Inicio de Sesión", font=("Calibri", 25))
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

    btn_gestion_clientes = ttk.Button(window, text="Progreso Estudiantes", width=25, command=admin_progreso_estudiantes, bootstyle=WARNING)
    btn_gestion_clientes.pack(pady=20)

    btn_gestion_clientes = ttk.Button(window, text="Gestion Padres", width=25, command=admin_gestion_clientes, bootstyle=WARNING)
    btn_gestion_clientes.pack(pady=20)

    btn_gestion_usuario = ttk.Button(window, text="Gestion Profesores", width=25, command=admin_gestion_usuarios, bootstyle=WARNING)
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

    btn_gestion_clientes = ttk.Button(window, text="Progreso Estudiantes", width=25, command=ventana_progreso_estudiantes, bootstyle=WARNING)
    btn_gestion_clientes.pack(pady=20)

    btn_gestion_clientes = ttk.Button(window, text="Preguntas GAME", width=25, command=ventana_preguntas_game, bootstyle=WARNING)
    btn_gestion_clientes.pack(pady=20)

    btn_gestion_clientes = ttk.Button(window, text="Gestion Padres", width=25, command=ventana_gestion_clientes, bootstyle=WARNING)
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
    label_bienvenida.pack(pady=(180,80))

    def game_matematicas():
        window.withdraw()
        iniciar_juego(id_estudiante)
        window.deiconify()

    btn_matematicas = ttk.Button(window, text="GAME", width=25, command=game_matematicas, bootstyle=WARNING)
    btn_matematicas.pack(pady=20)

    btn_ranking = ttk.Button(window, text="Ranking", width=25, command=lambda: ranking(id_estudiante), bootstyle=WARNING)
    btn_ranking.pack(pady=20)

    btn_cambiar_contraseña = ttk.Button(window, text="Cambiar Contraseña", width=20, command=lambda: ventana_cambiar_contraseña(lambda: menu_principal_estudiante(id_estudiante_actual)), bootstyle=INFO)
    btn_cambiar_contraseña.pack(pady=(70,15))

    btn_salir = ttk.Button(window, text="Cerrar Sesion", width=15, command=login_principal, bootstyle=DANGER)
    btn_salir.pack(pady=15)

def ventana_preguntas_game():
    limpiar_ventana()
    window.title("Preguntas Game")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_preguntas(tree)
            tree.update()

    def confirm_borrar_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta, tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("350x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de borrar esta pregunta?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [borrar_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta), refrescar_treeview(tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Preguntas Game", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_pregunta = tk.Label(window, text="Pregunta:", font="helvetica, 12")
    label_pregunta.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_pregunta = tk.Entry(window, width=60, font=("helvetica", 10))
    entry_pregunta.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_opcion1 = tk.Label(window, text="Opcion 1:", font="helvetica, 12")
    label_opcion1.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_opcion1 = tk.Entry(window, width=60, font=("helvetica", 10))
    entry_opcion1.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_opcion2 = tk.Label(window, text="Opcion 2:", font="helvetica, 12")
    label_opcion2.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_opcion2 = tk.Entry(window, width=60, font=("helvetica", 10))
    entry_opcion2.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_opcion3 = tk.Label(window, text="Opcion 3:", font="helvetica, 12")
    label_opcion3.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_opcion3 = tk.Entry(window, width=60, font=("helvetica", 10))
    entry_opcion3.grid(row=4, column=1, padx=(3, 10), pady=5)

    label_opcion4 = tk.Label(window, text="Opcion 4:", font="helvetica, 12")
    label_opcion4.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_opcion4 = tk.Entry(window, width=60, font=("helvetica", 10))
    entry_opcion4.grid(row=5, column=1, padx=(3, 10), pady=10)

    label_correcta = tk.Label(window, text="Respuesta Correcta:", font="helvetica, 12")
    label_correcta.grid(row=6, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_correcta = tk.Entry(window, width=60, font=("helvetica", 10))
    entry_correcta.grid(row=6, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Pregunta", command=lambda: buscar_pregunta(tree, entry_pregunta))
    btn_buscar.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    btn_crear = ttk.Button(window, width=20, bootstyle=LIGHT, text="Crear Pregunta", command=lambda: [crear_pregunta(usuario_actual, entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta, tree), refrescar_treeview(tree)])
    btn_crear.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Pregunta", command=lambda: [actualizar_pregunta(usuario_actual, entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    btn_eliminar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Eliminar Pregunta", command=lambda: [confirm_borrar_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta, tree), refrescar_treeview(tree)], state="disabled")
    btn_eliminar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda: [limpiar_campos_pregunta(entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta), tree.selection_remove(tree.selection()), refrescar_treeview(tree), btn_eliminar.config(state="disabled")])
    btn_limpiar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    columns = ('Pregunta', 'Opcion 1', 'Opcion 2', 'Opcion 3', 'Opcion 4', 'Correcta')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('Pregunta', text='Pregunta')
    tree.heading('Opcion 1', text='Opcion 1')
    tree.heading('Opcion 2', text='Opcion 2')
    tree.heading('Opcion 3', text='Opcion 3')
    tree.heading('Opcion 4', text='Opcion 4')
    tree.heading('Correcta', text='Correcta')
    tree.grid(row=7, column=0, columnspan=3, padx=10, pady=(50, 10), sticky="nsew")

    tree.column('Pregunta', width=100, anchor='w', stretch=True)
    tree.column('Opcion 1', width=100, anchor='w', stretch=True)
    tree.column('Opcion 2', width=100, anchor='w', stretch=True)
    tree.column('Opcion 3', width=100, anchor='w', stretch=True)
    tree.column('Opcion 4', width=100, anchor='w', stretch=True)
    tree.column('Correcta', width=100, anchor='w', stretch=True)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_eliminar.config(state="normal")
            seleccionar_preguntas(tree, entry_pregunta, entry_opcion1, entry_opcion2, entry_opcion3, entry_opcion4, entry_correcta)            
            tree.update()
        else:
            btn_eliminar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_preguntas(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_usuario, bootstyle=DANGER) 
    btn_atras.grid(row=8, column=0, columnspan=3, pady=15, sticky="n")

def ranking(id_estudiante):
    limpiar_ventana()
    window.title("Ranking")

    background_img = Image.open("img/fondo_next.png")
    background_img = background_img.resize((window.winfo_width(), window.winfo_height()), Image.Resampling.LANCZOS)
    background_img = ImageTk.PhotoImage(background_img)
    
    background_label = tk.Label(window, image=background_img)
    background_label.image = background_img
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    label_bienvenida = tk.Label(window, text="Ranking Game", font=("Calibri", 25))
    label_bienvenida.pack(pady=(180,10))

    tree = ttk.Treeview(window, columns=("Posición", "Nombre", "Puntos", "Nivel"), show="headings", style="Treeview")
    tree.heading("Posición", text="Posición")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Puntos", text="Puntos")
    tree.heading("Nivel", text="Nivel")

    tree.column("Posición", width=80, anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.column("Puntos", width=100, anchor="center")
    tree.column("Nivel", width=80, anchor="center")
    tree.pack(pady=20)

    ranking_data = obtener_ranking()
    for posicion, (nombre, puntos, nivel) in enumerate(ranking_data, start=1):
        tree.insert("", "end", values=(posicion, nombre, puntos, nivel))

    btn_salir = ttk.Button(window, text="Atrás", width=15, command=lambda: menu_principal_estudiante(id_estudiante), bootstyle=DANGER)
    btn_salir.pack(pady=15)

def admin_progreso_estudiantes():
    limpiar_ventana()
    window.title("Progreso Estudiantes - Administrador")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_progreso_all(tree)
            tree.update()

    def confirm_borrar_progreso(tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("500x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de borrar el progreso de todos los estudiantes?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [borrar_progreso(), refrescar_treeview(tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Progreso Estudiantes - Administrador", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_ID = tk.Label(window, text="ID:", font="helvetica, 12")
    label_ID.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_ID = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_ID.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_usuario = tk.Label(window, text="Usuario:", font="helvetica, 12")
    label_usuario.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_usuario = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_usuario.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_curso = tk.Label(window, text="Curso:", font="helvetica, 12")
    label_curso.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_curso = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_curso.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_nivel = tk.Label(window, text="Nivel:", font="helvetica, 12")
    label_nivel.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nivel = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_nivel.grid(row=4, column=1, padx=(3, 10), pady=5)

    label_puntos = tk.Label(window, text="Puntos:", font="helvetica, 12")
    label_puntos.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_puntos = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_puntos.grid(row=5, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Estudiante", command=lambda: buscar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos))
    btn_buscar.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Progreso", command=lambda: [actualizar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda:limpiar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos))
    btn_limpiar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_enviar = ttk.Button(window, width=20, text="Enviar al Correo", command=lambda: enviar_info_seleccionada(tree), bootstyle=LIGHT)
    btn_enviar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_borrar = ttk.Button(window, text="Borrar todo el progreso", width=30, command=lambda: [confirm_borrar_progreso(tree), refrescar_treeview(tree)], bootstyle=WARNING) 
    btn_borrar.grid(row=6, column=0, columnspan=3, pady=(30, 30), sticky="n")

    columns = ('ID', 'Usuario', 'Curso', 'Nivel', 'Puntos')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('ID', text='ID')
    tree.heading('Usuario', text='Usuario')
    tree.heading('Curso', text='Curso')
    tree.heading('Nivel', text='Nivel')
    tree.heading('Puntos', text='Puntos')
    tree.grid(row=7, column=0, columnspan=3, padx=10, pady=(30, 10), sticky="nsew")

    tree.column('ID', width=50, anchor='center', stretch=True)
    tree.column('Usuario', width=120, anchor='center', stretch=True)
    tree.column('Curso', width=120, anchor='center', stretch=True)
    tree.column('Nivel', width=120, anchor='center', stretch=True)
    tree.column('Puntos', width=100, anchor='center', stretch=True)

    tree.bind("<<TreeviewSelect>>", lambda event:    seleccionar_progreso(tree, entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos))
    tree.update()

    mostrar_progreso_all(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_admin, bootstyle=DANGER) 
    btn_atras.grid(row=8, column=0, columnspan=3, pady=15, sticky="n")

def admin_gestion_clientes():
    limpiar_ventana()
    window.title("Gestion Padres - Administrador")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_all(tree)
            tree.update()

    def confirm_inhabilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este cliente?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Gestion Padres - Administrador", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_cedula = tk.Label(window, text="Cedula:", font="helvetica, 12")
    label_cedula.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_cedula = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_cedula.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_nombre1 = tk.Label(window, text="Primer Nombre:", font="helvetica, 12")
    label_nombre1.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre1.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_nombre2 = tk.Label(window, text="Segundo Nombre:", font="helvetica, 12")
    label_nombre2.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre2.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_apellido1 = tk.Label(window, text="Primer Apellido:", font="helvetica, 12")
    label_apellido1.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido1.grid(row=4, column=1, padx=(3, 10), pady=10)

    label_apellido2 = tk.Label(window, text="Segundo Apellido:", font="helvetica, 12")
    label_apellido2.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido2.grid(row=5, column=1, padx=(3, 10), pady=10)

    label_telefono = tk.Label(window, text="Teléfono:", font="helvetica, 12")
    label_telefono.grid(row=6, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_telefono = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_telefono.grid(row=6, column=1, padx=(3, 10), pady=5)

    label_direccion = tk.Label(window, text="Dirección:", font="helvetica, 12")
    label_direccion.grid(row=7, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_direccion = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_direccion.grid(row=7, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Cliente", command=lambda: buscar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono))
    btn_buscar.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    btn_crear = ttk.Button(window, width=20, bootstyle=LIGHT, text="Crear Cliente", command=lambda: [crear_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)])
    btn_crear.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Cliente", command=lambda: [actualizar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    btn_inhabilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Inhabilitar Cliente", command=lambda: [confirm_inhabilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)], state="disabled")
    btn_inhabilitar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_habilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Habilitar Cliente", command=lambda: [habilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)])
    btn_habilitar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda: [limpiar_campos_clientes(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    columns = ('Cedula', 'Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido', 'Telefono', 'Direccion')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('Cedula', text='Cedula')
    tree.heading('Primer Nombre', text='Primer Nombre')
    tree.heading('Segundo Nombre', text='Segundo Nombre')
    tree.heading('Primer Apellido', text='Primer Apellido')
    tree.heading('Segundo Apellido', text='Segundo Apellido')
    tree.heading('Telefono', text='Telefono')
    tree.heading('Direccion', text='Direccion')
    tree.grid(row=8, column=0, columnspan=3, padx=10, pady=(50, 10), sticky="nsew")

    tree.column('Cedula', width=70, anchor='w', stretch=True)
    tree.column('Primer Nombre', width=130, anchor='w', stretch=True)
    tree.column('Segundo Nombre', width=130, anchor='w', stretch=True)
    tree.column('Primer Apellido', width=130, anchor='w', stretch=True)
    tree.column('Segundo Apellido', width=130, anchor='w', stretch=True)
    tree.column('Telefono', width=100, anchor='w', stretch=True)
    tree.column('Direccion', width=100, anchor='w', stretch=True)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_cliente(tree, entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_telefono, entry_direccion)
            tree.update()
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_all(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_admin, bootstyle=DANGER)
    btn_atras.grid(row=9, column=0, columnspan=3, pady=15, sticky="n")
    
def admin_gestion_usuarios():
    limpiar_ventana()
    window.title("Gestion Profesores - Administrador")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_usuarios(tree)
            tree.update()

    def confirm_inhabilitar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este usuario?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree), refrescar_treeview(tree), confirm_window.destroy(),], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Gestion Profesores - Administrador", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_cedula = tk.Label(window, text="Cedula:", font="helvetica, 12")
    label_cedula.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_cedula = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_cedula.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_nombre1 = tk.Label(window, text="Primer Nombre:", font="helvetica, 12")
    label_nombre1.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre1.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_nombre2 = tk.Label(window, text="Segundo Nombre:", font="helvetica, 12")
    label_nombre2.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre2.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_apellido1 = tk.Label(window, text="Primer Apellido:", font="helvetica, 12")
    label_apellido1.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido1.grid(row=4, column=1, padx=(3, 10), pady=10)

    label_apellido2 = tk.Label(window, text="Segundo Apellido:", font="helvetica, 12")
    label_apellido2.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido2.grid(row=5, column=1, padx=(3, 10), pady=10)

    label_usuario = tk.Label(window, text="Usuario:", font="helvetica, 12")
    label_usuario.grid(row=6, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_usuario = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_usuario.grid(row=6, column=1, padx=(3, 10), pady=10)

    label_email = tk.Label(window, text="Email:", font="helvetica, 12")
    label_email.grid(row=7, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_email = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_email.grid(row=7, column=1, padx=(3, 10), pady=10)

    label_perfil = tk.Label(window, text="Perfil:", font="helvetica, 12")
    label_perfil.grid(row=8, column=0, sticky="e", padx=(10, 3), pady=5)
    opciones_perfil = ['Administrador', 'Usuario']
    combobox_perfil = ttk.Combobox(window, values=opciones_perfil, width=37, font="helvetica, 10", state="readonly")
    combobox_perfil.grid(row=8, column=1, padx=(3, 10), pady=10)
    combobox_perfil.current(1) 

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Usuario", command=lambda: buscar_usuario(entry_cedula, entry_nombre2, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario))
    btn_buscar.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    btn_crear = ttk.Button(window, width=20, bootstyle=LIGHT, text="Crear Usuario", command=lambda: [crear_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree), refrescar_treeview(tree)])
    btn_crear.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Usuario", command=lambda: [actualizar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    btn_inhabilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Inhabilitar Usuario", command=lambda: [confirm_inhabilitar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree), refrescar_treeview(tree)], state="disabled")
    btn_inhabilitar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_habilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Habilitar Usuario", command=lambda: [habilitar_usuario(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil, tree), refrescar_treeview(tree)])
    btn_habilitar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda: [limpiar_campos_usuarios(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_email, entry_usuario, combobox_perfil), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    columns = ('Cedula', 'Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido', 'Usuario', 'Email')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('Cedula', text='Cedula')
    tree.heading('Primer Nombre', text='Primer Nombre')
    tree.heading('Segundo Nombre', text='Segundo Nombre')
    tree.heading('Primer Apellido', text='Primer Apellido')
    tree.heading('Segundo Apellido', text='Segundo Apellido')
    tree.heading('Usuario', text='Usuario')
    tree.heading('Email', text='Email')
    tree.grid(row=9, column=0, columnspan=3, padx=10, pady=(50, 10), sticky="nsew")

    tree.column('Cedula', width=70, anchor='w', stretch=True)
    tree.column('Primer Nombre', width=130, anchor='w', stretch=True)
    tree.column('Segundo Nombre', width=130, anchor='w', stretch=True)
    tree.column('Primer Apellido', width=130, anchor='w', stretch=True)
    tree.column('Segundo Apellido', width=130, anchor='w', stretch=True)
    tree.column('Usuario', width=80, anchor='w', stretch=True)
    tree.column('Email', width=100, anchor='w', stretch=True)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_usuario(tree, entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_usuario, entry_email, combobox_perfil)
            tree.update()
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_usuarios(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_admin, bootstyle=DANGER)
    btn_atras.grid(row=10, column=0, columnspan=3, pady=15, sticky="n")

def admin_gestion_estudiantes():
    limpiar_ventana()
    window.title("Gestion Estudiantes - Administrador")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_all_estudiante(tree)
            tree.update()

    def confirm_inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este estudiante?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree) ,confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Gestion Estudiantes - Administrador", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_ID = tk.Label(window, text="ID:", font="helvetica, 12")
    label_ID.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_ID = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_ID.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_nombre1 = tk.Label(window, text="Primer Nombre:", font="helvetica, 12")
    label_nombre1.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre1.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_nombre2 = tk.Label(window, text="Segundo Nombre:", font="helvetica, 12")
    label_nombre2.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre2.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_apellido1 = tk.Label(window, text="Primer Apellido:", font="helvetica, 12")
    label_apellido1.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido1.grid(row=4, column=1, padx=(3, 10), pady=10)

    label_apellido2 = tk.Label(window, text="Segundo Apellido:", font="helvetica, 12")
    label_apellido2.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido2.grid(row=5, column=1, padx=(3, 10), pady=10)

    label_curso = tk.Label(window, text="Curso:", font="helvetica, 12")
    label_curso.grid(row=6, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_curso = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_curso.grid(row=6, column=1, padx=(3, 10), pady=10)

    label_usuario = tk.Label(window, text="Usuario:", font="helvetica, 12")
    label_usuario.grid(row=7, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_usuario = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_usuario.grid(row=7, column=1, padx=(3, 10), pady=5)

    label_email = tk.Label(window, text="Email:", font="helvetica, 12")
    label_email.grid(row=8, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_email = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_email.grid(row=8, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Estudiante", command=lambda: buscar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario))
    btn_buscar.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_crear = ttk.Button(window, width=20, bootstyle=LIGHT, text="Crear Estudiante", command=lambda: [crear_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)])
    btn_crear.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Estudiante", command=lambda: [actualizar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_inhabilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Inhabilitar Estudiante", command=lambda: [confirm_inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)], state="disabled")
    btn_inhabilitar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_habilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Habilitar Estudiante", command=lambda: [habilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)])
    btn_habilitar.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda: [limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.grid(row=7, column=2, padx=10, pady=10, sticky="w")

    columns = ('ID', 'Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido', 'Curso', 'Usuario', 'Email')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('ID', text='ID')
    tree.heading('Primer Nombre', text='Primer Nombre')
    tree.heading('Segundo Nombre', text='Segundo Nombre')
    tree.heading('Primer Apellido', text='Primer Apellido')
    tree.heading('Segundo Apellido', text='Segundo Apellido')
    tree.heading('Curso', text='Curso')
    tree.heading('Usuario', text='Usuario')
    tree.heading('Email', text='Email')
    tree.grid(row=9, column=0, columnspan=3, padx=10, pady=(50, 10), sticky="nsew")

    tree.column('ID', width=50, anchor='w', stretch=True)
    tree.column('Primer Nombre', width=130, anchor='w', stretch=True)
    tree.column('Segundo Nombre', width=130, anchor='w', stretch=True)
    tree.column('Primer Apellido', width=130, anchor='w', stretch=True)
    tree.column('Segundo Apellido', width=130, anchor='w', stretch=True)
    tree.column('Curso', width=40, anchor='w', stretch=True)
    tree.column('Usuario', width=50, anchor='w', stretch=True)
    tree.column('Email', width=100, anchor='w', stretch=True)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_estudiante(tree, entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_usuario, entry_email)
            tree.update()
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_all_estudiante(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_admin, bootstyle=DANGER) 
    btn_atras.grid(row=10, column=0, columnspan=3, pady=15, sticky="n")

def ventana_progreso_estudiantes():
    limpiar_ventana()
    window.title("Progreso Estudiantes")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_progreso_all(tree)
            tree.update()

    def confirm_borrar_progreso(tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("500x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de borrar el progreso de todos los estudiantes?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [borrar_progreso(), refrescar_treeview(tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Progreso Estudiantes", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_ID = tk.Label(window, text="ID:", font="helvetica, 12")
    label_ID.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_ID = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_ID.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_usuario = tk.Label(window, text="Usuario:", font="helvetica, 12")
    label_usuario.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_usuario = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_usuario.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_curso = tk.Label(window, text="Curso:", font="helvetica, 12")
    label_curso.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_curso = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_curso.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_nivel = tk.Label(window, text="Nivel:", font="helvetica, 12")
    label_nivel.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nivel = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_nivel.grid(row=4, column=1, padx=(3, 10), pady=5)

    label_puntos = tk.Label(window, text="Puntos:", font="helvetica, 12")
    label_puntos.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_puntos = tk.Entry(window, width=25, font=("helvetica", 10))
    entry_puntos.grid(row=5, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Estudiante", command=lambda: buscar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos))
    btn_buscar.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Progreso", command=lambda: [actualizar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda:limpiar_progreso(entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos))
    btn_limpiar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_enviar = ttk.Button(window, width=20, text="Enviar al Correo", command=lambda: enviar_info_seleccionada(tree), bootstyle=LIGHT)
    btn_enviar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_borrar = ttk.Button(window, text="Borrar todo el progreso", width=30, command=lambda: [confirm_borrar_progreso(tree), refrescar_treeview(tree)], bootstyle=WARNING) 
    btn_borrar.grid(row=6, column=0, columnspan=3, pady=(30, 30), sticky="n")

    columns = ('ID', 'Usuario', 'Curso', 'Nivel', 'Puntos')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('ID', text='ID')
    tree.heading('Usuario', text='Usuario')
    tree.heading('Curso', text='Curso')
    tree.heading('Nivel', text='Nivel')
    tree.heading('Puntos', text='Puntos')
    tree.grid(row=7, column=0, columnspan=3, padx=10, pady=(30, 10), sticky="nsew")

    tree.column('ID', width=50, anchor='center', stretch=True)
    tree.column('Usuario', width=120, anchor='center', stretch=True)
    tree.column('Curso', width=120, anchor='center', stretch=True)
    tree.column('Nivel', width=120, anchor='center', stretch=True)
    tree.column('Puntos', width=100, anchor='center', stretch=True)

    tree.bind("<<TreeviewSelect>>", lambda event:    seleccionar_progreso(tree, entry_ID, entry_usuario, entry_curso, entry_nivel, entry_puntos))
    tree.update()

    mostrar_progreso_all(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_usuario, bootstyle=DANGER) 
    btn_atras.grid(row=8, column=0, columnspan=3, pady=15, sticky="n")

def ventana_gestion_clientes():
    limpiar_ventana()
    window.title("Gestion Padres")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_clientes(tree)
            tree.update()

    def confirm_inhabilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este cliente?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree), confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Gestion Padres", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_cedula = tk.Label(window, text="Cedula:", font="helvetica, 12")
    label_cedula.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_cedula = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_cedula.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_nombre1 = tk.Label(window, text="Primer Nombre:", font="helvetica, 12")
    label_nombre1.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre1.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_nombre2 = tk.Label(window, text="Segundo Nombre:", font="helvetica, 12")
    label_nombre2.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre2.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_apellido1 = tk.Label(window, text="Primer Apellido:", font="helvetica, 12")
    label_apellido1.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido1.grid(row=4, column=1, padx=(3, 10), pady=10)

    label_apellido2 = tk.Label(window, text="Segundo Apellido:", font="helvetica, 12")
    label_apellido2.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido2.grid(row=5, column=1, padx=(3, 10), pady=10)

    label_telefono = tk.Label(window, text="Teléfono:", font="helvetica, 12")
    label_telefono.grid(row=6, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_telefono = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_telefono.grid(row=6, column=1, padx=(3, 10), pady=5)

    label_direccion = tk.Label(window, text="Dirección:", font="helvetica, 12")
    label_direccion.grid(row=7, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_direccion = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_direccion.grid(row=7, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Cliente", command=lambda: buscar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono))
    btn_buscar.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_crear = ttk.Button(window, width=20, bootstyle=LIGHT, text="Crear Cliente", command=lambda: [crear_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)])
    btn_crear.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Cliente", command=lambda: [actualizar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_inhabilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Inhabilitar Cliente", command=lambda: [confirm_inhabilitar_cliente(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono, tree), refrescar_treeview(tree)], state="disabled")
    btn_inhabilitar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda: [limpiar_campos_clientes(entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_direccion, entry_telefono), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    columns = ('Cedula', 'Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido', 'Telefono', 'Direccion')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('Cedula', text='Cedula')
    tree.heading('Primer Nombre', text='Primer Nombre')
    tree.heading('Segundo Nombre', text='Segundo Nombre')
    tree.heading('Primer Apellido', text='Primer Apellido')
    tree.heading('Segundo Apellido', text='Segundo Apellido')
    tree.heading('Telefono', text='Telefono')
    tree.heading('Direccion', text='Direccion')
    tree.grid(row=8, column=0, columnspan=3, padx=10, pady=(50, 10), sticky="nsew")

    tree.column('Cedula', width=70, anchor='w', stretch=True)
    tree.column('Primer Nombre', width=130, anchor='w', stretch=True)
    tree.column('Segundo Nombre', width=130, anchor='w', stretch=True)
    tree.column('Primer Apellido', width=130, anchor='w', stretch=True)
    tree.column('Segundo Apellido', width=130, anchor='w', stretch=True)
    tree.column('Telefono', width=100, anchor='w', stretch=True)
    tree.column('Direccion', width=100, anchor='w', stretch=True)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_cliente(tree, entry_cedula, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_telefono, entry_direccion)
            tree.update()
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_clientes(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_usuario, bootstyle=DANGER)
    btn_atras.grid(row=9, column=0, columnspan=3, pady=15, sticky="n")

def ventana_gestion_estudiantes():
    limpiar_ventana()
    window.title("Gestion Estudiantes")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    style = ttk.Style()
    style.configure("Treeview", font=("helvetica", 11))
    style.configure("Treeview.Heading", font=("helvetica", 12, "bold"))

    def refrescar_treeview(tree):
            for item in tree.get_children():
                tree.delete(item)
            mostrar_estudiante(tree)
            tree.update()

    def confirm_inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree):
        confirm_window = tk.Toplevel(window)
        confirm_window.title("Ventana de Confirmacion")
        confirm_window.geometry("300x150")
        confirm_window.grab_set()

        label_confirmar = tk.Label(confirm_window, text="¿Está seguro de inhabilitar este estudiante?", font=("Calibri", 13))
        label_confirmar.pack(pady=(20, 10))

        btn_confirmar = ttk.Button(confirm_window, text="Sí", command=lambda: [inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree) ,confirm_window.destroy()], width=10, bootstyle=SUCCESS)
        btn_confirmar.pack(side="left", padx=30, pady=20)

        btn_cancelar = ttk.Button(confirm_window, text="No", command=confirm_window.destroy, width=10, bootstyle=DANGER)
        btn_cancelar.pack(side="right", padx=30, pady=20)

    label_bienvenida = tk.Label(window, text="Gestion Estudiantes", font=("Calibri", 25))
    label_bienvenida.grid(row=0, column=0, columnspan=3, pady=(30, 30), sticky="n")

    label_ID = tk.Label(window, text="ID:", font="helvetica, 12")
    label_ID.grid(row=1, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_ID = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_ID.grid(row=1, column=1, padx=(3, 10), pady=10)

    label_nombre1 = tk.Label(window, text="Primer Nombre:", font="helvetica, 12")
    label_nombre1.grid(row=2, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre1.grid(row=2, column=1, padx=(3, 10), pady=10)

    label_nombre2 = tk.Label(window, text="Segundo Nombre:", font="helvetica, 12")
    label_nombre2.grid(row=3, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_nombre2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_nombre2.grid(row=3, column=1, padx=(3, 10), pady=10)

    label_apellido1 = tk.Label(window, text="Primer Apellido:", font="helvetica, 12")
    label_apellido1.grid(row=4, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido1 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido1.grid(row=4, column=1, padx=(3, 10), pady=10)

    label_apellido2 = tk.Label(window, text="Segundo Apellido:", font="helvetica, 12")
    label_apellido2.grid(row=5, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_apellido2 = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_apellido2.grid(row=5, column=1, padx=(3, 10), pady=10)

    label_curso = tk.Label(window, text="Curso:", font="helvetica, 12")
    label_curso.grid(row=6, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_curso = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_curso.grid(row=6, column=1, padx=(3, 10), pady=10)

    label_usuario = tk.Label(window, text="Usuario:", font="helvetica, 12")
    label_usuario.grid(row=7, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_usuario = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_usuario.grid(row=7, column=1, padx=(3, 10), pady=5)

    label_email = tk.Label(window, text="Email:", font="helvetica, 12")
    label_email.grid(row=8, column=0, sticky="e", padx=(10, 3), pady=5)
    entry_email = tk.Entry(window, width=40, font=("helvetica", 10))
    entry_email.grid(row=8, column=1, padx=(3, 10), pady=10)

    btn_buscar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Buscar Estudiante", command=lambda: buscar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario))
    btn_buscar.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    btn_crear = ttk.Button(window, width=20, bootstyle=LIGHT, text="Crear Estudiante", command=lambda: [crear_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)])
    btn_crear.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    btn_actualizar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Actualizar Estudiante", command=lambda: [actualizar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)])
    btn_actualizar.grid(row=4, column=2, padx=10, pady=10, sticky="w")

    btn_inhabilitar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Inhabilitar Estudiante", command=lambda: [confirm_inhabilitar_estudiante(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario, tree), refrescar_treeview(tree)], state="disabled")
    btn_inhabilitar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

    btn_limpiar = ttk.Button(window, width=20, bootstyle=LIGHT, text="Limpiar", command=lambda: [limpiar_campos(entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_email, entry_usuario), tree.selection_remove(tree.selection()), btn_inhabilitar.config(state="disabled")])
    btn_limpiar.grid(row=6, column=2, padx=10, pady=10, sticky="w")

    columns = ('ID', 'Primer Nombre', 'Segundo Nombre', 'Primer Apellido', 'Segundo Apellido', 'Curso', 'Usuario', 'Email')
    tree = ttk.Treeview(window, columns=columns, show='headings', style="Treeview")
    tree.heading('ID', text='ID')
    tree.heading('Primer Nombre', text='Primer Nombre')
    tree.heading('Segundo Nombre', text='Segundo Nombre')
    tree.heading('Primer Apellido', text='Primer Apellido')
    tree.heading('Segundo Apellido', text='Segundo Apellido')
    tree.heading('Curso', text='Curso')
    tree.heading('Usuario', text='Usuario')
    tree.heading('Email', text='Email')
    tree.grid(row=9, column=0, columnspan=3, padx=10, pady=(50, 10), sticky="nsew")

    tree.column('ID', width=50, anchor='w', stretch=True)
    tree.column('Primer Nombre', width=130, anchor='w', stretch=True)
    tree.column('Segundo Nombre', width=130, anchor='w', stretch=True)
    tree.column('Primer Apellido', width=130, anchor='w', stretch=True)
    tree.column('Segundo Apellido', width=130, anchor='w', stretch=True)
    tree.column('Curso', width=40, anchor='w', stretch=True)
    tree.column('Usuario', width=50, anchor='w', stretch=True)
    tree.column('Email', width=100, anchor='w', stretch=True)

    def select(event):
        selected = tree.selection()
        if selected:
            btn_inhabilitar.config(state="normal")
            seleccionar_estudiante(tree, entry_ID, entry_nombre1, entry_nombre2, entry_apellido1, entry_apellido2, entry_curso, entry_usuario, entry_email)
            tree.update()
        else:
            btn_inhabilitar.config(state="disabled")

    tree.bind("<<TreeviewSelect>>", select)

    mostrar_estudiante(tree)

    btn_atras = ttk.Button(window, text="Atrás", width=10, command=menu_principal_usuario, bootstyle=DANGER)
    btn_atras.grid(row=10, column=0, columnspan=3, pady=15, sticky="n")

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
        messagebox.showwarning("Error", f"Por favor, completa todos los campos.")
        return

    if nueva_contraseña != confirmar_contraseña:
        messagebox.showerror("Error", f"La nueva contraseña y la confirmación no coinciden.")
        return

    if len(nueva_contraseña) < 6:
        messagebox.showerror("Error", f"La contraseña debe tener al menos 6 caracteres.")
        return

    if obtener_credenciales(nombre_usuario, contraseña_actual):
        if actualizar_contraseña(nombre_usuario, nueva_contraseña):
            messagebox.showinfo("Correcto", f"Contraseña actualizada correctamente.")
            if id_estudiante_actual:
                menu_principal_estudiante(id_estudiante_actual)
            else:
                menu_principal_usuario()
        else:
            messagebox.showerror("Error", f"Hubo un problema al actualizar la contraseña.")
    else:
        messagebox.showerror("Error", f"La contraseña actual es incorrecta.")

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
                    query = "SELECT id_estudiantes FROM estudiantes WHERE nombre_usuario = %s"
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