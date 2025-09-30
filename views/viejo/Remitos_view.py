import tkinter as tk
from tkinter import ttk, messagebox
from controllers.RemitosControllers import listar_remitos, Buscar_remito_por_id, modificar_proveedor, listar_detalles_por_remito

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def Gestion_Remitos():
    Wrem = tk.Toplevel()
    Wrem.title("Gestion Remitos")
    Wrem.geometry("800x500")
    Wrem.configure(bg="#004643")

    # Tabla
    dgv = ttk.Treeview(Wrem, columns=("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"), show="headings")
    for col in ("ID Remito", "Fecha", "ID Proveedor", "Nombre Proveedor"):
        dgv.heading(col, text=col)
    dgv.pack(fill=tk.BOTH, expand=True)

    def cargar_todos():
        dgv.delete(*dgv.get_children())  #Borra datos que estaban en el treeview
        for r in listar_remitos(): #Llama a la funcion listar usuarios del controller
            dgv.insert("", tk.END, values=(r.id_remito, r.fecha_remito, r.id_proveedor, r.nombre_proveedor))

    def buscarID():
        mini = tk.Toplevel()
        mini.title("Buscar ID")

        tk.Label(mini, text="ID Remito").pack()
        entry_id = tk.Entry(mini) 
        entry_id.pack() 

        def guardarID():
            try:
                idrem = int(entry_id.get().strip())
                dgv.delete(*dgv.get_children())
                remito = Buscar_remito_por_id(idrem)

                if remito:
                    dgv.insert("", tk.END, values=(
                        remito.id_remito,
                        remito.fecha_remito,
                        remito.id_proveedor,
                        remito.nombre_proveedor
                    ))
                else:
                    messagebox.showinfo("Buscar", f"No existe un remito con ID {idrem}")

            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        tk.Button(mini, text="Buscar", command=guardarID).pack(pady=10)


    def modificar_prov():
        datos = get_sel()
        if not datos:
            messagebox.showerror("Error", "Seleccione un proveedor")
            return

        mini = tk.Toplevel(Wrem)
        mini.title("Modificar Proveedor")

        tk.Label(mini, text="Id Proveedor").pack()
        entry_id_prov = tk.Entry(mini); entry_id_prov.insert(0, datos[2]); entry_id_prov.pack()

        def guardar():
            try:
                modificar_proveedor(
                    int(datos[0]),                         # id_remito
                    int(entry_id_prov.get())               # id_proveedor
                )
                cargar_todos()  # refrescar la tabla
                mini.destroy()
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(mini, text="Guardar", command=guardar).pack(pady=10)

    def ver_detalles():
        selected = dgv.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un remito")
            return

        try:
            datos = dgv.item(selected[0], "values")
            id_remito = int(datos[0])
        except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")
                return

        detalles = listar_detalles_por_remito(id_remito)
        if not detalles:
            messagebox.showinfo("Sin datos", f"No hay detalles para el remito {id_remito}")
            return
        
        # Generar PDF
        nombre_archivo = f"remito_{id_remito}.pdf"
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"Detalle Remito #{id_remito}", styles["Title"]))
        elements.append(Spacer(1, 12))

        data = [["ID Remito","ID Material","Nombre Material", "Cantidad"]]
        for rd in detalles:
            data.append([rd.id_remito, rd.id_material, rd.nombre_material, rd.cantidad])

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
            ("TEXTCOLOR", (0,0), (-1,0), colors.black),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ALIGN", (0,0), (-1,-1), "CENTER")
        ]))

        elements.append(tabla)
        doc.build(elements)

        messagebox.showinfo("PDF generado", f"Se creó el archivo {os.path.abspath(nombre_archivo)}")

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un usuario")
            return None
        return dgv.item(sel)["values"]

    # Frame de los botones
    frame_btns = tk.Frame(Wrem, bg="#004643")
    frame_btns.pack(pady=10)

    # Botones de acciones
    tk.Button(frame_btns, text="Ver Todos", command=cargar_todos).grid(row=0, column=0, padx=5)
    tk.Button(frame_btns, text="Busqueda por ID", command=buscarID).grid(row=0, column=1, padx=5)
    tk.Button(frame_btns, text="Modificar Proveedor", command=modificar_prov).grid(row=0, column=2, padx=5)
    tk.Button(frame_btns, text="Ver Detalles", command=ver_detalles).grid(row=0, column=4, padx=50)

    cargar_todos()