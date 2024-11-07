import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
from Pass_Management import recuperar_contrasena
from Conexiones_MySQL import obtener_credenciales, actualizar_contraseña, conectar_db
from Clientes import mostrar_clientes, crear_cliente, actualizar_cliente, inhabilitar_cliente, seleccionar_cliente, buscar_cliente, mostrar_all, habilitar_cliente
from Usuarios import buscar_usuario, inhabilitar_usuario, crear_usuario, habilitar_usuario, actualizar_usuario, mostrar_usuarios, seleccionar_usuario
from Estudiantes import buscar_estudiante, habilitar_estudiante, inhabilitar_estudiante, actualizar_estudiante, mostrar_estudiante, seleccionar_estudiante, crear_estudiante, mostrar_all_estudiante
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

    label_img = tk.Label(window, image=img, bg="cyan3")
    label_img.image = img
    label_img.pack(pady=10)
    
    x_centro = 500
    y_inicial = 450
    incremento_x = 150

    label_text = tk.Label(window, text="Inicio de Sesion", font=("Calibri", 25), bg="cyan3")
    label_text.place(x=x_centro, y=y_inicial, anchor="center")

    label_user = tk.Label(window, text="Usuario", font=("Arial", 12), bg="cyan3")
    label_user.place(x=x_centro - incremento_x, y=y_inicial + 50, anchor="center")
    entry_user = tk.Entry(window, width=30)
    entry_user.place(x=x_centro, y=y_inicial + 50, anchor="center")

    label_pass = tk.Label(window, text="Contraseña", font=("Arial", 12), bg="cyan3")
    label_pass.place(x=x_centro - incremento_x, y=y_inicial + 90, anchor="center")
    entry_pass = tk.Entry(window, width=30, show="*")
    entry_pass.place(x=x_centro, y=y_inicial + 90, anchor="center")

    btn_login = tk.Button(window, text="Ingresar", width=15, command=lambda: iniciar_sesion(entry_user.get(), entry_pass.get()))
    btn_login.place(x=x_centro, y=y_inicial + 130, anchor="center")

    label_forgot = tk.Label(window, text="¿Olvidaste tu contraseña?", fg="blue", cursor="hand2", bg="cyan3")
    label_forgot.place(x=x_centro, y=y_inicial + 180, anchor="center")
    label_forgot.bind("<Button-1>", lambda e: ventana_recuperar_contrasena())

    btn_salir = tk.Button(window, text="Salir", width=10, command=cerrar_aplicacion)
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

    label_img = tk.Label(window, image=img, bg="cyan3")
    label_img.image = img
    label_img.pack(pady=10)

    x_centro = 500
    y_inicial = 270

    label_instruccion = tk.Label(window, text="Ingresa tu usuario o correo electrónico", bg="cyan3", font=("Calibri", 25))
    label_instruccion.place(x=x_centro, y=y_inicial, anchor="center")

    entry_user_or_email = tk.Entry(window, width=30)
    entry_user_or_email.place(x=x_centro, y=y_inicial + 40, anchor="center")

    btn_recuperar = tk.Button(window, text="Recuperar Contraseña", width=20, command=lambda: recuperar_contrasena(entry_user_or_email.get()))
    btn_recuperar.place(x=x_centro, y=y_inicial + 80, anchor="center")

    btn_atras = tk.Button(window, text="Atrás", width=10, command=login_principal)
    btn_atras.place(x=x_centro, y=y_inicial + 180, anchor="center")

def menu_principal_admin():
    limpiar_ventana()
    window.title("Sistema Principal Administrador")

    label_bienvenida = tk.Label(window, text="Sistema Principal Administrador", font=("Calibri", 25), bg="cyan3")
    label_bienvenida.pack(pady=50)

    btn_gestion_clientes = tk.Button(window, text="Gestion Clientes", width=15, command=admin_gestion_clientes)
    btn_gestion_clientes.pack(pady=10)

    btn_gestion_usuario = tk.Button(window, text="Gestion Usuarios", width=15, command=admin_gestion_usuarios)
    btn_gestion_usuario.pack(pady=10)

    btn_gestion_estudiante = tk.Button(window, text="Gestion Estudiantes", width=15, command=admin_gestion_estudiantes)
    btn_gestion_estudiante.pack(pady=10)

    btn_salir = tk.Button(window, text="Cerrar Sesion", width=10, command=login_principal)
    btn_salir.pack(pady=10)

