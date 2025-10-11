import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
from assets.Themes import themes
from controllers.LogsController import registrar
from controllers.UsuarioControllers import (
    listar_usuarios, listar_activos, listar_inactivos, listar_solicitudes,
    modificar_usuario, baja_usuario, alta_usuario,
    aprobar_usuario, rechazar_usuario, buscar_por_apellido
)
from views.Logs_view import mostrar_logs

# Funcion de utilidad para botones
def set_button_state(btn, enabled: bool):
    colors = themes.get_colors()
    if enabled:
        btn.configure(state="normal", fg_color=colors["BUTTON"], text_color=colors["BUTTON_TXT"])
    else:
        btn.configure(state="disabled", fg_color=colors["BUTTON_OFF"], text_color=colors["BUTTON_TXT_OFF"])

def abrir_menu_admin(usuario, winlog):
    colors = themes.get_colors()
    menuadm = ctk.CTkToplevel(winlog)
    menuadm.state("zoomed")
    menuadm.geometry("1100x600")
    menuadm.title("Panel Administrador")
    menuadm.configure(fg_color=colors["BG"])

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

    def Salir_Programa():
        menuadm.destroy()        # cierra el menú
        winlog.deiconify()       # 🔥 vuelve a mostrar el login
        winlog.destroy()

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

        scrollbar_y = ctk.CTkScrollbar(frame_tree, orientation="vertical")
        scrollbar_y.pack(side="right", fill="y")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=colors["BG"],
            foreground=colors["TEXT"],
            fieldbackground=colors["BG"],
            bordercolor=colors["FRAME"],
            font=("Arial", 13),
            rowheight=28
        )
        style.map(
            "Treeview",
            background=[("selected", colors["TOP"])],
            foreground=[("selected", colors["BUTTON_TXT"])]
        )
        style.configure(
            "Treeview.Heading",
            background=colors["TOP"],        
            foreground=colors["BUTTON_TXT"],  
            font=("Arial", 14, "bold"),
            relief="flat"                 
        )

        sort_state = {}

        def ordenar_por_columna(col):
            # Obtiene todos los items actuales
            datos = [(dgv.set(k, col), k) for k in dgv.get_children("")]
            
            # Intenta convertir a número si corresponde
            try:
                datos = [(float(v), k) for v, k in datos]
            except ValueError:
                pass  # si no es número, lo deja como texto
            
            # Alterna entre ascendente y descendente
            reverse = sort_state.get(col, False)
            datos.sort(reverse=reverse)
            
            # Reorganiza los items
            for index, (_, k) in enumerate(datos):
                dgv.move(k, "", index)
            
            # Guarda el nuevo estado de orden
            sort_state[col] = not reverse

        dgv = ttk.Treeview(frame_tree, columns=("ID","Nombre","Apellido","Email","Puesto","Estado"), show="headings", yscrollcommand=scrollbar_y.set)
        for col in ("ID","Nombre","Apellido","Email","Puesto","Estado"):
            dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
            dgv.column(col, anchor="center", width=150)
        dgv.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar_y.configure(command=dgv.yview)

        # Frame botones
        frame_botones = ctk.CTkFrame(contenedor, fg_color=colors["FRAME"])
        frame_botones.pack(fill="x", pady=5)

        # Frame interno para centrar los botones
        botones_center = ctk.CTkFrame(frame_botones, fg_color="transparent")
        botones_center.pack(anchor="center")

        # Botones
        btn_buscar_apellido = ctk.CTkButton(botones_center, text="Buscar Apellido", command=buscar_apellido)
        btn_modificar = ctk.CTkButton(botones_center, text="Modificar", command=modificar)
        btn_baja      = ctk.CTkButton(botones_center, text="Dar Baja", command=baja)
        btn_alta      = ctk.CTkButton(botones_center, text="Dar Alta", command=alta)
        btn_aprobar   = ctk.CTkButton(botones_center, text="Aprobar", command=aprobar)
        btn_rechazar  = ctk.CTkButton(botones_center, text="Rechazar", command=rechazar)

        for b in (btn_buscar_apellido, btn_modificar, btn_baja, btn_alta, btn_aprobar, btn_rechazar):
            b.pack(side="left", padx=5)

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
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.email,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
        elif sel == "Usuarios Activos":
            for u in listar_activos():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.email,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
        elif sel == "Usuarios Inactivos":
            for u in listar_inactivos():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.email,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
        else:
            for u in listar_solicitudes():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.email,u.puesto,ESTADOS.get(u.activo, "Desconocido")))
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

        ctk.CTkLabel(frame_center, text="Apellido").pack(pady=5)
        entry_email = ctk.CTkEntry(frame_center); entry_email.insert(0,datos[2]); entry_email.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Puesto").pack(pady=5)
        combo_puesto = ctk.CTkComboBox(frame_center, values=["admin","operario","supervisor"])
        combo_puesto.set(datos[3]); combo_puesto.pack(pady=5)

        def guardar():
            modificar_usuario(datos[0], entry_nombre.get(), entry_apellido.get(), combo_puesto.get())
            messagebox.showinfo("Éxito","Usuario actualizado")
            registrar(usuario, "Modificacion a un Usuario.","USERS")
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
                        dgv.insert("", "end", values=(u.id_usuario, u.nombre, u.apellido, u.email, u.puesto, ESTADOS.get(u.activo, "Desconocido")))
                else:
                    messagebox.showinfo("Resultado", "No se encontraron usuarios con ese apellido.")
                mini.destroy()

        ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=search).pack(pady=10)


    def baja():
        datos = get_sel()
        if datos:
            baja_usuario(datos[0])
            registrar(usuario, "Se dio de baja un usuario.","USERS") 
            cargar_datos()

    def alta():
        datos = get_sel()
        if datos:
            alta_usuario(datos[0])
            registrar(usuario, "Se dio de alta un usuario.","USERS")
            cargar_datos()

    def aprobar():
        datos = get_sel()
        if datos:
            aprobar_usuario(datos[0])
            registrar(usuario, "Solicitud aprobada.","USERS")
            cargar_datos()

    def rechazar():
        datos = get_sel()
        if datos:
            rechazar_usuario(datos[0])
            registrar(usuario, "Solicitud rechazada.","USERS")
            cargar_datos()
    
    def mostrar_gestion_logs():
        limpiar_contenedor()
        mostrar_logs(contenedor)

    # Botones menú lateral
    btn_inicio = ctk.CTkButton(menu_lateral, text="Inicio",
                               fg_color=colors["BUTTON"], width=180,
                               command=mostrar_inicio)
    btn_inicio.pack(pady=5)
    
    btn_gestion = ctk.CTkButton(menu_lateral, text="Gestión de Usuarios",
                                fg_color=colors["BUTTON"], width=180,
                                command=mostrar_gestion_usuarios)
    btn_gestion.pack(pady=5)

    btn_logs = ctk.CTkButton(menu_lateral, text="Ver Logs", 
                         fg_color=colors["BUTTON"],
                         text_color=colors["BUTTON_TXT"],
                         command=mostrar_gestion_logs)
    btn_logs.pack(pady=5, fill="x")

    btn_salir = ctk.CTkButton(menu_lateral, text="Salir",
                               fg_color="#ff4d4d", width=180,
                               command=Salir_Programa)
    btn_salir.pack(side="bottom", pady=10)

    btn_cerrar = ctk.CTkButton(menu_lateral, text="Cerrar Sesión",
                               fg_color="#ff4d4d", width=180,
                               command=cerrar_sesion)
    btn_cerrar.pack(side="bottom", pady=10)

    mostrar_inicio()
