import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.RemitosControllers import (
    listar_remitos, Buscar_remito_por_id,
    modificar_proveedor, listar_detalles_por_remito
)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

COLOR_BG = "#16161a"
COLOR_FRAME = "#242629"
COLOR_TOP = "#2cb67d"
COLOR_BTN = "#7f5af0"

def gestion_remitos(parent_frame):
    # limpiar
    for w in parent_frame.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(parent_frame, fg_color=COLOR_BG)
    main.pack(fill="both", expand=True)

    # ---- Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background=COLOR_BG,
                    foreground="white",
                    fieldbackground=COLOR_BG,
                    rowheight=28)
    style.map("Treeview",
              background=[("selected", COLOR_TOP)],
              foreground=[("selected", "white")])

    frame_tree = ctk.CTkFrame(main, fg_color=COLOR_FRAME)
    frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

    dgv = ttk.Treeview(frame_tree,
                       columns=("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"),
                       show="headings")
    for c in ("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"):
        dgv.heading(c, text=c)
        dgv.column(c, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

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

    def buscarID():
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Buscar Remito")
        mini.geometry("300x200")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="ID Remito").pack(pady=5)
        entry = ctk.CTkEntry(frame_center); entry.pack(pady=5)

        def go():
            try:
                rid = int(entry.get())
                dgv.delete(*dgv.get_children())
                r = Buscar_remito_por_id(rid)
                if r:
                    dgv.insert("", "end", values=(r.id_remito, r.fecha_remito, r.id_proveedor, r.nombre_proveedor))
                else:
                    messagebox.showinfo("Buscar", f"No existe remito {rid}")
                mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(frame_center, text="Buscar", fg_color=COLOR_BTN, command=go).pack(pady=10)

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
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(frame_center, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

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
    fb = ctk.CTkFrame(main, fg_color=COLOR_FRAME)
    fb.pack(fill="x", pady=5)
    ctk.CTkButton(fb, text="Ver Todos", fg_color=COLOR_BTN, command=cargar_todos).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Buscar ID", fg_color=COLOR_BTN, command=buscarID).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Modificar Proveedor", fg_color=COLOR_BTN, command=modificar_prov_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Ver Detalles", fg_color=COLOR_BTN, command=ver_detalles).pack(side="left", padx=10, pady=10)

    cargar_todos()
