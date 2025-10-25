import customtkinter as ctk
from tkinter import ttk, messagebox
from assets.Themes import themes
from controllers.LogsController import registrar # registrar(usuario, "Error al Logearse.")
from controllers.RemitosControllers import (
    listar_remitos, buscar_remitos_por_fecha,
    modificar_proveedor, listar_detalles_por_remito)
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

# Funcion de gestion Remitos
def gestion_remitos(contenedor, usuario):
    color = themes.get_colors()             # Setear colores
    
    # limpiar contenedor
    for w in contenedor.winfo_children():
        w.destroy()

    # marco principal
    main = ctk.CTkFrame(contenedor, fg_color=color["BG"])
    main.pack(fill="both", expand=True)

    # Creacion de frame del Treeview dentro del contenedor
    frame_tree = ctk.CTkFrame(main, fg_color=color["FRAME"])
    frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Barras de Scroll para Treeview
    scrollbar_y = ctk.CTkScrollbar(frame_tree, orientation="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # Treeview
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

    # Funcion para ordenamiento de mayor o menor de Columnas en Treeview
    def ordenar_por_columna(col):
            datos = [(dgv.set(k, col), k) for k in dgv.get_children("")] # Obtiene todos los items actuales
            try:
                datos = [(float(v), k) for v, k in datos]       # Intenta convertir a número si corresponde
            except ValueError:
                pass                                            # si no es número, lo deja como texto

            reverse = sort_state.get(col, False)                # Alterna entre ascendente y descendente
            datos.sort(reverse=reverse)

            for index, (_, k) in enumerate(datos):              # Reorganiza los items
                dgv.move(k, "", index)
            
            sort_state[col] = not reverse                       # Guarda el nuevo estado de orden
    
    # Inicializacion de datos y barra de scroll en Treeview
    dgv = ttk.Treeview(frame_tree,
                       columns=("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"),
                       show="headings", yscrollcommand=scrollbar_y.set)
    for col in ("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"):
        dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
        dgv.column(col, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    scrollbar_y.configure(command=dgv.yview)

    # Funcion de cargar todos los datos dentro del Treeview
    def cargar_todos():
        dgv.delete(*dgv.get_children())
        for r in listar_remitos():
            dgv.insert("", "end", values=(r.id_remito, r.fecha_remito, r.id_proveedor, r.nombre_proveedor))

    # Funcion de seleccionar registro
    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un remito")
            return None
        return dgv.item(sel)["values"]
    
    # ***Funciones Internas***
    # Funcion de Buscar Remito por Fecha
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

                # Concatenar la fecha
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
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

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
                prov = int(e_prov.get())
                modificar_proveedor(int(datos[0]), prov)
                registrar(usuario, "Modificacion de proveedor de Remito.", "REMITO")
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
        ctk.CTkButton(frame_center, text="Guardar", fg_color=color["BUTTON"], command=guardar).pack(pady=10)

    # Funcion para generar PDF de Remito
    def ver_detalles():
        datos = get_sel()
        if not datos: return
        idr = int(datos[0])
        dets = listar_detalles_por_remito(idr)
        if not dets:
            messagebox.showinfo("Sin datos", "No hay detalles")
            return

        output_dir = os.path.join("reports", "remitos")
        os.makedirs(output_dir, exist_ok=True)
        fname = os.path.join(output_dir, f"remito_{idr}.pdf")
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

    # Frame de botones
    fb = ctk.CTkFrame(main, fg_color=color["FRAME"])
    fb.pack(fill="x", pady=5)

    # Frame de centrar botones
    botones_center = ctk.CTkFrame(fb, fg_color="transparent")
    botones_center.pack(anchor="center")

    # Botones
    ctk.CTkButton(botones_center, text="Ver Todos", fg_color=color["BUTTON"], command=cargar_todos).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Buscar por Fecha", fg_color=color["BUTTON"], command=buscar_por_fecha).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Modificar Proveedor", fg_color=color["BUTTON"], command=modificar_prov_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Generar PDF", fg_color=color["BUTTON"], command=ver_detalles).pack(side="left", padx=10, pady=10)

    # inicial
    cargar_todos()