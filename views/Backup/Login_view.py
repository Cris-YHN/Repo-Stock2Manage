import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from controllers.UsuarioControllers import registrar_usuario, login_usuario, obtener_usuario_por_id
from controllers.LogsController import registrar as registrolog
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

    # 🔥 Cargar ícono global para toda la app
    icon_path = "assets/images/icono.ico"
    try:
        winlog.iconbitmap(icon_path)  # Tkinter clásico (solo por compatibilidad)
    except Exception as e:
        print("iconbitmap fallback:", e)

    # CustomTkinter: se aplica correctamente después de update()
    winlog.update_idletasks()
    try:
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        winlog.wm_iconphoto(True, icon_image)
    except Exception as e:
        print("wm_iconphoto fallback:", e)

    def apply_theme():
        c = themes.get_colors()
        winlog.configure(fg_color=c["BG"])
        title.configure(text_color=c["TEXT"])
        login_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        reg_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        theme_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        forgot_btn.configure(text_color=c["TEXT"])

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
    theme_btn = ctk.CTkButton(winlog, text="🌙", fg_color=colors["BUTTON"], command=toggle)
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
                    registrolog(usuario, "Error al Logearse.", "LOGIN")
                    return

                messagebox.showinfo("Bienvenido", f"Hola {usuario.nombre} {usuario.apellido}")
                registrolog(usuario, "Se logeo con exito.", "LOGIN")

                winlog.withdraw()

                if usuario.puesto == "admin":
                    abrir_menu_admin(usuario, winlog)
                elif usuario.puesto == "operario":
                    abrir_menu_operario(usuario, winlog)
                elif usuario.puesto == "supervisor":
                    abrir_menu_supervisor(usuario,winlog)
            else:
                check_user = obtener_usuario_por_id(user_id)
                if check_user and check_user.activo == 0:
                    messagebox.showerror("Cuenta bloqueada", "Tu cuenta fue bloqueada por 5 intentos fallidos hoy. Contacta al administrador.")
                else:
                    messagebox.showerror("Error", "Credenciales inválidas.")
                return
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def abrir_registro():
        colors = themes.get_colors()
        reg = ctk.CTkToplevel(winlog); reg.transient(winlog); reg.grab_set()
        reg.title("Registro de Usuario")
        reg.geometry("400x400")
        reg.configure(fg_color=colors["BG"])

        ctk.CTkLabel(reg, text="Nombre", text_color=colors["TEXT"]).pack(pady=5)
        entry_nombre = ctk.CTkEntry(reg, width=250); entry_nombre.pack(pady=5)

        ctk.CTkLabel(reg, text="Apellido", text_color=colors["TEXT"]).pack(pady=5)
        entry_apellido = ctk.CTkEntry(reg, width=250); entry_apellido.pack(pady=5)

        ctk.CTkLabel(reg, text="Contraseña", text_color=colors["TEXT"]).pack(pady=5)
        entry_pass_reg = ctk.CTkEntry(reg, show="*", width=250); entry_pass_reg.pack(pady=5)

        ctk.CTkLabel(reg, text="Email", text_color=colors["TEXT"]).pack(pady=5)
        entry_email = ctk.CTkEntry(reg, width=250); entry_email.pack(pady=5)

        ctk.CTkLabel(reg, text="Puesto", text_color=colors["TEXT"]).pack(pady=5)
        combo_puesto = ctk.CTkComboBox(reg, values=["admin", "operario", "supervisor"], width=250)
        combo_puesto.set("admin")
        combo_puesto.pack(pady=5)

        def registrar():
            try:
                nombre = entry_nombre.get().strip()
                apellido = entry_apellido.get().strip()
                contr = entry_pass_reg.get()
                email = entry_email.get()
                puesto = combo_puesto.get()
                if nombre and apellido and contr:
                    usuario = registrar_usuario(nombre, apellido, contr, email, puesto)
                    messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                    registrolog(usuario, "Registro Satisfactorio", "REGISTRO")
                    reg.destroy()
                else:
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        ctk.CTkButton(reg, text="Registrar", fg_color=colors["BUTTON"],
                      text_color=colors["BUTTON_TXT"], command=registrar).pack(pady=15)
    
    def abrir_recuperar():
        colors = themes.get_colors()
        rec = ctk.CTkToplevel(winlog)
        rec.transient(winlog)
        rec.grab_set()
        rec.title("Recuperar Contraseña")
        rec.geometry("400x400")
        rec.configure(fg_color=colors["BG"])

        ctk.CTkLabel(rec, text="ID de Usuario", text_color=colors["TEXT"]).pack(pady=5)
        entry_id = ctk.CTkEntry(rec, width=250)
        entry_id.pack(pady=5)

        def enviar_codigo():
            from controllers.UsuarioControllers import enviar_codigo_recuperacion
            try:
                user_id = int(entry_id.get())
                usuario = enviar_codigo_recuperacion(user_id)
                if usuario:
                    messagebox.showinfo("Enviado", f"Se envió un código a {usuario.email}")
                    mostrar_verificacion(usuario)
                else:
                    messagebox.showerror("Error", "Usuario no encontrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(rec, text="Enviar Código", fg_color=colors["BUTTON"],
                      text_color=colors["BUTTON_TXT"], command=enviar_codigo).pack(pady=10)

        def mostrar_verificacion(usuario):
            ctk.CTkLabel(rec, text="Código recibido:", text_color=colors["TEXT"]).pack(pady=5)
            entry_code = ctk.CTkEntry(rec, width=250)
            entry_code.pack(pady=5)
            ctk.CTkLabel(rec, text="Nueva contraseña:", text_color=colors["TEXT"]).pack(pady=5)
            entry_new = ctk.CTkEntry(rec, show="*", width=250)
            entry_new.pack(pady=5)

            def cambiar():
                from controllers.UsuarioControllers import verificar_codigo, cambiar_contrasenia
                codigo = entry_code.get().strip().upper()
                if verificar_codigo(usuario.id_usuario, codigo):
                    resultado = cambiar_contrasenia(usuario.id_usuario, entry_new.get())
                    messagebox.showinfo("Resultado", resultado)
                    if "actualizada" in resultado.lower():
                        rec.destroy()
                else:
                    messagebox.showerror("Error", "Código incorrecto")

            ctk.CTkButton(rec, text="Cambiar Contraseña", fg_color=colors["BUTTON"],
                          text_color=colors["BUTTON_TXT"], command=cambiar).pack(pady=15)

    # Botones principales
    login_btn = ctk.CTkButton(winlog, text="INICIAR SESIÓN", fg_color=colors["BUTTON"],
                              text_color=colors["BUTTON_TXT"], width=200, height=40, command=login)
    login_btn.pack(pady=(20, 10))

    reg_btn = ctk.CTkButton(winlog, text="REGISTRARSE", fg_color=colors["BUTTON"],
                            text_color=colors["BUTTON_TXT"], width=200, height=40, command=abrir_registro)
    reg_btn.pack()

    forgot_btn = ctk.CTkButton(winlog, text="Olvidé mi contraseña",
                               fg_color="transparent", text_color=colors["TEXT"],
                               command=abrir_recuperar)
    forgot_btn.pack(pady=(10, 20))

    winlog.mainloop()