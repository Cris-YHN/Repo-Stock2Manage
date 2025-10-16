import customtkinter as ctk
from tkinter import ttk, messagebox
from assets.Themes import themes
from controllers.LogsController import registrar # registrar(usuario, "Error al Logearse.")
from controllers.RemitosControllers import (
    listar_remitos, buscar_remitos_por_fecha,
    modificar_proveedor, listar_detalles_por_remito
)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def gestion_remitos(parent_frame,usuario):
    color = themes.get_colors()

    # limpiar
    for w in parent_frame.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(parent_frame, fg_color=color["BG"])
    main.pack(fill="both", expand=True)

    frame_tree = ctk.CTkFrame(main, fg_color=color["FRAME"])
    frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

    scrollbar_y = ctk.CTkScrollbar(frame_tree, orientation="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # ---- Treeview
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
            font=("Arial", 15, "bold"),
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

    dgv = ttk.Treeview(frame_tree,
                       columns=("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"),
                       show="headings", yscrollcommand=scrollbar_y.set)
    for col in ("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"):
        dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
        dgv.column(col, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    scrollbar_y.configure(command=dgv.yview)

    def cargar_todos():
        dgv.delete(*dgv.get_children())
        for r in listar_remitos():
            dgv.insert("", "end", values=(r.id_remito, r.fecha_remito, r.id_proveedor, r.nombre_proveedor))

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un remito")
            return None
        return dgv.item(sel)["values"]

    def buscar_por_fecha():
        mini = ctk.CTkToplevel(main)
        mini.transient(main)
        mini.grab_set()
        mini.title("Buscar Remitos por Fecha")
        mini.geometry("300x350")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        # Entradas
        ctk.CTkLabel(frame_center, text="Año (YYYY)").pack(pady=5)
        entry_year = ctk.CTkEntry(frame_center, width=100)
        entry_year.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Mes (MM)").pack(pady=5)
        entry_month = ctk.CTkEntry(frame_center, width=100)
        entry_month.pack(pady=5)

        ctk.CTkLabel(frame_center, text="Día (DD)").pack(pady=5)
        entry_day = ctk.CTkEntry(frame_center, width=100)
        entry_day.pack(pady=5)

        def go():
            try:
                año = entry_year.get().strip()
                mes = entry_month.get().strip()
                dia = entry_day.get().strip()

                # Validar formato
                if not (año.isdigit() and len(año) == 4):
                    messagebox.showerror("Error", "El año debe tener 4 dígitos.")
                    return
                if mes and (not mes.isdigit() or not (1 <= int(mes) <= 12)):
                    messagebox.showerror("Error", "Mes inválido.")
                    return
                if dia and (not dia.isdigit() or not (1 <= int(dia) <= 31)):
                    messagebox.showerror("Error", "Día inválido.")
                    return

                # Construir patrón de búsqueda
                patron = año
                if mes:
                    patron += f"-{mes.zfill(2)}"
                if dia:
                    patron += f"-{dia.zfill(2)}"

                # Buscar remitos por fecha
                dgv.delete(*dgv.get_children())
                remitos = buscar_remitos_por_fecha(patron)

                if remitos:
                    for r in remitos:
                        dgv.insert("", "end", values=(r.id_remito, r.fecha_remito, r.id_proveedor, r.nombre_proveedor))
                else:
                    messagebox.showinfo("Buscar", f"No se encontraron remitos para la fecha {patron}")

                mini.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(frame_center, text="Buscar", fg_color=color["BUTTON"], command=go).pack(pady=15)


    def modificar_prov_view():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Modificar Proveedor")
        mini.geometry("250x200")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="ID Proveedor").pack(pady=5)
        e_prov = ctk.CTkEntry(frame_center); e_prov.insert(0, datos[2]); e_prov.pack(pady=5)

        def guardar():
            try:
                modificar_proveedor(int(datos[0]), int(e_prov.get()))
                registrar(usuario, "Modificacion de proveedor de Remito.", "REMITO")
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(frame_center, text="Guardar", fg_color=color["BUTTON"], command=guardar).pack(pady=10)

    def ver_detalles():
        datos = get_sel()
        if not datos: return
        idr = int(datos[0])
        dets = listar_detalles_por_remito(idr)
        if not dets:
            messagebox.showinfo("Sin datos", "No hay detalles")
            return

        fname = f"remito_{idr}.pdf"
        doc = SimpleDocTemplate(fname, pagesize=A4)
        styles = getSampleStyleSheet()
        elems = [Paragraph(f"Detalle Remito #{idr}", styles["Title"]), Spacer(1, 12)]
        data = [["ID Remito","ID Material","Nombre Material","Cantidad"]]
        for d in dets:
            data.append([d.id_remito, d.id_material, d.nombre_material, d.cantidad])
        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ALIGN", (0,0), (-1,-1), "CENTER")
        ]))
        elems.append(table)
        doc.build(elems)
        messagebox.showinfo("PDF", f"Generado: {os.path.abspath(fname)}")

    # barra de botones
    fb = ctk.CTkFrame(main, fg_color=color["FRAME"])
    fb.pack(fill="x", pady=5)

    botones_center = ctk.CTkFrame(fb, fg_color="transparent")
    botones_center.pack(anchor="center")


    ctk.CTkButton(botones_center, text="Ver Todos", fg_color=color["BUTTON"], command=cargar_todos).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Buscar por Fecha", fg_color=color["BUTTON"], command=buscar_por_fecha).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Modificar Proveedor", fg_color=color["BUTTON"], command=modificar_prov_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Generar PDF", fg_color=color["BUTTON"], command=ver_detalles).pack(side="left", padx=10, pady=10)

    cargar_todos()