def menu_principal_usuario():
    limpiar_ventana()
    window.title("Menú Principal - Sistema de Gestión")

    label_bienvenida = tk.Label(window, text="Bienvenido al Sistema de Gestión", font=("Calibri", 25), bg="cyan3")
    label_bienvenida.pack(pady=50)

    btn_gestion_clientes = tk.Button(window, text="Gestion Clientes", width=15, command=ventana_gestion_clientes)
    btn_gestion_clientes.pack(pady=10)

    btn_gestion_estudiante = tk.Button(window, text="Gestion Estudiantes", width=15, command=ventana_gestion_estudiantes)
    btn_gestion_estudiante.pack(pady=10)

    btn_cambiar_contraseña = tk.Button(window, text="Cambiar Contraseña", width=15, command=lambda: ventana_cambiar_contraseña(menu_principal_usuario))
    btn_cambiar_contraseña.pack(pady=10)

    btn_salir = tk.Button(window, text="Cerrar Sesion", width=10, command=login_principal)
    btn_salir.pack(pady=10)

def menu_principal_estudiante(id_estudiante):
    limpiar_ventana()
    window.title("Menú Principal Estudiante")

    label_bienvenida = tk.Label(window, text="Bienvenido Estudiante", font=("Calibri", 25), bg="cyan3")
    label_bienvenida.pack(pady=50)

    def game_matematicas():
        window.withdraw()
        iniciar_juego(id_estudiante)
        window.deiconify()

    btn_matematicas = tk.Button(window, text="Matematicas", width=15, command=game_matematicas)
    btn_matematicas.pack(pady=10)

    btn_ciencias = tk.Button(window, text="Ciencias", width=15, command="***********")
    btn_ciencias.pack(pady=10)

    btn_geografia = tk.Button(window, text="Geografia", width=15, command="***********")
    btn_geografia.pack(pady=10)

    btn_cambiar_contraseña = tk.Button(window, text="Cambiar Contraseña", width=15, command=lambda: ventana_cambiar_contraseña(lambda: menu_principal_estudiante(id_estudiante_actual)))
    btn_cambiar_contraseña.pack(pady=10)

    btn_salir = tk.Button(window, text="Cerrar Sesion", width=10, command=login_principal)
    btn_salir.pack(pady=10)

def admin_gestion_clientes():
    limpiar_ventana()
    window.title("Gestion Clientes - Administrador")

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

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Cliente", command=lambda: inhabilitar_cliente(entry_cedula, tree))
    btn_inhabilitar.pack(pady=5)

    btn_habilitar = tk.Button(window, text="Habilitar Cliente", command=lambda: habilitar_cliente(entry_cedula, tree))
    btn_habilitar.pack(pady=5)

    columns = ('Cedula', 'Nombre', 'Apellido','Direccion', 'Telefono')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('Cedula', text='Cedula')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Direccion', text='Direccion')
    tree.heading('Telefono', text='Telefono')
    tree.pack(pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_cliente(tree, entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono))

    mostrar_all(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_admin)
    btn_atras.pack(pady=10)

def admin_gestion_usuarios():
    limpiar_ventana()
    window.title("Gestion Usuarios - Administrador")

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

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Usuario", command=lambda: inhabilitar_usuario(entry_cedula, tree))
    btn_inhabilitar.pack(pady=5)

    btn_habilitar = tk.Button(window, text="Habilitar Usuario", command=lambda: habilitar_usuario(entry_cedula, tree))
    btn_habilitar.pack(pady=5)

    columns = ('Cedula', 'Nombre', 'Apellido', 'Email', 'Usuario')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('Cedula', text='Cedula')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Email', text='Email')
    tree.heading('Usuario', text='Usuario')
    tree.pack(pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_usuario(tree, entry_cedula, entry_nombre, entry_apellido, entry_email, entry_usuario, combobox_perfil))

    mostrar_usuarios(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_admin)
    btn_atras.pack(pady=10)

