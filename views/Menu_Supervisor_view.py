import customtkinter as ctk
from PIL import Image
from assets.Themes import themes
from views.Stock_view import gestion_stock
from views.Proveedor_view import gestion_proveedores
from views.Remitos_view import gestion_remitos
from views.Crear_manufactura_view import gestion_crear_manufactura
from views.Logs_view import mostrar_logs


# Funcion de Ventana de menu Supervisor
def abrir_menu_supervisor(usuario, winlog):
    colors = themes.get_colors()            # Setear Colores

    # Creacion de ventana 
    menusup = ctk.CTkToplevel()
    menusup.state("zoomed")
    menusup.geometry("1100x600")
    menusup.title("Menú Supervisor")
    menusup.configure(fg_color=colors["BG"])

    # Panel superior
    top_panel = ctk.CTkFrame(menusup, fg_color=colors["TOP"], height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Menú Supervisor",
                              font=("Arial", 20, "bold"), text_color=colors["BUTTON_TXT"])
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color=colors["BUTTON_TXT"])
    lbl_usuario.pack(side="right", padx=20)

    # Menú lateral (botones de gestion y salidas)
    menu_lateral = ctk.CTkFrame(menusup, fg_color=colors["FRAME"], width=200)
    menu_lateral.pack(side="left", fill="y")

    ctk.CTkLabel(menu_lateral, text="Menú", text_color=colors["TEXT"],
                 font=("Arial",16,"bold")).pack(pady=15)
    
    # Contenedor principal (Donde se implementan las gestiones)
    contenedor = ctk.CTkFrame(menusup, fg_color=colors["BG"])
    contenedor.pack(side="right", fill="both", expand=True)

    # Contenido de Inicio con logo centrado
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(220,220))
    logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
    logo_label.pack(expand=True)

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
        menusup.destroy()        # Cierra la ventana del menu
        winlog.deiconify()       # Vuelve a mostrar la ventana de login

    def Salir_Programa():
        menusup.destroy()        # Cierra la ventana del menu
        winlog.deiconify()       # Vuelve a mostrar la ventana de login
        winlog.destroy()         # Cierre de ventana de login y cierre exitoso del sistema
    
    # ***FUNCIONES INTERNAS***
    def mostrar_gestion_stock():
        limpiar_contenedor()
        gestion_stock(contenedor, usuario) 

    def mostrar_gestion_proveedor():
        limpiar_contenedor()
        gestion_proveedores(contenedor, usuario) 

    def mostrar_gestion_remitos():
        limpiar_contenedor()
        gestion_remitos(contenedor, usuario) 

    def mostrar_gestion_manufactura():
        limpiar_contenedor()
        gestion_crear_manufactura(contenedor, usuario)
    
    def mostrar_gestion_logs():
        limpiar_contenedor()
        mostrar_logs(contenedor)
    
    # Botones menú lateral
    btn_inicio = ctk.CTkButton(menu_lateral, text="Inicio",
                               fg_color=colors["BUTTON"], width=180,
                               command=mostrar_inicio)
    btn_inicio.pack(pady=5)
    
    btn_stock = ctk.CTkButton(menu_lateral, text="Gestión de Stock",
                                fg_color=colors["BUTTON"], width=180,
                                command=mostrar_gestion_stock)
    btn_stock.pack(pady=5)

    btn_proveedor = ctk.CTkButton(menu_lateral, text="Gestión de Proveedores",
                                fg_color=colors["BUTTON"], width=180, command=mostrar_gestion_proveedor
                                )
    btn_proveedor.pack(pady=5)

    btn_remitos = ctk.CTkButton(menu_lateral, text="Gestión de Remitos",
                                fg_color=colors["BUTTON"], width=180, command=mostrar_gestion_remitos
                                )
    btn_remitos.pack(pady=5)

    btn_manufactura = ctk.CTkButton(menu_lateral, text="Gestión de Manufactura",
                                fg_color=colors["BUTTON"], width=180, command=mostrar_gestion_manufactura
                                )
    btn_manufactura.pack(pady=5)

    btn_logs = ctk.CTkButton(menu_lateral, text="Ver Logs",
                            fg_color=colors["BUTTON"], width=180,
                            command=mostrar_gestion_logs)
    btn_logs.pack(pady=5)

    btn_salir = ctk.CTkButton(menu_lateral, text="Salir",
                               fg_color="#ff4d4d", width=180,
                               command=Salir_Programa)
    btn_salir.pack(side="bottom", pady=10)

    btn_cerrar = ctk.CTkButton(menu_lateral, text="Cerrar Sesión",
                               fg_color="#ff4d4d", width=180,
                               command=cerrar_sesion)
    btn_cerrar.pack(side="bottom", pady=10)
    
    mostrar_inicio()