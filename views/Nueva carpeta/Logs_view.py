import customtkinter as ctk
from tkinter import ttk
from assets.Themes import themes
from controllers.LogsController import listar_todos

def mostrar_logs(contenedor):
    # Limpiar contenido previo
    for widget in contenedor.winfo_children():
        widget.destroy()

    # Setear colores
    colors = themes.get_colors()

    # Frame principal
    frame_logs = ctk.CTkFrame(contenedor, fg_color=colors["BG"])
    frame_logs.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    lbl_titulo = ctk.CTkLabel(frame_logs, text="Registro de Actividades", 
                              font=("Arial", 24, "bold"),
                              text_color=colors["TEXT"])
    lbl_titulo.pack(pady=10)

    # Treeview
    tree_frame = ctk.CTkFrame(frame_logs, fg_color=colors["FRAME"])
    tree_frame.pack(fill="both", expand=True, pady=10)

    scrollbar_y = ctk.CTkScrollbar(tree_frame, orientation="vertical")
    scrollbar_y.pack(side="right", fill="y")

    dgv = ttk.Treeview(tree_frame, columns=("Usuario", "Acción", "Nivel", "Equipo", "Fecha"), show="headings", yscrollcommand=scrollbar_y.set)
    dgv.pack(fill="both", expand=True)

    # Configurar encabezados
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

    for col in ("Usuario", "Acción", "Nivel", "Equipo", "Fecha"):
        dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
        dgv.column(col, anchor="center", width=160)

    scrollbar_y.configure(command=dgv.yview)

    for col in ("Usuario", "Acción", "Nivel", "Equipo", "Fecha"):
        dgv.heading(col, text=col)
        dgv.column(col, anchor="center", width=160)

    scrollbar_y.configure(command=dgv.yview)

    def cargar_todos():
        dgv.delete(*dgv.get_children())
        for l in listar_todos():
            dgv.insert("", "end", values=(
                l.usuario, l.accion, l.nivel, l.equipo, l.fecha
            ))
    
    cargar_todos()