def admin_gestion_estudiantes():
    limpiar_ventana()
    window.title("Gestion Estudiantes - Administrador")

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

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Usuario", command=lambda: inhabilitar_estudiante(entry_ID, tree))
    btn_inhabilitar.pack(pady=5)

    btn_habilitar = tk.Button(window, text="Habilitar Usuario", command=lambda: habilitar_estudiante(entry_ID, tree))
    btn_habilitar.pack(pady=5)

    columns = ('ID', 'Nombre', 'Apellido', 'Email', 'Usuario')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Email', text='Email')
    tree.heading('Usuario', text='Usuario')
    tree.pack(pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_estudiante(tree, entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario))

    mostrar_all_estudiante(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_admin)
    btn_atras.pack(pady=10)

def ventana_gestion_clientes():
    limpiar_ventana()
    window.title("Gestion Clientes")

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

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Cliente", command=lambda: inhabilitar_cliente(entry_cedula, tree))
    btn_inhabilitar.pack(pady=5)

    columns = ('Cedula', 'Nombre', 'Apellido','Direccion', 'Telefono')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('Cedula', text='Cedula')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Direccion', text='Direccion')
    tree.heading('Telefono', text='Telefono')
    tree.pack(pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_cliente(tree, entry_cedula, entry_nombre, entry_apellido, entry_direccion, entry_telefono))

    mostrar_clientes(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_usuario)
    btn_atras.pack(pady=10)

def ventana_gestion_estudiantes():
    limpiar_ventana()
    window.title("Gestion Estudiantes")

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

    btn_inhabilitar = tk.Button(window, text="Inhabilitar Usuario", command=lambda: inhabilitar_estudiante(entry_ID, tree))
    btn_inhabilitar.pack(pady=5)

    columns = ('ID', 'Nombre', 'Apellido', 'Email', 'Usuario')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nombre', text='Nombre')
    tree.heading('Apellido', text='Apellido')
    tree.heading('Email', text='Email')
    tree.heading('Usuario', text='Usuario')
    tree.pack(pady=10)

    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_estudiante(tree, entry_ID, entry_nombre, entry_apellido, entry_email, entry_usuario))

    mostrar_estudiante(tree)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=menu_principal_usuario)
    btn_atras.pack(pady=10)

def ventana_cambiar_contraseña(ventana_anterior):
    limpiar_ventana()
    window.title("Cambiar Contraseña")

    label_instruccion = tk.Label(window, text="Ingresa tu contraseña actual y la nueva contraseña", bg="cyan3", font=("Arial", 12))
    label_instruccion.pack(pady=5)

    label_actual = tk.Label(window, text="Contraseña actual", bg="cyan3", font=("Arial", 12))
    label_actual.pack(pady=5)
    entry_actual = tk.Entry(window, width=30, show="*")
    entry_actual.pack()

    label_nueva = tk.Label(window, text="Nueva contraseña", bg="cyan3", font=("Arial", 12))
    label_nueva.pack(pady=5)
    entry_nueva = tk.Entry(window, width=30, show="*")
    entry_nueva.pack()

    label_confirmar = tk.Label(window, text="Confirmar nueva contraseña", bg="cyan3", font=("Arial", 12))
    label_confirmar.pack(pady=5)
    entry_confirmar = tk.Entry(window, width=30, show="*")
    entry_confirmar.pack()

    btn_actualizar = tk.Button(window, text="Actualizar Contraseña", width=15, command=lambda: cambiar_contraseña(entry_actual.get(), entry_nueva.get(), entry_confirmar.get()))
    btn_actualizar.pack(pady=20)

    btn_atras = tk.Button(window, text="Atrás", width=10, command=ventana_anterior)
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
            messagebox.showinfo("Contraseña actualizada correctamente.")
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
    window = tk.Tk()
    window.geometry("1000x800")
    window.configure(bg="cyan3")

    login_principal()
    window.mainloop()