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
    style.configure("Treeview",
                    background=colors["BG"],
                    fieldbackground=colors["BG"],
                    foreground=colors["TEXT"],
                    rowheight=26,
                    font=("Arial", 12))
    style.configure("Treeview.Heading",
                    background=colors["TOP"],
                    foreground=colors["BUTTON_TXT"],
                    font=("Arial", 13, "bold"))

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