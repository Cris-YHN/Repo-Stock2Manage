import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
from controllers.UsuarioControllers import (
    listar_usuarios, listar_inactivos, listar_solicitudes,
    modificar_usuario, baja_usuario, alta_usuario,
    aprobar_usuario, rechazar_usuario, buscar_por_apellido
)

# Colores
ctk.set_appearance_mode("dark")
COLOR_BG       = "#16161a"
COLOR_TOP      = "#2cb67d"
COLOR_FRAME    = "#242629"
COLOR_BTN      = "#7f5af0"
COLOR_BTN_OFF  = "#3a3a3a"
COLOR_BTN_TXT  = "#ffffff"
COLOR_BTN_TXT_OFF = "#777777"

# Funcion de utilidad para botones
def set_button_state(btn, enabled: bool):
    if enabled:
        btn.configure(state="normal", fg_color=COLOR_BTN, text_color=COLOR_BTN_TXT)
    else:
        btn.configure(state="disabled", fg_color=COLOR_BTN_OFF, text_color=COLOR_BTN_TXT_OFF)

def abrir_menu_admin(usuario):
    menuadm = ctk.CTk()
    menuadm.geometry("1100x600")
    menuadm.title("Panel Administrador")
    menuadm.configure(fg_color=COLOR_BG)

    # Panel superior (verde)
    top_panel = ctk.CTkFrame(menuadm, fg_color=COLOR_TOP, height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Panel Administrador",
                              font=("Arial", 20, "bold"), text_color="white")
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color="white")
    lbl_usuario.pack(side="right", padx=20)

    # Menú lateral (botones)
    menu_lateral = ctk.CTkFrame(menuadm, fg_color=COLOR_FRAME, width=200)
    menu_lateral.pack(side="left", fill="y")

    ctk.CTkLabel(menu_lateral, text="Menú", text_color="white",
                 font=("Arial",16,"bold")).pack(pady=15)

    # contenedor principal
    contenedor = ctk.CTkFrame(menuadm, fg_color=COLOR_BG)
    contenedor.pack(side="right", fill="both", expand=True)

    # inicio con logo centrado
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(220,220))
    logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
    logo_label.pack(expand=True)          # ocupa el centro al inicio

    # Funcionalidad de gestion de usuario
    frame_gestion = None
    dgv = None
    combo_filtro = None
    frame_botones = None

    # Treeview en modo oscuro
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background=COLOR_BG,
                    foreground="white",
                    fieldbackground=COLOR_BG,
                    rowheight=28)
    style.map("Treeview",
              background=[("selected", COLOR_TOP)],
              foreground=[("selected", "white")])

    # Funciones
    def limpiar_contenedor():
        for widget in contenedor.winfo_children():
            widget.destroy()

    # Para volver a inicio
    def mostrar_inicio():
        limpiar_contenedor()
        logo_lbl = ctk.CTkLabel(contenedor, image=logo, text="")
        logo_lbl.pack(expand=True)

    # Para ingresar al modo de gestion de usuarios
    def mostrar_gestion_usuarios():
        nonlocal frame_gestion, dgv, combo_filtro, frame_botones
        limpiar_contenedor()

        # Filtro arriba
        combo_filtro = ctk.CTkComboBox(contenedor,
                        values=["Usuarios Activos","Usuarios Inactivos","Solicitudes de Usuarios"],
                        width=250)
        combo_filtro.set("Usuarios Activos")
        combo_filtro.pack(pady=10)

        # Treeview
        frame_tree = ctk.CTkFrame(contenedor, fg_color=COLOR_FRAME)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

        dgv = ttk.Treeview(frame_tree, columns=("ID","Nombre","Apellido","Puesto","Activo"), show="headings")
        for col in ("ID","Nombre","Apellido","Puesto","Activo"):
            dgv.heading(col, text=col)
            dgv.column(col, anchor="center", width=150)
        dgv.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame botones
        frame_botones = ctk.CTkFrame(contenedor, fg_color=COLOR_FRAME)
        frame_botones.pack(fill="x", pady=5)

        # Botones
        btn_buscar_apellido = ctk.CTkButton(frame_botones, text="Buscar Apellido", command=buscar_apellido)
        btn_modificar = ctk.CTkButton(frame_botones, text="Modificar", command=modificar)
        btn_baja      = ctk.CTkButton(frame_botones, text="Dar Baja", command=baja)
        btn_alta      = ctk.CTkButton(frame_botones, text="Dar Alta", command=alta)
        btn_aprobar   = ctk.CTkButton(frame_botones, text="Aprobar", command=aprobar)
        btn_rechazar  = ctk.CTkButton(frame_botones, text="Rechazar", command=rechazar)


        # Posicionar
        btn_buscar_apellido.pack(side="left", padx=5)
        btn_modificar.pack(side="left", padx=5)
        btn_baja.pack(side="left", padx=5)
        btn_alta.pack(side="left", padx=5)
        btn_aprobar.pack(side="left", padx=5)
        btn_rechazar.pack(side="left", padx=5)

        # Guardar referencias para cambio de estado
        frame_botones.btn_buscar_apellido = btn_buscar_apellido
        frame_botones.btn_modificar       = btn_modificar
        frame_botones.btn_baja            = btn_baja
        frame_botones.btn_alta            = btn_alta
        frame_botones.btn_aprobar         = btn_aprobar
        frame_botones.btn_rechazar        = btn_rechazar

        cargar_datos()
        combo_filtro.configure(command=lambda _:cargar_datos())

    def cargar_datos():
        dgv.delete(*dgv.get_children())
        sel = combo_filtro.get()
        if sel == "Usuarios Activos":
            for u in listar_usuarios():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,u.activo))
        elif sel == "Usuarios Inactivos":
            for u in listar_inactivos():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,u.activo))
        else:
            for u in listar_solicitudes():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,u.activo))
        actualizar_botones()

    def actualizar_botones():
        sel = combo_filtro.get()
        set_button_state(frame_botones.btn_modificar, sel=="Usuarios Activos")
        set_button_state(frame_botones.btn_baja,      sel=="Usuarios Activos")
        set_button_state(frame_botones.btn_alta,      sel=="Usuarios Inactivos")
        set_button_state(frame_botones.btn_aprobar,   sel=="Solicitudes de Usuarios")
        set_button_state(frame_botones.btn_rechazar,  sel=="Solicitudes de Usuarios")

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención","Selecciona un usuario")
            return None
        return dgv.item(sel)["values"]

    def modificar():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(menuadm)
        mini.title("Modificar Usuario")
        mini.geometry("400x350")

        ctk.CTkLabel(mini, text="Nombre").pack(pady=5)
        entry_nombre = ctk.CTkEntry(mini); entry_nombre.insert(0,datos[1]); entry_nombre.pack(pady=5)

        ctk.CTkLabel(mini, text="Apellido").pack(pady=5)
        entry_apellido = ctk.CTkEntry(mini); entry_apellido.insert(0,datos[2]); entry_apellido.pack(pady=5)

        ctk.CTkLabel(mini, text="Puesto").pack(pady=5)
        combo_puesto = ctk.CTkComboBox(mini, values=["admin","operario","supervisor"])
        combo_puesto.set(datos[3]); combo_puesto.pack(pady=5)

        def guardar():
            modificar_usuario(datos[0], entry_nombre.get(), entry_apellido.get(), combo_puesto.get())
            messagebox.showinfo("Éxito","Usuario actualizado")
            mini.destroy()
            cargar_datos()

        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    def buscar_apellido():
        # Ventana emergente para ingresar apellido
        mini = ctk.CTkToplevel(menuadm)
        mini.title("Buscar por Apellido")
        mini.geometry("300x150")

        mini.transient(menuadm)  # se asocia a la ventana padre
        mini.grab_set()          # bloquea interacción con el padre

        ctk.CTkLabel(mini, text="Apellido:").pack(pady=5)
        entry_ap = ctk.CTkEntry(mini, width=200)
        entry_ap.pack(pady=5)

        def search():
            try:
                apellido = entry_ap.get().strip()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if not apellido:
                    messagebox.showwarning("Atención", "Debe ingresar un apellido")
                    return
                dgv.delete(*dgv.get_children())
                resultados = buscar_por_apellido(apellido)
                if resultados:
                    for u in resultados:
                        dgv.insert("", "end", values=(u.id_usuario, u.nombre, u.apellido, u.puesto, u.activo))
                else:
                    messagebox.showinfo("Resultado", "No se encontraron usuarios con ese apellido.")
                mini.destroy()

        ctk.CTkButton(mini, text="Buscar", fg_color=COLOR_BTN, command=search).pack(pady=10)


    def baja():
        datos = get_sel()
        if datos:
            baja_usuario(datos[0]); cargar_datos()

    def alta():
        datos = get_sel()
        if datos:
            alta_usuario(datos[0]); cargar_datos()

    def aprobar():
        datos = get_sel()
        if datos:
            aprobar_usuario(datos[0]); cargar_datos()

    def rechazar():
        datos = get_sel()
        if datos:
            rechazar_usuario(datos[0]); cargar_datos()

    # Botones menú lateral
    btn_inicio = ctk.CTkButton(menu_lateral, text="Inicio",
                               fg_color=COLOR_BTN, width=180,
                               command=mostrar_inicio)
    btn_inicio.pack(pady=5)
    
    btn_gestion = ctk.CTkButton(menu_lateral, text="Gestión de Usuarios",
                                fg_color=COLOR_BTN, width=180,
                                command=mostrar_gestion_usuarios)
    btn_gestion.pack(pady=5)

    btn_cerrar = ctk.CTkButton(menu_lateral, text="Cerrar Sesión",
                               fg_color="#ff4d4d", width=180,
                               command=menuadm.destroy)
    btn_cerrar.pack(side="bottom", pady=10)

    menuadm.mainloop()
