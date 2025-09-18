import tkinter as tk
from tkinter import ttk, messagebox
from controllers.UsuarioControllers import registrar_usuario, login_usuario
from views.Menu_Admin_view import abrir_menu_admin
from views.Menu_Operario_view import abrir_menu_operario
from views.Menu_Supervisor_view import abrir_menu_supervisor


def ventana_login():
    # """Ventana principal de inicio de sesión"""
    winlog = tk.Tk()
    winlog.geometry("700x500")
    winlog.configure(bg="#004643")
    winlog.title("Inicio de sesión")

    # --- Widgets de ingreso de datos ---
    tk.Label(winlog, text="ID Usuario").pack(pady=(20, 5))
    entry_id = tk.Entry(winlog)
    entry_id.pack(pady=5)

    tk.Label(winlog, text="Contraseña").pack(pady=5)
    entry_pass = tk.Entry(winlog, show="*")
    entry_pass.pack(pady=5)

    # --- Funciones internas ---
    def login():
        user_id = entry_id.get().strip()
        password = entry_pass.get()
        usuario = login_usuario(user_id, password)
        if usuario:
            messagebox.showinfo("Bienvenido", f"Hola {usuario.nombre} {usuario.apellido}")
            if usuario.puesto == "admin":
                abrir_menu_admin(usuario)
            elif usuario.puesto == "operario":
                abrir_menu_operario(usuario)
            elif usuario.puesto == "supervisor":
                abrir_menu_supervisor(usuario)
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    def abrir_registro():
        # """Ventana de registro de nuevo usuario"""
        reg = tk.Toplevel(winlog)
        reg.title("Registro de Usuario")
        reg.geometry("350x300")
        reg.configure(bg="#004643")

        tk.Label(reg, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(reg); entry_nombre.pack(pady=5)

        tk.Label(reg, text="Apellido").pack(pady=5)
        entry_apellido = tk.Entry(reg); entry_apellido.pack(pady=5)

        tk.Label(reg, text="Contraseña").pack(pady=5)
        entry_pass_reg = tk.Entry(reg, show="*"); entry_pass_reg.pack(pady=5)

        tk.Label(reg, text="Puesto").pack(pady=5)
        combo_puesto = ttk.Combobox(reg, values=["admin", "operario", "supervisor"], state="readonly")
        combo_puesto.current(0)
        combo_puesto.pack(pady=5)

        def registrar():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            contr = entry_pass_reg.get()
            puesto = combo_puesto.get()
            if nombre and apellido and contr:
                registrar_usuario(nombre, apellido, contr, puesto)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                reg.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios")

        tk.Button(reg, text="Registrar", command=registrar).pack(pady=15)

    # --- Botones de acción ---
    tk.Button(winlog, text="Ingresar", command=login).pack(pady=(10, 5))
    tk.Button(winlog, text="Registrarse", command=abrir_registro).pack()

    winlog.mainloop()