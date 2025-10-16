import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from assets.Themes import themes
from controllers.LogsController import registrar
from controllers.ManufacturaControllers import listar_pasos
from controllers.MaterialControllers import uso_material

# Funcion de menu de operario
def abrir_menu_operario(usuario, winlog):
    colors = themes.get_colors()            # Setear Colores

    # Creacion de ventana 
    menuope = ctk.CTkToplevel()
    menuope.state("zoomed")
    menuope.geometry("1100x600")
    menuope.title("Panel Operario")
    menuope.configure(fg_color=colors["BG"])
    menuope.iconbitmap("assets/images/icono.ico")

    # Panel superior
    top_panel = ctk.CTkFrame(menuope, fg_color=colors["TOP"], height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Panel Operario",
                              font=("Arial", 20, "bold"), text_color=colors["BUTTON_TXT"])
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color=colors["BUTTON_TXT"])
    lbl_usuario.pack(side="right", padx=20)

    # Menú lateral (botones de gestion y salidas)
    menu_lateral = ctk.CTkFrame(menuope, fg_color=colors["FRAME"], width=200)
    menu_lateral.pack(side="left", fill="y")

    ctk.CTkLabel(menu_lateral, text="Menú", text_color=colors["TEXT"],
                 font=("Arial",16,"bold")).pack(pady=15)
    
    # Contenedor principal (Donde se implementan las gestiones)
    contenedor = ctk.CTkFrame(menuope, fg_color=colors["BG"])
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
        menuope.destroy()        # Cierra la ventana del menu
        winlog.deiconify()       # Vuelve a mostrar la ventana de login

    def Salir_Programa():
        menuope.destroy()        # Cierra la ventana del menu
        winlog.deiconify()       # Vuelve a mostrar la ventana de login
        winlog.destroy()         # Cierre de ventana de login y cierre exitoso del sistema

    # ***FUNCIONES INTERNAS***
    def gestion_procesar_manufactura():
        limpiar_contenedor()

        # Frame de manufactura
        frame = ctk.CTkFrame(contenedor, fg_color=colors["BG"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Procesar Manufactura",
                    font=("Arial",18,"bold"), text_color=colors["TEXT"]).pack(pady=10)

        # ID manufactura
        ctk.CTkLabel(frame, text="ID Manufactura:", text_color=colors["TEXT"]).pack(pady=5)
        entry_idmanu = ctk.CTkEntry(frame, width=150)
        entry_idmanu.pack(pady=5)

        # Combobox para los pasos
        ctk.CTkLabel(frame, text="Seleccione el Paso:", text_color=colors["TEXT"]).pack(pady=5)
        combo_pasos = ctk.CTkComboBox(frame, values=[], width=300)
        combo_pasos.pack(pady=5)

        pasos = []

        # Botón cargar pasos
        def cargar_pasos():
            nonlocal pasos
            try:
                id_manu = int(entry_idmanu.get())
            except ValueError:
                messagebox.showerror("Error", "Debe ingresar un ID numérico")
                return

            pasos = listar_pasos(id_manu)
            if not pasos:
                combo_pasos.configure(values=[])
                combo_pasos.set("")
                messagebox.showinfo("Sin datos", f"No hay pasos registrados para manufactura {id_manu}")
                return

            opciones = sorted(set([f"Paso {p.id_paso}" for p in pasos]))
            combo_pasos.configure(values=opciones)
            combo_pasos.set(opciones[0])

        ctk.CTkButton(frame, text="Cargar Pasos", fg_color=colors["BUTTON"], command=cargar_pasos).pack(pady=10)

        # Botón procesar paso
        def procesar_paso():
            selected_text = combo_pasos.get()
            if not selected_text:
                messagebox.showwarning("Atención", "Debe seleccionar un paso")
                return

            try:
                paso_num = int(selected_text.split()[1])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Formato de paso inválido")
                return

            materiales_del_paso = [p for p in pasos if p.id_paso == paso_num]

            if not materiales_del_paso:         # Aviso de faltante de material
                messagebox.showinfo("Info", f"No hay materiales para el Paso {paso_num}")
                return

            for m in materiales_del_paso:       # Descuento de material
                print(f"Descontando: id_material={m.id_material}, cantidad={m.cantidad_necesaria}")
                try:
                    uso_material(m.cantidad_necesaria, m.id_material)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return

            messagebox.showinfo("Procesado", f"Se procesó Paso {paso_num} con {len(materiales_del_paso)} materiales.")
            registrar(usuario, "Se proceso la manufactura con exito.", "MANUFAC")

        ctk.CTkButton(frame, text="Procesar Paso",
                    fg_color=colors["BUTTON"],
                    command=procesar_paso).pack(pady=10)
        
    # Botones menú lateral
    btn_inicio = ctk.CTkButton(menu_lateral, text="Inicio",
                               fg_color=colors["BUTTON"], width=180,
                               command=mostrar_inicio)
    btn_inicio.pack(pady=5)
    
    btn_gestion = ctk.CTkButton(menu_lateral, text="Procesar Manufactura",
                                fg_color=colors["BUTTON"], width=180,
                                command=gestion_procesar_manufactura)
    btn_gestion.pack(pady=5)

    btn_salir = ctk.CTkButton(menu_lateral, text="Salir",
                               fg_color="#ff4d4d", width=180,
                               command=Salir_Programa)
    btn_salir.pack(side="bottom", pady=10)

    btn_cerrar = ctk.CTkButton(menu_lateral, text="Cerrar Sesión",
                               fg_color="#ff4d4d", width=180,
                               command=cerrar_sesion)
    btn_cerrar.pack(side="bottom", pady=10)

    mostrar_inicio()