import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from controllers.UsuarioControllers import registrar_usuario, login_usuario
from views.Menu_Admin_view import abrir_menu_admin
from views.Menu_Operario_view import abrir_menu_operario
from views.Menu_Supervisor_view import abrir_menu_supervisor
from assets.Themes import themes


def ventana_login():
    themes.init_theme()                    # detecta el sistema
    colors = themes.get_colors()            # colores iniciales

    winlog = ctk.CTk()
    winlog.geometry("600x600")
    winlog.configure(fg_color=colors["BG"])
    winlog.title("Inicio de sesión")
    winlog.iconbitmap("assets/images/icono.ico")

    def apply_theme():
        c = themes.get_colors()
        winlog.configure(fg_color=c["BG"])
        title.configure(text_color=c["TEXT"])
        login_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        reg_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        theme_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])

    def toggle():
        themes.toggle_theme()
        ctk.set_appearance_mode(themes.current_mode)  # 🔥 sincroniza con CustomTkinter
        apply_theme()                       # actualiza la vista

    # Logo
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(120,120))
    logo_label = ctk.CTkLabel(winlog, image=logo, text="")
    logo_label.pack(pady=(20,10))

    # Título
    title = ctk.CTkLabel(winlog, text="Inicio de Sesión", font=("Arial", 24, "bold"), text_color=colors["TEXT"])
    title.pack(pady=(20, 20))

    # Botón de tema (con ícono)
    theme_btn = ctk.CTkButton(winlog, text="🌙", command=toggle)
    theme_btn.pack(pady=20)

    # Entradas
    entry_id = ctk.CTkEntry(winlog, placeholder_text="ID Usuario", width=300, height=40)
    entry_id.pack(pady=10)

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

                winlog.withdraw()

                if usuario.puesto == "admin":
                    abrir_menu_admin(usuario,winlog)
                elif usuario.puesto == "operario":
                    abrir_menu_operario(usuario, winlog)
                elif usuario.puesto == "supervisor":
                    abrir_menu_supervisor(usuario,winlog)
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def abrir_registro():
        colors = themes.get_colors()
        reg = ctk.CTkToplevel(winlog)
        reg.title("Registro de Usuario")
        reg.geometry("400x400")
        reg.configure(fg_color=colors["BG"])

        ctk.CTkLabel(reg, text="Nombre", text_color=colors["TEXT"]).pack(pady=5)
        entry_nombre = ctk.CTkEntry(reg, width=250); entry_nombre.pack(pady=5)

        ctk.CTkLabel(reg, text="Apellido", text_color=colors["TEXT"]).pack(pady=5)
        entry_apellido = ctk.CTkEntry(reg, width=250); entry_apellido.pack(pady=5)

        ctk.CTkLabel(reg, text="Contraseña", text_color=colors["TEXT"]).pack(pady=5)
        entry_pass_reg = ctk.CTkEntry(reg, show="*", width=250); entry_pass_reg.pack(pady=5)

        ctk.CTkLabel(reg, text="Puesto", text_color=colors["TEXT"]).pack(pady=5)
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

        ctk.CTkButton(reg, text="Registrar", fg_color=colors["BUTTON"],
                      text_color=colors["BUTTON_TXT"], command=registrar).pack(pady=15)

    # Botones principales
    login_btn = ctk.CTkButton(winlog, text="INICIAR SESIÓN", fg_color=colors["BUTTON"],
                              text_color=colors["BUTTON_TXT"], width=200, height=40, command=login)
    login_btn.pack(pady=(20, 10))

    reg_btn = ctk.CTkButton(winlog, text="REGISTRARSE", fg_color=colors["BUTTON"],
                            text_color=colors["BUTTON_TXT"], width=200, height=40, command=abrir_registro)
    reg_btn.pack()

    winlog.mainloop()