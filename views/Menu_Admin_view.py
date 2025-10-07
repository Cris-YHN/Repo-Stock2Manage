import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
from assets.Themes import themes
from controllers.UsuarioControllers import (
    listar_usuarios, listar_activos, listar_inactivos, listar_solicitudes,
    modificar_usuario, baja_usuario, alta_usuario,
    aprobar_usuario, rechazar_usuario, buscar_por_apellido
)

# Funcion de utilidad para botones
def set_button_state(btn, enabled: bool):
    colors = themes.get_colors()
    if enabled:
        btn.configure(state="normal", fg_color=colors["BUTTON"], text_color=colors["BUTTON_TXT"])
    else:
        btn.configure(state="disabled", fg_color=colors["BUTTON_OFF"], text_color=colors["BUTTON_TXT_OFF"])

def abrir_menu_admin(usuario, winlog):
    colors = themes.get_colors()
    menuadm = ctk.CTkToplevel()
    menuadm.geometry("1100x600")
    menuadm.title("Panel Administrador")
    menuadm.configure(fg_color=colors["BG"])
    menuadm.iconbitmap("assets/images/icono.ico")

    def apply_theme():
        c = themes.get_colors()
        menuadm.configure(fg_color=c["BG"])
        top_panel.configure(fg_color=c["TOP"])
        menu_lateral.configure(fg_color=c["FRAME"])
        contenedor.configure(fg_color=c["BG"])

        # Actualizar labels y botones
        lbl_titulo.configure(text_color=c["BUTTON_TXT"])
        lbl_usuario.configure(text_color=c["BUTTON_TXT"])

        for widget in menu_lateral.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=c["TEXT"])
            elif isinstance(widget, ctk.CTkButton):
                if widget.cget("text") == "Cerrar Sesión":
                    widget.configure(fg_color="#ff4d4d", text_color="white")
                else:
                    widget.configure(fg_color=c["BUTTON"], text_color=c["BUTTON_TXT"])

        # --- 🔥 Treeview dinámico que realmente cambia ---
        style = ttk.Style()

        # 💡 alternar tema base para romper la caché visual
        current_theme = style.theme_use()
        style.theme_use("clam" if current_theme == "default" else "default")

        # aplicar nuevos colores
        style.configure(
            "Treeview",
            background=c["BG"],
            foreground=c["TEXT"],
            fieldbackground=c["BG"],
            bordercolor=c["FRAME"],
            font=("Arial", 13),
            rowheight=28
        )
        style.map(
            "Treeview",
            background=[("selected", c["TOP"])],
            foreground=[("selected", c["TEXT"])]
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 14, "bold"),
            background=c["TOP"],
            foreground="white"
        )

        # 🔧 Reasignar y refrescar todos los Treeview visibles
        def refrescar_treeview(widget):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Treeview):
                    child.configure(style="Treeview")
                    child.update_idletasks()
                else:
                    refrescar_treeview(child)
        refrescar_treeview(contenedor)

    def toggle():
        themes.toggle_theme()
        ctk.set_appearance_mode(themes.current_mode)  # 🔥 sincroniza con CustomTkinter
        apply_theme()                                 # ahora actualiza TODO
        btn_tema.configure(
            text="☀️ Modo Claro" if themes.current_mode == "dark" else "🌙 Modo Oscuro"
        )

    # Panel superior (verde)
    top_panel = ctk.CTkFrame(menuadm, fg_color=colors["TOP"], height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Panel Administrador",
                              font=("Arial", 20, "bold"), text_color=colors["BUTTON_TXT"])
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color=colors["BUTTON_TXT"])
    lbl_usuario.pack(side="right", padx=20)

    # Menú lateral (botones)
    menu_lateral = ctk.CTkFrame(menuadm, fg_color=colors["FRAME"], width=200)
    menu_lateral.pack(side="left", fill="y")

    ctk.CTkLabel(menu_lateral, text="Menú", text_color=colors["TEXT"],
                 font=("Arial",16,"bold")).pack(pady=15)

    # contenedor principal
    contenedor = ctk.CTkFrame(menuadm, fg_color=colors["BG"])
    contenedor.pack(side="right", fill="both", expand=True)

    # inicio con logo centrado
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(220,220))
    logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
    logo_label.pack(expand=True)

    # Funcionalidad de gestion de usuario
    frame_gestion = None
    dgv = None
    combo_filtro = None
    frame_botones = None

    # Funciones
    def limpiar_contenedor():
        for widget in contenedor.winfo_children():
            widget.destroy()

    # Para volver a inicio
    def mostrar_inicio():
        limpiar_contenedor()
        logo_lbl = ctk.CTkLabel(contenedor, image=logo, text="")
        logo_lbl.pack(expand=True)
    
    def cerrar_sesion():
        menuadm.destroy()        # cierra el menú
        winlog.deiconify()       # 🔥 vuelve a mostrar el login

    # Para ingresar al modo de gestion de usuarios
    def mostrar_gestion_usuarios():
        nonlocal frame_gestion, dgv, combo_filtro, frame_botones
        limpiar_contenedor()

        # Filtro arriba
        combo_filtro = ctk.CTkComboBox(contenedor,
                        values=["Todos los Usuarios","Usuarios Activos","Usuarios Inactivos","Solicitudes de Usuarios"],
                        width=250)
        combo_filtro.set("Todos los Usuarios")
        combo_filtro.pack(pady=10)

        # Treeview
        frame_tree = ctk.CTkFrame(contenedor, fg_color=colors["FRAME"])
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

        dgv = ttk.Treeview(frame_tree, columns=("ID","Nombre","Apellido","Puesto","Estado"), show="headings")
        for col in ("ID","Nombre","Apellido","Puesto","Estado"):
            dgv.heading(col, text=col)
            dgv.column(col, anchor="center", width=150)
        dgv.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame botones
        frame_botones = ctk.CTkFrame(contenedor, fg_color=colors["FRAME"])
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

    # Diccionario de estados
    ESTADOS = {
        0: "En solicitud",
        1: "Activo",
        2: "Inactivo"
    }

    def cargar_datos():
        dgv.delete(*dgv.get_children())
        sel = combo_filtro.get()
        if sel == "Todos los Usuarios":
            for u in listar_usuarios():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
        elif sel == "Usuarios Activos":
            for u in listar_activos():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
        elif sel == "Usuarios Inactivos":
            for u in listar_inactivos():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
        else:
            for u in listar_solicitudes():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
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
        mini = ctk.CTkToplevel(menuadm); mini.transient(menuadm); mini.grab_set()
        mini.title("Modificar Usuario")
        mini.geometry("400x350")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre").pack(pady=5)
        entry_nombre = ctk.CTkEntry(frame_center); entry_nombre.insert(0,datos[1]); entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Apellido").pack(pady=5)
        entry_apellido = ctk.CTkEntry(frame_center); entry_apellido.insert(0,datos[2]); entry_apellido.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Puesto").pack(pady=5)
        combo_puesto = ctk.CTkComboBox(frame_center, values=["admin","operario","supervisor"])
        combo_puesto.set(datos[3]); combo_puesto.pack(pady=5)

        def guardar():
            modificar_usuario(datos[0], entry_nombre.get(), entry_apellido.get(), combo_puesto.get())
            messagebox.showinfo("Éxito","Usuario actualizado")
            mini.destroy()
            cargar_datos()

        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=20)

    def buscar_apellido():
        # Ventana emergente para ingresar apellido
        mini = ctk.CTkToplevel(menuadm); mini.transient(menuadm); mini.grab_set()
        mini.title("Buscar por Apellido")
        mini.geometry("300x200")

        mini.transient(menuadm)  # se asocia a la ventana padre
        mini.grab_set()          # bloquea interacción con el padre

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Apellido:").pack(pady=5)
        entry_ap = ctk.CTkEntry(frame_center, width=200)
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
                        dgv.insert("", "end", values=(u.id_usuario, u.nombre, u.apellido, u.puesto, ESTADOS.get(u.activo, "Desconocido")))
                else:
                    messagebox.showinfo("Resultado", "No se encontraron usuarios con ese apellido.")
                mini.destroy()

        ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=search).pack(pady=10)


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
                               fg_color=colors["BUTTON"], width=180,
                               command=mostrar_inicio)
    btn_inicio.pack(pady=5)
    
    btn_gestion = ctk.CTkButton(menu_lateral, text="Gestión de Usuarios",
                                fg_color=colors["BUTTON"], width=180,
                                command=mostrar_gestion_usuarios)
    btn_gestion.pack(pady=5)

    btn_cerrar = ctk.CTkButton(menu_lateral, text="Cerrar Sesión",
                               fg_color="#ff4d4d", width=180,
                               command=cerrar_sesion)
    btn_cerrar.pack(side="bottom", pady=10)

    btn_tema = ctk.CTkButton(menu_lateral, text="🌙 Modo Oscuro",
                               fg_color=colors["BUTTON"], width=180,
                               command=toggle)
    btn_tema.pack(side="bottom", pady=10)

    mostrar_inicio()
