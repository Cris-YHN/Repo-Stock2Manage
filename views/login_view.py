import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from controllers.UsuarioControllers import registrar_usuario, login_usuario, verificar_codigo, cambiar_contrasenia
from controllers.LogsController import registrar as registrolog
from views.Menu_Admin_view import abrir_menu_admin
from views.Menu_Operario_view import abrir_menu_operario
from views.Menu_Supervisor_view import abrir_menu_supervisor
from assets.Themes import themes
import re

def ventana_login():
    themes.init_theme()                    # Detecta el sistema
    colors = themes.get_colors()            # Colores iniciales

    # Creacion de ventana
    winlog = ctk.CTk()
    winlog.geometry("600x600")
    winlog.configure(fg_color=colors["BG"])
    winlog.title("Inicio de sesión")

    # Carga de Icono de APP
    icon_path = "assets/images/icono.ico"
    try:
        winlog.iconbitmap(icon_path)
    except Exception as e:
        print("iconbitmap fallback:", e)

    # Aplicar los Colores en cambio de modo
    def apply_theme():
        c = themes.get_colors()
        winlog.configure(fg_color=c["BG"])
        titulo.configure(text_color=c["TEXT"])
        theme_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        login_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        regist_btn.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])
        forgot_btn.configure(text_color=c["TEXT"])
    
    # Funcion referenciada para el cambio de modo oscuro/claro
    def toggle():
        themes.toggle_theme()
        ctk.set_appearance_mode(themes.current_mode)
        apply_theme()
    
    # Logo
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(120,120))
    logo_label = ctk.CTkLabel(winlog, image=logo, text="")
    logo_label.pack(pady=(20,10))

    # Titulo
    titulo = ctk.CTkLabel(winlog, text="Inicio de Sesión", font=("Arial", 24, "bold"), text_color=colors["TEXT"])
    titulo.pack(pady=(20, 20))

    # Boton de cambio de modo oscuro/claro
    theme_btn = ctk.CTkButton(winlog, text="Cambiar Tema", fg_color=colors["BUTTON"], command=toggle)
    theme_btn.pack(pady=20)

    # Entradas
    entry_id = ctk.CTkEntry(winlog, placeholder_text="ID Usuario", width=300, height=40)
    entry_id.pack(pady=10)

    entry_pass = ctk.CTkEntry(winlog, placeholder_text="Contraseña", show="*", width=300, height=40)
    entry_pass.pack(pady=10)

    # ***FUNCIONES INTERNAS DEL PROGRAMA***

    # Funcion Login
    def login():
        try:
            user_id = int(entry_id.get().strip())
            password = entry_pass.get()

            # Intentar loguearse
            usuario = login_usuario(user_id, password)

            # Si se devuelve un usuario válido
            if usuario:
                if usuario.intentos_fallidos >= 5:
                        messagebox.showerror("Cuenta bloqueada", "Tu cuenta fue bloqueada por 5 intentos fallidos. Contacta al administrador.")
                        registrolog(usuario, "Cuenta bloqueada por varios ingresos erroneos.", "LOGIN")
                        return
                
                if usuario.activo == 0:
                    messagebox.showerror("Acceso denegado", "Tu usuario está inactivo. Contacta al administrador.")
                    registrolog(usuario, "Intento de acceso con usuario inactivo.", "LOGIN")
                    return

                # Login correcto
                messagebox.showinfo("Bienvenido", f"Hola {usuario.nombre} {usuario.apellido}")
                registrolog(usuario, "Se logueó con éxito.", "LOGIN")

                winlog.withdraw()  # Oculta ventana login

                # Abrir menú según el puesto
                if usuario.puesto == "admin":
                    abrir_menu_admin(usuario, winlog)
                elif usuario.puesto == "operario":
                    abrir_menu_operario(usuario, winlog)
                elif usuario.puesto == "supervisor":
                    abrir_menu_supervisor(usuario, winlog)
                else:
                    messagebox.showerror("Error", "Puesto no reconocido para este usuario.")
                    winlog.deiconify()
            else: # si devuelve un None
                messagebox.showerror("Error", "Credenciales incorrectas.")

        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    
    # Funcion de Ventana Registro
    def abrir_registro():
        colors = themes.get_colors()
        winreg = ctk.CTkToplevel(winlog)
        winreg.transient(winlog)
        winreg.grab_set()
        winreg.title("Registro de Usuario")
        winreg.geometry("400x500")
        winreg.configure(fg_color=colors["BG"])

        def validar_contrasenia(passwd):
                if len(passwd) < 8:
                    return False
                if not re.search(r"[A-Z]", passwd):  # Mayúscula
                    return False
                if not re.search(r"[a-z]", passwd):  # Minúscula
                    return False
                if not re.search(r"\d", passwd):     # Número
                    return False
                if not re.search(r"[!@#$%^&*(),.?\":{}|<>]-_+", passwd):  # Especial
                    return False
                return True

        # Entrada de Datos
        ctk.CTkLabel(winreg, text="Nombre", text_color=colors["TEXT"]).pack(pady=5)
        entry_nombre = ctk.CTkEntry(winreg, width=250); entry_nombre.pack(pady=5)

        ctk.CTkLabel(winreg, text="Apellido", text_color=colors["TEXT"]).pack(pady=5)
        entry_apellido = ctk.CTkEntry(winreg, width=250); entry_apellido.pack(pady=5)

        ctk.CTkLabel(winreg, text="Puesto", text_color=colors["TEXT"]).pack(pady=5)
        combo_puesto = ctk.CTkComboBox(winreg, values=["admin", "operario", "supervisor"], width=250)
        combo_puesto.set("operario")
        combo_puesto.pack(pady=5)

        ctk.CTkLabel(winreg, text="Email", text_color=colors["TEXT"]).pack(pady=5)
        entry_email = ctk.CTkEntry(winreg, width=250); entry_email.pack(pady=5)

        ctk.CTkLabel(winreg, text="Contraseña", text_color=colors["TEXT"]).pack(pady=5)

        pass_frame = ctk.CTkFrame(winreg, fg_color="transparent")
        pass_frame.pack(pady=5)

        # Entry igual que los demás (mismo ancho)
        entry_pass_reg = ctk.CTkEntry(pass_frame, show="*", width=250)
        entry_pass_reg.pack(side="left", padx=(0, 5))

        # Botón info (mismo estilo visual que los otros)
        def mostrar_info():
            messagebox.showinfo(
                "Requisitos de contraseña",
                "La contraseña debe contener:\n"
                "• Al menos 1 letra mayúscula\n"
                "• Al menos 1 letra minúscula\n"
                "• Al menos 1 número\n"
                "• Al menos 1 carácter especial (!@#$%^&*...)\n"
                "• Mínimo 8 caracteres"
            )

        info_btn = ctk.CTkButton(
            pass_frame,
            text="ℹ️",
            width=35,
            fg_color=colors["FRAME"],      # color neutro
            hover_color=colors["BUTTON"],  # resalta al pasar el mouse
            text_color=colors["TEXT"],
            corner_radius=8,
            command=mostrar_info
        )
        info_btn.pack(side="left")

        def registrar():
            try:
                nombre = entry_nombre.get().strip()
                apellido = entry_apellido.get().strip()
                puesto = combo_puesto.get()
                email = entry_email.get()
                passwd = entry_pass_reg.get()

                if not validar_contrasenia(passwd):
                    messagebox.showwarning(
                        "Contraseña inválida",
                        "Debe contener al menos:\n"
                        "- 1 mayúscula\n- 1 minúscula\n- 1 número\n- 1 carácter especial\n- 8 caracteres mínimos"
                    )
                    return

                if nombre and apellido and passwd:
                    usuario = registrar_usuario(nombre, apellido, passwd, email, puesto)
                    messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                    registrolog(usuario, "Registro Satisfactorio", "REGISTRO")
                    winreg.destroy()
                else:
                    messagebox.showerror("Error", "Todos los campos son obligatorios")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        ctk.CTkButton(winreg, text="Registrar", fg_color=colors["BUTTON"],
                      text_color=colors["BUTTON_TXT"], command=registrar).pack(pady=15)
    
    # Ventana de Olvide mi contraseña
    def abrir_recuperar():
        colors = themes.get_colors()
        winrec = ctk.CTkToplevel(winlog)
        winrec.transient(winlog)
        winrec.grab_set()
        winrec.title("Recuperar Contraseña")
        winrec.geometry("400x400")
        winrec.configure(fg_color=colors["BG"])

        ctk.CTkLabel(winrec, text="ID de Usuario", text_color=colors["TEXT"]).pack(pady=5)
        entry_id = ctk.CTkEntry(winrec, width=250)
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
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        ctk.CTkButton(winrec, text="Enviar Código", fg_color=colors["BUTTON"],
                      text_color=colors["BUTTON_TXT"], command=enviar_codigo).pack(pady=10)

        def mostrar_verificacion(usuario):
            ctk.CTkLabel(winrec, text="Código recibido:", text_color=colors["TEXT"]).pack(pady=5)
            entry_code = ctk.CTkEntry(winrec, width=250)
            entry_code.pack(pady=5)
            ctk.CTkLabel(winrec, text="Nueva contraseña:", text_color=colors["TEXT"]).pack(pady=5)
            entry_new = ctk.CTkEntry(winrec, show="*", width=250)
            entry_new.pack(pady=5)

            def cambiar():
                try:
                    codigo = entry_code.get().strip().upper()
                    if verificar_codigo(usuario.id_usuario, codigo):
                        resultado = cambiar_contrasenia(usuario.id_usuario, entry_new.get())
                        messagebox.showinfo("Resultado", resultado)
                        if "actualizada" in resultado.lower():
                            winrec.destroy()
                    else:
                        messagebox.showerror("Error", "Código incorrecto")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ctk.CTkButton(winrec, text="Cambiar Contraseña", fg_color=colors["BUTTON"],
                          text_color=colors["BUTTON_TXT"], command=cambiar).pack(pady=15)
    
    # Botones principales
    login_btn = ctk.CTkButton(winlog, text="INICIAR SESIÓN", fg_color=colors["BUTTON"],
                              text_color=colors["BUTTON_TXT"], width=200, height=40, command=login)
    login_btn.pack(pady=(20, 10))

    regist_btn = ctk.CTkButton(winlog, text="REGISTRARSE", fg_color=colors["BUTTON"],
                            text_color=colors["BUTTON_TXT"], width=200, height=40, command=abrir_registro)
    regist_btn.pack()

    forgot_btn = ctk.CTkButton(winlog, text="Olvidé mi contraseña",
                               fg_color="transparent", text_color=colors["TEXT"],
                               command=abrir_recuperar)
    forgot_btn.pack(pady=(10, 20))

    winlog.mainloop()