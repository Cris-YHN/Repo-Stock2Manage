import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
from assets.Themes import themes
from controllers.LogsController import registrar
from controllers.UsuarioControllers import (
    listar_usuarios, listar_activos, listar_inactivos, listar_solicitudes,
    modificar_usuario, baja_usuario, alta_usuario,
    aprobar_usuario, rechazar_usuario, buscar_por_apellido)
from views.Logs_view import mostrar_logs

# Funcion para deshabilitar botones
def set_button_state(btn, enabled: bool):
    colors = themes.get_colors()
    if enabled:
        btn.configure(state="normal", fg_color=colors["BUTTON"], text_color=colors["BUTTON_TXT"])
    else:
        btn.configure(state="disabled", fg_color=colors["BUTTON_OFF"], text_color=colors["BUTTON_TXT_OFF"])

def abrir_menu_admin(usuario, winlog):
    colors = themes.get_colors() # Setear Colores

    # Creacion de ventana 
    menuadm = ctk.CTkToplevel(winlog)
    menuadm.state("zoomed")
    menuadm.geometry("1100x600")
    menuadm.title("Menú Administrador")
    menuadm.configure(fg_color=colors["BG"])

    # Panel Superior
    top_panel = ctk.CTkFrame(menuadm, fg_color=colors["TOP"], height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Menú Administrador",
                              font=("Arial", 20, "bold"), text_color=colors["BUTTON_TXT"])
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color=colors["BUTTON_TXT"])
    lbl_usuario.pack(side="right", padx=20)

    # Menú lateral (botones de gestion y salidas)
    menu_lateral = ctk.CTkFrame(menuadm, fg_color=colors["FRAME"], width=200)
    menu_lateral.pack(side="left", fill="y")

    ctk.CTkLabel(menu_lateral, text="Menú", text_color=colors["TEXT"],
                 font=("Arial",16,"bold")).pack(pady=15)
    
    # Contenedor principal (Donde se implementan las gestiones)
    contenedor = ctk.CTkFrame(menuadm, fg_color=colors["BG"])
    contenedor.pack(side="right", fill="both", expand=True)

    # Contenido de Inicio con logo centrado
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(220,220))
    logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
    logo_label.pack(expand=True)

    # Funcionalidad de gestion de usuario
    frame_gestion = None
    dgv = None
    combo_filtro = None
    frame_botones = None

    # Función para limpiar el contenido del contenedor
    def limpiar_contenedor():
        for widget in contenedor.winfo_children():
            widget.destroy()
    
    # Funcion de vista de Inicio
    def mostrar_inicio():
        limpiar_contenedor()
        logo_lbl = ctk.CTkLabel(contenedor, image=logo, text="")
        logo_lbl.pack(expand=True)
    
    # Funcion para cerrar sesion y Salir del Sistema
    def cerrar_sesion():
        menuadm.destroy()        # Cierra la ventana del menu
        winlog.deiconify()       # Vuelve a mostrar la ventana de login

    def Salir_Programa():
        menuadm.destroy()        # Cierra la ventana del menu
        winlog.deiconify()       # Vuelve a mostrar la ventana de login
        winlog.destroy()         # Cierre de ventana de login y cierre exitoso del sistema
    
    # Funcion para ingresar a la gestion de Usuarios
    def mostrar_gestion_usuarios():
        nonlocal frame_gestion, dgv, combo_filtro, frame_botones
        limpiar_contenedor()

        # Filtro de vistas del Treeview (ComboBox)
        combo_filtro = ctk.CTkComboBox(contenedor,
                        values=["Todos los Usuarios","Usuarios Activos","Usuarios Inactivos","Solicitudes de Usuarios"],
                        width=250)
        combo_filtro.set("Todos los Usuarios")
        combo_filtro.pack(pady=10)

        # Creacion de frame del Treeview dentro del contenedor
        frame_tree = ctk.CTkFrame(contenedor, fg_color=colors["FRAME"])
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Barras de Scroll para Treeview
        scrollbar_y = ctk.CTkScrollbar(frame_tree, orientation="vertical")
        scrollbar_y.pack(side="right", fill="y")

        # Treeview
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

        # Funcion para ordenamiento de mayor o menor de Columnas en Treeview
        def ordenar_por_columna(col):
            datos = [(dgv.set(k, col), k) for k in dgv.get_children("")] # Obtiene todos los items actuales
            try:
                datos = [(float(v), k) for v, k in datos]       # Intenta convertir a número si corresponde
            except ValueError:
                pass                                                  # si no es número, lo deja como texto

            reverse = sort_state.get(col, False)                # Alterna entre ascendente y descendente
            datos.sort(reverse=reverse)

            for index, (_, k) in enumerate(datos):              # Reorganiza los items
                dgv.move(k, "", index)
            
            sort_state[col] = not reverse                       # Guarda el nuevo estado de orden
        
        # Inicializacion de datos y barra de scroll en Treeview
        dgv = ttk.Treeview(frame_tree, columns=("ID","Nombre","Apellido","Email","Puesto","Estado"), show="headings", yscrollcommand=scrollbar_y.set)
        for col in ("ID","Nombre","Apellido","Email","Puesto","Estado"):
            dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
            dgv.column(col, anchor="center", width=150)
        dgv.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar_y.configure(command=dgv.yview)

        # Frame de botones
        frame_botones = ctk.CTkFrame(contenedor, fg_color=colors["FRAME"])
        frame_botones.pack(fill="x", pady=5)

        # Frame interno para centrar los botones
        botones_center = ctk.CTkFrame(frame_botones, fg_color="transparent")
        botones_center.pack(anchor="center")

        # Botones
        btn_buscar_apellido = ctk.CTkButton(botones_center, text="Buscar Apellido", fg_color=colors["BUTTON"], command=buscar_apellido)
        btn_modificar = ctk.CTkButton(botones_center, text="Modificar",fg_color=colors["BUTTON"], command=modificar)
        btn_baja      = ctk.CTkButton(botones_center, text="Dar Baja",fg_color=colors["BUTTON"], command=baja)
        btn_alta      = ctk.CTkButton(botones_center, text="Dar Alta",fg_color=colors["BUTTON"], command=alta)
        btn_aprobar   = ctk.CTkButton(botones_center, text="Aprobar",fg_color=colors["BUTTON"], command=aprobar)
        btn_rechazar  = ctk.CTkButton(botones_center, text="Rechazar",fg_color=colors["BUTTON"], command=rechazar)

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

    # Funcion de cargar todos los datos dentro del Treeview
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
    
    # Funcion para deshabilitar y habilitar botones dependiendo de la vista
    def actualizar_botones():
        sel = combo_filtro.get()
        set_button_state(frame_botones.btn_modificar, sel=="Usuarios Activos")
        set_button_state(frame_botones.btn_baja,      sel=="Usuarios Activos")
        set_button_state(frame_botones.btn_alta,      sel=="Usuarios Inactivos")
        set_button_state(frame_botones.btn_aprobar,   sel=="Solicitudes de Usuarios")
        set_button_state(frame_botones.btn_rechazar,  sel=="Solicitudes de Usuarios")
    
    # Funcion de seleccionar registro
    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención","Selecciona un usuario")
            return None
        return dgv.item(sel)["values"]
    
    # Funcion de modificar datos de Usuarios
    def modificar():
        datos = get_sel()           # Revisa que se haya seleccionado un registro
        if not datos: return

        # Creacion de mini ventana
        mini = ctk.CTkToplevel(menuadm)
        mini.transient(menuadm)
        mini.grab_set()
        mini.title("Modificar Usuario")
        mini.geometry("400x350")

        # Frame para centrar Entries y Labels
        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        # Entries, Labels y ComboBox
        ctk.CTkLabel(frame_center, text="Nombre").pack(pady=5)
        entry_nombre = ctk.CTkEntry(frame_center); entry_nombre.insert(0,datos[1]); entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Apellido").pack(pady=5)
        entry_apellido = ctk.CTkEntry(frame_center); entry_apellido.insert(0,datos[2]); entry_apellido.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Email").pack(pady=5)
        entry_email = ctk.CTkEntry(frame_center); entry_email.insert(0,datos[3]); entry_email.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Puesto").pack(pady=5)
        combo_puesto = ctk.CTkComboBox(frame_center, values=["admin","operario","supervisor"])
        combo_puesto.set(datos[4]); combo_puesto.pack(pady=5)

        # Funcion para guardar la modificacion
        def guardar():
            try:
                name = entry_nombre.get()
                surname = entry_apellido.get()
                correo = entry_email.get()
                rol = combo_puesto.get()
                modificar_usuario(datos[0], name, surname, correo, rol)
                messagebox.showinfo("Éxito","Usuario actualizado")
                registrar(usuario, "Modificacion a un Usuario.","USERS")
                mini.destroy()
                cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Botones de mini ventana
        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=20)
    
    def buscar_apellido():
        # Ventana emergente para ingresar apellido
        mini = ctk.CTkToplevel(menuadm); mini.transient(menuadm); mini.grab_set()
        mini.title("Buscar por Apellido")
        mini.geometry("300x200")
        mini.transient(menuadm)
        mini.grab_set()         

        # Frame para centrar Entries y Labels
        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        # Entrada de dato
        ctk.CTkLabel(frame_center, text="Apellido:").pack(pady=5)
        entry_ap = ctk.CTkEntry(frame_center, width=200)
        entry_ap.pack(pady=5)

        # Funcion de Busqueda
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

        # Botones de mini ventana
        ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=search).pack(pady=10)
    
    # Funcion de Baja de Usuario
    def baja():
        datos = get_sel()
        if datos:
            baja_usuario(datos[0])
            registrar(usuario, "Se dio de baja un usuario.","USERS") 
            cargar_datos()

    # Funcion de Alta de Usuario
    def alta():
        datos = get_sel()
        if datos:
            alta_usuario(datos[0])
            registrar(usuario, "Se dio de alta un usuario.","USERS")
            cargar_datos()

    # Funcion de Aprobacion de Solicitud de Usuario
    def aprobar():
        datos = get_sel()
        if datos:
            aprobar_usuario(datos[0])
            registrar(usuario, "Solicitud aprobada.","USERS")
            cargar_datos()

    # Funcion de Rechazo de Solicitud de Usuario (Borra su existencia de la BD)
    def rechazar():
        datos = get_sel()
        if datos:
            rechazar_usuario(datos[0])
            registrar(usuario, "Solicitud rechazada.","USERS")
            cargar_datos()
    
    # Funcion que trae la vista de Logs desde su archivo
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