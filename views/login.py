import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from controllers.UsuarioControllers import registrar_usuario, login_usuario
from views.Menu_Admin_view import abrir_menu_admin
from views.Menu_Operario_view import abrir_menu_operario
from views.Menu_Supervisor_view import abrir_menu_supervisor

# Configuración de tema
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("green")

# Colores personalizados de la paleta
COLOR_BG = "#16161a"
COLOR_PARAGRAPH = "#94a1b2"
COLOR_BUTTON = "#7f5af0"
COLOR_TEXT = "#ffffff"


def ventana_login():
    winlog = ctk.CTk()
    winlog.geometry("500x500")
    winlog.configure(fg_color=COLOR_BG)
    winlog.title("Inicio de sesión")
    winlog.iconbitmap("assets/images/icono.ico")

    # Logo
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(120,120))
    logo_label = ctk.CTkLabel(winlog, image=logo, text="")
    logo_label.pack(pady=(20,10))

    # Titulo
    title = ctk.CTkLabel(winlog, text="Inicio de Sesión", font=("Arial", 24, "bold"), text_color=COLOR_TEXT)
    title.pack(pady=(20, 20))

    # ID Usuario
    entry_id = ctk.CTkEntry(winlog, placeholder_text="ID Usuario", width=300, height=40)
    entry_id.pack(pady=10)

    # Contraseña
    entry_pass = ctk.CTkEntry(winlog, placeholder_text="Contraseña", show="*", width=300, height=40)
    entry_pass.pack(pady=10)

    # Funciones internas
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
        reg = ctk.CTkToplevel(winlog)
        reg.title("Registro de Usuario")
        reg.geometry("400x400")
        reg.configure(fg_color=COLOR_BG)

        ctk.CTkLabel(reg, text="Nombre", text_color=COLOR_TEXT).pack(pady=5)
        entry_nombre = ctk.CTkEntry(reg, width=250); entry_nombre.pack(pady=5)

        ctk.CTkLabel(reg, text="Apellido", text_color=COLOR_TEXT).pack(pady=5)
        entry_apellido = ctk.CTkEntry(reg, width=250); entry_apellido.pack(pady=5)

        ctk.CTkLabel(reg, text="Contraseña", text_color=COLOR_TEXT).pack(pady=5)
        entry_pass_reg = ctk.CTkEntry(reg, show="*", width=250); entry_pass_reg.pack(pady=5)

        ctk.CTkLabel(reg, text="Puesto", text_color=COLOR_TEXT).pack(pady=5)
        combo_puesto = ctk.CTkComboBox(reg, values=["admin", "operario", "supervisor"], width=250)
        combo_puesto.set("admin")
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

        ctk.CTkButton(reg, text="Registrar", fg_color=COLOR_BUTTON, text_color=COLOR_TEXT, command=registrar).pack(pady=15)

    # Botones principales
    ctk.CTkButton(winlog, text="INICIAR SESIÓN", fg_color=COLOR_BUTTON, text_color=COLOR_TEXT,
                  width=200, height=40, command=login).pack(pady=(20, 10))

    ctk.CTkButton(winlog, text="REGISTRARSE", fg_color="gray20", text_color=COLOR_TEXT,
                  width=200, height=40, command=abrir_registro).pack()

    winlog.mainloop()
