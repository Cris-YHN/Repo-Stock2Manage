import tkinter as tk
from tkinter import ttk, messagebox
from controllers.UsuarioControllers import UsuarioController

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de sesión")
        self.controller = UsuarioController()

        # --- Login ---
        tk.Label(root, text="ID Usuario").pack(pady=(20, 5))
        self.entry_id = tk.Entry(root)
        self.entry_id.pack(pady=5)

        tk.Label(root, text="Contraseña").pack(pady=5)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack(pady=5)

        tk.Button(root, text="Ingresar", command=self.login).pack(pady=(10,5))
        tk.Button(root, text="Registrarse", command=self.abrir_registro).pack()

    # ---- Login ----
    def login(self):
        user_id = self.entry_id.get()
        password = self.entry_pass.get()
        usuario = self.controller.login_usuario(user_id, password)
        if usuario:
            messagebox.showinfo("Bienvenido", f"Hola {usuario.nombre} {usuario.apellido}")
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    # ---- Registro en ventana aparte ----
    def abrir_registro(self):
        reg = tk.Toplevel(self.root)
        reg.title("Registro de Usuario")
        reg.geometry("350x300")
        reg.configure(bg="#004643")

        tk.Label(reg, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(reg); entry_nombre.pack(pady=5)

        tk.Label(reg, text="Apellido").pack(pady=5)
        entry_apellido = tk.Entry(reg); entry_apellido.pack(pady=5)

        tk.Label(reg, text="Contraseña").pack(pady=5)
        entry_pass = tk.Entry(reg, show="*"); entry_pass.pack(pady=5)

        tk.Label(reg, text="Puesto").pack(pady=5)
        combo_puesto = ttk.Combobox(
            reg, values=["admin", "operario", "supervisor"], state="readonly"
        )
        combo_puesto.current(0)
        combo_puesto.pack(pady=5)

        def registrar():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            contr = entry_pass.get()
            puesto = combo_puesto.get()
            if nombre and apellido and contr:
                self.controller.registrar_usuario(nombre, apellido, contr, puesto)
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                reg.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios")

        tk.Button(reg, text="Registrar", command=registrar).pack(pady=15)