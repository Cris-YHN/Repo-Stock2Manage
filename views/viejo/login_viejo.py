import tkinter as tk
from tkinter import ttk, messagebox
from controllers.UsuarioControllers import registrar_usuario, login_usuario
from views.Menu_Admin_viejo import abrir_menu_admin
from views.Menu_Operario_view import abrir_menu_operario
from views.Menu_Supervisor_view import abrir_menu_supervisor


def ventana_login():
    # creacion de ventana de login
    winlog = tk.Tk()
    winlog.geometry("700x500")
    winlog.configure(bg="#004643")
    winlog.title("Inicio de sesión")

    # Distintos Widgets de la ventana
    tk.Label(winlog, text="ID Usuario").pack(pady=(20, 5))
    entry_id = tk.Entry(winlog)
    entry_id.pack(pady=5)

    tk.Label(winlog, text="Contraseña").pack(pady=5)
    entry_pass = tk.Entry(winlog, show="*")
    entry_pass.pack(pady=5)

    # Fuciones internas
    def login():
        try:
            user_id = int(entry_id.get().strip())
            password = entry_pass.get()
            usuario = login_usuario(user_id, password)
            if usuario:
                if usuario.activo == 0:
                    messagebox.showerror("Acceso denegado", "Tu usuario está inactivo. Contacta al administrador.")
                    return

                messagebox.showinfo("Bienvenido", f"Hola {usuario.nombre} {usuario.apellido}")
                winlog.destroy()

                if usuario.puesto == "admin":
                    abrir_menu_admin(usuario)
                elif usuario.puesto == "operario":
                    abrir_menu_operario(usuario)
                elif usuario.puesto == "supervisor":
                    abrir_menu_supervisor(usuario)
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
        except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
        except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def abrir_registro():
        # Ventana de Registro de usuario
        reg = tk.Toplevel(winlog)
        reg.title("Registro de Usuario")
        reg.geometry("350x300")
        reg.configure(bg="#004643")

        #Entrys para el ingreso de datos
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
            try:
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
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        tk.Button(reg, text="Registrar", command=registrar).pack(pady=15)

    # --- Botones de acción ---
    tk.Button(winlog, text="Ingresar", command=login).pack(pady=(10, 5))
    tk.Button(winlog, text="Registrarse", command=abrir_registro).pack()

    winlog.mainloop()