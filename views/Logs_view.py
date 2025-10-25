import customtkinter as ctk
from tkinter import ttk, messagebox
from assets.Themes import themes
from controllers.LogsController import listar_todos, listar_por_nivel
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def mostrar_logs(contenedor):
    # Limpiar contenido previo
    for widget in contenedor.winfo_children():
        widget.destroy()

    # Setear colores
    color = themes.get_colors()

    # Frame principal
    frame_logs = ctk.CTkFrame(contenedor, fg_color=color["BG"])
    frame_logs.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    lbl_titulo = ctk.CTkLabel(frame_logs, text="Registro de Actividades", 
                              font=("Arial", 24, "bold"),
                              text_color=color["TEXT"])
    lbl_titulo.pack(pady=10)

    # Combo filtro
    combo_filtro = ctk.CTkComboBox(
        frame_logs,
        values=["Todos", "Login", "Registro", "Manufac", "Remito", "Stock", "Proveedor", "Users"],
        width=250
    )
    combo_filtro.set("Todos")
    combo_filtro.pack(pady=10)

    # Treeview
    tree_frame = ctk.CTkFrame(frame_logs, fg_color=color["FRAME"])
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
        background=color["BG"],
        foreground=color["TEXT"],
        fieldbackground=color["BG"],
        bordercolor=color["FRAME"],
        font=("Arial", 13),
        rowheight=28
    )
    style.map(
        "Treeview",
        background=[("selected", color["TOP"])],
        foreground=[("selected", color["BUTTON_TXT"])]
    )
    style.configure(
        "Treeview.Heading",
        background=color["TOP"],        
        foreground=color["BUTTON_TXT"],  
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

    def cargar_datos():
        dgv.delete(*dgv.get_children())
        sel = combo_filtro.get()
        if sel == "Todos":
            logs = listar_todos()
        else:
            logs = listar_por_nivel(sel.upper())  # usa nivel en mayúsculas

        for l in logs:
            dgv.insert("", "end", values=(l.usuario, l.accion, l.nivel, l.equipo, l.fecha))
    
    def generar_pdf_logs():
        # Recolectar datos actuales del treeview
        items = dgv.get_children()
        if not items:
            messagebox.showwarning("Sin datos", "No hay registros para exportar.")
            return

        # Crear tabla de datos
        data = [["Usuario", "Acción", "Nivel", "Equipo", "Fecha"]]
        for item in items:
            data.append(list(dgv.item(item)["values"]))

        # Nombre del archivo según filtro
        filtro = combo_filtro.get().upper()
        output_dir = os.path.join("reports", "logs")
        os.makedirs(output_dir, exist_ok=True)
        fname = os.path.join(output_dir, f"logs_{filtro}.pdf")
        doc = SimpleDocTemplate(fname, pagesize=A4)
        styles = getSampleStyleSheet()

        elems = [
            Paragraph(f"Registro de Actividades - {filtro}", styles["Title"]),
            Spacer(1, 12)
        ]

        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
            ("TEXTCOLOR", (0,0), (-1,0), colors.black),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 10),
        ]))

        elems.append(table)
        doc.build(elems)

        messagebox.showinfo("PDF generado", f"Archivo creado:\n{os.path.abspath(fname)}")

    # Botón PDF 
    btn_pdf = ctk.CTkButton(frame_logs, text="Generar PDF", fg_color=color["BUTTON"], command=generar_pdf_logs)
    btn_pdf.pack(pady=10)

    combo_filtro.configure(command=lambda _: cargar_datos())
    cargar_datos()