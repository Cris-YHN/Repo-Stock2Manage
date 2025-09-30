import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
from assets.images.resources import logo_img
from controllers.ManufacturaControllers import listar_pasos
from controllers.MaterialControllers import uso_material

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

def abrir_menu_operario(usuario):
    menuope = ctk.CTkToplevel()
    menuope.geometry("1100x600")
    menuope.title("Panel Operario")
    menuope.configure(fg_color=COLOR_BG)
    menuope.iconbitmap("assets/images/icono.ico")

    # Panel superior (verde)
    top_panel = ctk.CTkFrame(menuope, fg_color=COLOR_TOP, height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Panel Operario",
                              font=("Arial", 20, "bold"), text_color="white")
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color="white")
    lbl_usuario.pack(side="right", padx=20)

    # Menú lateral (botones)
    menu_lateral = ctk.CTkFrame(menuope, fg_color=COLOR_FRAME, width=200)
    menu_lateral.pack(side="left", fill="y")

    ctk.CTkLabel(menu_lateral, text="Menú", text_color="white",
                 font=("Arial",16,"bold")).pack(pady=15)
    
    # contenedor principal
    contenedor = ctk.CTkFrame(menuope, fg_color=COLOR_BG)
    contenedor.pack(side="right", fill="both", expand=True)

    # inicio con logo centrado
    logo = ctk.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(220,220))
    logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
    logo_label.pack(expand=True)

    # Funciones
    def limpiar_contenedor():
        for widget in contenedor.winfo_children():
            widget.destroy()

    # Para volver a inicio
    def mostrar_inicio():
        limpiar_contenedor()
        logo_lbl = ctk.CTkLabel(contenedor, image=logo, text="")
        logo_lbl.pack(expand=True)


    def gestion_procesar_manufactura():
        limpiar_contenedor()

        frame = ctk.CTkFrame(contenedor, fg_color=COLOR_BG)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Procesar Manufactura",
                    font=("Arial",18,"bold"), text_color="white").pack(pady=10)

        # ID manufactura
        ctk.CTkLabel(frame, text="ID Manufactura:", text_color="white").pack(pady=5)
        entry_idmanu = ctk.CTkEntry(frame, width=150)
        entry_idmanu.pack(pady=5)

        # Combobox para los pasos
        ctk.CTkLabel(frame, text="Seleccione el Paso:", text_color="white").pack(pady=5)
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

        ctk.CTkButton(frame, text="Cargar Pasos", fg_color=COLOR_BTN, command=cargar_pasos).pack(pady=10)

        # Botón procesar paso
        def procesar_paso():
            selected_text = combo_pasos.get()
            if not selected_text:
                messagebox.showwarning("Atención", "Debe seleccionar un paso")
                return

            try:
                # extrae el número del paso seleccionado, ej. "Paso 2" → 2
                paso_num = int(selected_text.split()[1])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Formato de paso inválido")
                return

            # Filtrar todos los materiales que pertenecen a ese paso
            materiales_del_paso = [p for p in pasos if p.id_paso == paso_num]

            if not materiales_del_paso:
                messagebox.showinfo("Info", f"No hay materiales para el Paso {paso_num}")
                return

            # Descontar todos los materiales del paso
            for m in materiales_del_paso:
                print(f"Descontando: id_material={m.id_material}, cantidad={m.cantidad_necesaria}")
                uso_material(m.cantidad_necesaria, m.id_material)

            messagebox.showinfo("Procesado", f"Se procesó Paso {paso_num} con {len(materiales_del_paso)} materiales.")

        ctk.CTkButton(frame, text="Procesar Paso",
                    fg_color=COLOR_BTN,
                    command=procesar_paso).pack(pady=10)
    # Botones menú lateral
    btn_inicio = ctk.CTkButton(menu_lateral, text="Inicio",
                               fg_color=COLOR_BTN, width=180,
                               command=mostrar_inicio)
    btn_inicio.pack(pady=5)
    
    btn_gestion = ctk.CTkButton(menu_lateral, text="Gestión de Usuarios",
                                fg_color=COLOR_BTN, width=180,
                                command=gestion_procesar_manufactura)
    btn_gestion.pack(pady=5)

    btn_cerrar = ctk.CTkButton(menu_lateral, text="Cerrar Sesión",
                               fg_color="#ff4d4d", width=180,
                               command=menuope.destroy)
    btn_cerrar.pack(side="bottom", pady=10)

    menuope.mainloop()