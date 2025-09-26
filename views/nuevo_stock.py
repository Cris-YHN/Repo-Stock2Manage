# views/nuevo_stock.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.MaterialControllers import (
    listar_materiales, listar_materiales_inactivos, listar_materiales_escasos,
    buscar_id, crear_material, modificar_material,
    baja_material, alta_material, Carga_Materiales_delRemito
)
from controllers.RemitosControllers import crear_remito
from controllers.ProveedorControllers import listar_proveedores
from entities.RemitosEntity import RemitoDetalle
import datetime

COLOR_BG    = "#16161a"
COLOR_TOP   = "#2cb67d"
COLOR_FRAME = "#242629"
COLOR_BTN   = "#7f5af0"

def gestion_stock(parent_frame):
    # limpiar
    for w in parent_frame.winfo_children():
        w.destroy()

    # marco principal
    main = ctk.CTkFrame(parent_frame, fg_color=COLOR_BG)
    main.pack(fill="both", expand=True)

    # ---- Combo filtro
    filtro = ctk.CTkComboBox(
        main,
        values=["Materiales Activos", "Materiales Inactivos", "Materiales Escasos"],
        width=250
    )
    filtro.set("Materiales Activos")
    filtro.pack(pady=10)

    # ---- Treeview oscuro
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

    columnas = ("ID","Nombre","Stock","ID Proveedor","Proveedor","Max Ingreso","Activo")
    dgv = ttk.Treeview(frame_tree, columns=columnas, show="headings")
    for c in columnas:
        dgv.heading(c, text=c)
        dgv.column(c, anchor="center", width=120)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    # ---- Funciones de datos
    def cargar_datos():
        dgv.delete(*dgv.get_children())
        sel = filtro.get()
        if sel == "Materiales Activos":
            datos = listar_materiales()
        elif sel == "Materiales Inactivos":
            datos = listar_materiales_inactivos()
        else:
            datos = listar_materiales_escasos()
        for m in datos:
            dgv.insert("", "end", values=(
                m.id_material, m.nombre, m.stock_disponible,
                m.id_proveedor, m.nombre_proveedor,
                m.max_ingreso, m.activo
            ))

    # ---- CRUD Helpers
    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un material")
            return None
        return dgv.item(sel)["values"]

    def buscar_id_view():
        mini = ctk.CTkToplevel(main)
        mini.title("Buscar por ID")
        mini.geometry("300x150")
        mini.transient(main); mini.grab_set()

        ctk.CTkLabel(mini, text="ID Material:").pack(pady=5)
        entry_id = ctk.CTkEntry(mini); entry_id.pack(pady=5)

        def buscar():
            try:
                mid = int(entry_id.get())
            except ValueError:
                messagebox.showerror("Error", "Debe ser número")
                return
            dgv.delete(*dgv.get_children())
            m = buscar_id(mid)
            if m:
                dgv.insert("", "end", values=(
                    m.id_material, m.nombre, m.stock_disponible,
                    m.id_proveedor, m.nombre_proveedor,
                    m.max_ingreso, m.activo
                ))
            else:
                messagebox.showinfo("Resultado", f"No existe material con ID {mid}")
            mini.destroy()

        ctk.CTkButton(mini, text="Buscar", fg_color=COLOR_BTN, command=buscar).pack(pady=10)

    def agregar_mat():
        mini = ctk.CTkToplevel(main)
        mini.title("Nuevo Material"); mini.transient(main); mini.grab_set()

        ctk.CTkLabel(mini, text="Nombre").pack(pady=5)
        e_nom = ctk.CTkEntry(mini); e_nom.pack(pady=5)
        ctk.CTkLabel(mini, text="ID Proveedor").pack(pady=5)
        e_prov = ctk.CTkEntry(mini); e_prov.pack(pady=5)

        def guardar():
            try:
                nombre = e_nom.get().strip()
                prov   = int(e_prov.get().strip())
            except:
                messagebox.showerror("Error", "Datos inválidos"); return
            if not any(p.id_proveedor == prov for p in listar_proveedores()):
                messagebox.showerror("Error", "Proveedor inexistente"); return
            crear_material(nombre, prov)
            cargar_datos(); mini.destroy()
        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    def modificar_mat():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main)
        mini.title("Modificar Material"); mini.transient(main); mini.grab_set()

        ctk.CTkLabel(mini, text="Nombre").pack(pady=5)
        e_nom = ctk.CTkEntry(mini); e_nom.insert(0, datos[1]); e_nom.pack(pady=5)
        ctk.CTkLabel(mini, text="Stock").pack(pady=5)
        e_stock = ctk.CTkEntry(mini); e_stock.insert(0, datos[2]); e_stock.pack(pady=5)
        ctk.CTkLabel(mini, text="ID Proveedor").pack(pady=5)
        e_prov = ctk.CTkEntry(mini); e_prov.insert(0, datos[3]); e_prov.pack(pady=5)

        def guardar():
            try:
                modificar_material(int(datos[0]), e_nom.get(),
                                   int(e_stock.get()), int(e_prov.get()))
                cargar_datos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    def baja_mat():
        datos = get_sel()
        if datos and messagebox.askyesno("Confirmación","¿Dar de baja?"):
            baja_material(int(datos[0])); cargar_datos()

    def alta_mat():
        datos = get_sel()
        if datos and messagebox.askyesno("Confirmación","¿Dar de alta?"):
            alta_material(int(datos[0])); cargar_datos()

    def cargar_remito_view():
        mini = ctk.CTkToplevel(main)
        mini.title("Cargar Remito"); mini.transient(main); mini.grab_set()
        materiales = []

        ctk.CTkLabel(mini, text="Proveedor").pack(pady=5)
        e_prov = ctk.CTkEntry(mini); e_prov.pack(pady=5)
        frame = ctk.CTkFrame(mini); frame.pack(pady=10)

        def add_row():
            row = ctk.CTkFrame(frame); row.pack(pady=5)
            e_id = ctk.CTkEntry(row, width=60); e_id.grid(row=0, column=0, padx=5)
            e_qty= ctk.CTkEntry(row, width=60); e_qty.grid(row=0, column=1, padx=5)
            ctk.CTkButton(row, text="❌", width=20,
                          command=lambda r=row: (materiales.remove((e_id,e_qty)), r.destroy())
            ).grid(row=0, column=2, padx=5)
            materiales.append((e_id,e_qty))

        def guardar():
            try:
                idp = int(e_prov.get())
                if not any(p.id_proveedor == idp for p in listar_proveedores()):
                    messagebox.showerror("Error", "Proveedor inexistente"); return
                detalles = []
                for e_id,e_qty in materiales:
                    detalles.append(RemitoDetalle(
                        id_material=int(e_id.get()),
                        cantidad=int(e_qty.get())
                    ))
                    Carga_Materiales_delRemito(int(e_id.get()), int(e_qty.get()))
                crear_remito(datetime.date.today().strftime("%Y-%m-%d"), idp, detalles)
                messagebox.showinfo("Éxito","Remito cargado")
                cargar_datos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(mini, text="Agregar Material", command=add_row).pack(pady=5)
        ctk.CTkButton(mini, text="Guardar Remito", command=guardar).pack(pady=5)

    # ---- Barra de botones
    frame_botones = ctk.CTkFrame(main, fg_color=COLOR_FRAME)
    frame_botones.pack(fill="x", pady=5)

    ctk.CTkButton(frame_botones, text="Buscar ID",   fg_color=COLOR_BTN, command=buscar_id_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="Agregar",    fg_color=COLOR_BTN, command=agregar_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="Modificar",  fg_color=COLOR_BTN, command=modificar_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="Baja",       fg_color=COLOR_BTN, command=baja_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="Alta",       fg_color=COLOR_BTN, command=alta_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="Remito",     fg_color=COLOR_BTN, command=cargar_remito_view).pack(side="left", padx=10, pady=10)

    # inicial
    filtro.configure(command=lambda _: cargar_datos())
    cargar_datos()
