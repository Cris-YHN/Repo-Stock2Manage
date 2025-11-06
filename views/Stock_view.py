import customtkinter as ctk
from tkinter import ttk, messagebox, Listbox
from assets.Themes import themes
from controllers.LogsController import registrar 
from controllers.MaterialControllers import (
    listar_materiales, listar_materiales_activos, listar_materiales_inactivos, listar_materiales_escasos,
    buscar_nombre, crear_material, modificar_material,
    baja_material, alta_material, Carga_Materiales_delRemito, verificar_material_proveedor
)
from controllers.RemitosControllers import crear_remito
from controllers.ProveedorControllers import listar_proveedores
from entities.RemitosEntity import RemitoDetalle
import datetime

# Funcion de gestion Stock
def gestion_stock(contenedor, usuario):
    colors = themes.get_colors()
    
    # limpiar contenedor
    for w in contenedor.winfo_children():
        w.destroy()

    # marco principal
    main = ctk.CTkFrame(contenedor, fg_color=colors["BG"])
    main.pack(fill="both", expand=True)

    # Combo filtro
    filtro = ctk.CTkComboBox(
        main,
        values=["Todos los Materiales","Materiales Activos", "Materiales Inactivos", "Materiales Escasos"],
        width=250
    )
    filtro.set("Todos los Materiales")
    filtro.pack(pady=10)

    # Creacion de frame del Treeview dentro del contenedor
    frame_tree = ctk.CTkFrame(main, fg_color=colors["FRAME"])
    frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

    # Barras de Scroll para Treeview
    scrollbar_y = ctk.CTkScrollbar(frame_tree, orientation="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # Treeview
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
    columnas = ("ID","Nombre","Stock","ID Proveedor","Proveedor","Max Ingreso","Estado")
    dgv = ttk.Treeview(frame_tree, columns=columnas, show="headings", yscrollcommand=scrollbar_y.set)

    for col in columnas:
        # Ocultamos visualmente las columnas ID e ID Proveedor
        if col in ("ID", "ID Proveedor"):
            dgv.heading(col, text="")  # Sin título visible
            dgv.column(col, anchor="center", width=0, stretch=False)  # Ancho cero
        else:
            dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
            dgv.column(col, anchor="center", width=150)

    dgv.pack(fill="both", expand=True, padx=2, pady=2)

    scrollbar_y.configure(command=dgv.yview)

    # Diccionario de estados
    ESTADOS = {
        0: "Inactivo",
        1: "Activo"
    }

    # Funcion de cargar todos los datos dentro del Treeview
    def cargar_datos():
        dgv.delete(*dgv.get_children())
        sel = filtro.get()
        if sel == "Todos los Materiales":
            datos = listar_materiales()
        elif sel == "Materiales Activos":
            datos = listar_materiales_activos()
        elif sel == "Materiales Inactivos":
            datos = listar_materiales_inactivos()
        else:
            datos = listar_materiales_escasos()
        for m in datos:
            dgv.insert("", "end", values=(
                m.id_material, m.nombre, m.stock_disponible,
                m.id_proveedor, m.nombre_proveedor,
                m.max_ingreso, ESTADOS.get(m.activo, "Desconocido")
            ))

    # Funcion de seleccionar registro
    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención","Selecciona un usuario")
            return None
        return dgv.item(sel)["values"]
    
    # ***Funciones Internas***
    # Funcion de Buscar Material por Nombre
    def buscar_nombre_view():
        mini = ctk.CTkToplevel(main)
        mini.title("Buscar por Nombre")
        mini.geometry("300x150")
        mini.transient(main); mini.grab_set()

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre de Material:").pack(pady=5)
        entry_id = ctk.CTkEntry(frame_center); entry_id.pack(pady=5)

        def buscar():
            try:
                namemat = entry_id.get()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return
            dgv.delete(*dgv.get_children())
            resultados = buscar_nombre(namemat)
            if resultados:
                for m in resultados:
                    dgv.insert("", "end", values=(
                        m.id_material, m.nombre, m.stock_disponible,
                        m.id_proveedor, m.nombre_proveedor,
                        m.max_ingreso, ESTADOS.get(m.activo, "Desconocido")
                    ))
            else:
                messagebox.showinfo("Resultado", f"No existe material {namemat}")
            mini.destroy()

        ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=buscar).pack(pady=10)
    
    # Funcion de agregar material al Stock
    def agregar_mat():
        mini = ctk.CTkToplevel(main)
        mini.title("Nuevo Material"); mini.transient(main); mini.grab_set()
        mini.geometry("350x300")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre").pack(pady=5)
        e_nom = ctk.CTkEntry(frame_center); e_nom.pack(pady=5)
        ctk.CTkLabel(frame_center, text="ID Proveedor").pack(pady=10)
        e_prov = ctk.CTkEntry(frame_center); e_prov.pack(pady=5)

        def guardar():
            try:
                nombre = e_nom.get().strip()
                prov   = int(e_prov.get().strip())
            except Exception as e:
                messagebox.showerror("Error", str(e)); return
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
            if not any(p.id_proveedor == prov for p in listar_proveedores()):
                messagebox.showerror("Error", "Proveedor inexistente"); return
            crear_material(nombre, prov)
            registrar(usuario, "Material agregado correctamente.", "STOCK")
            cargar_datos(); mini.destroy()
        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=10)
    
    # Funcion de modificar datos de un material del stock
    def modificar_mat():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main)
        mini.title("Modificar Material"); mini.transient(main); mini.grab_set()
        mini.geometry("400x350")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre").pack(pady=5)
        e_nom = ctk.CTkEntry(frame_center); e_nom.insert(0, datos[1]); e_nom.pack(pady=5)
        ctk.CTkLabel(frame_center, text="Stock").pack(pady=10)
        e_stock = ctk.CTkEntry(frame_center); e_stock.insert(0, datos[2]); e_stock.pack(pady=5)
        ctk.CTkLabel(frame_center, text="ID Proveedor").pack(pady=10)
        e_prov = ctk.CTkEntry(frame_center); e_prov.insert(0, datos[3]); e_prov.pack(pady=5)

        def guardar():
            try:
                modificar_material(int(datos[0]), e_nom.get(),
                                   int(e_stock.get()), int(e_prov.get()))
                registrar(usuario, "Material modificado correctamente.", "STOCK")
                cargar_datos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")
        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=20)
    
    # Funcion para dar de baja algun material
    def baja_mat():
        datos = get_sel()
        if datos and messagebox.askyesno("Confirmación","¿Dar de baja?"):
            baja_material(int(datos[0])); cargar_datos()
            registrar(usuario, "Material fue dado de baja.", "STOCK")

    # Funcion para dar de alta algun material que fue dado de baja
    def alta_mat():
        datos = get_sel()
        if datos and messagebox.askyesno("Confirmación","¿Dar de alta?"):
            alta_material(int(datos[0])); cargar_datos()
            registrar(usuario, "Material fue dado de alta.", "STOCK")

    # Funcion para el armado de Remitos
    def cargar_remito_view():
        mini = ctk.CTkToplevel(main)
        mini.title("Cargar Remito"); mini.transient(main); mini.grab_set()
        mini.geometry("500x500")
        materiales = []
        proveedor_valido = {"id": None, "ok": False}

        frame_prov = ctk.CTkFrame(mini, fg_color="transparent")
        frame_prov.pack(pady=10)

        ctk.CTkLabel(frame_prov, text="ID Proveedor").grid(row=0, column=0, padx=5, pady=5)
        e_prov = ctk.CTkEntry(frame_prov, width=150)
        e_prov.grid(row=0, column=1, padx=5, pady=5)

        import tkinter as tk
        listbox_sug = tk.Listbox(
        frame_prov,
        height=4,
        width=45,
        bg=colors["FRAME"],
        fg=colors["TEXT"],
        highlightbackground=colors["TOP"],
        highlightcolor=colors["TOP"],
        selectbackground=colors["TOP"],
        selectforeground=colors["BUTTON_TXT"],
        relief="flat",
        borderwidth=2,
        font=("Arial", 13)
        )
        listbox_sug.grid(row=1, column=1, padx=5, pady=2)

        def actualizar_sugerencias(event=None):
            texto = e_prov.get().lower()
            listbox_sug.delete(0, "end")
            proveedor_valido["ok"] = False

            if not texto:
                return

            proveedores = listar_proveedores()
            for prov in proveedores:
                if texto in prov.nombre_proveedor.lower():
                    listbox_sug.insert("end", f"{prov.nombre_proveedor} | ID:{prov.id_proveedor}")

        def seleccionar_proveedor(event=None):
            if not listbox_sug.curselection():
                return

            sel = listbox_sug.get(listbox_sug.curselection())
            nombre, idp = sel.split("| ID:")

            # Setear nombre definitivo
            e_prov.delete(0, "end")
            e_prov.insert(0, nombre.strip())

            proveedor_valido["id"] = int(idp.strip())
            proveedor_valido["ok"] = True

            # Limpiar y ocultar las sugerencias
            listbox_sug.delete(0, "end")
            listbox_sug.grid_remove()

            # Bloquear entrada para que no se pueda modificar
            e_prov.configure(state="disabled")


        e_prov.bind("<KeyRelease>", actualizar_sugerencias)
        listbox_sug.bind("<<ListboxSelect>>", seleccionar_proveedor)

        frame_mats_container = ctk.CTkFrame(mini)
        frame_mats_container.pack(pady=10, fill="both", expand=True)

        canvas = ctk.CTkCanvas(
            frame_mats_container,
            bg=colors["BG"],
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar_mats = ctk.CTkScrollbar(
            frame_mats_container, orientation="vertical",
            command=canvas.yview
        )
        scrollbar_mats.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar_mats.set)

        # Contenido scrolleable
        frame_mats = ctk.CTkFrame(canvas, fg_color="transparent")
        frame_mats.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame_mats, anchor="nw")

        def cargar_materiales_del_proveedor():
            if not proveedor_valido["ok"]:
                messagebox.showwarning("Atención", "Seleccione un proveedor válido de la lista.")
                return
            
            idp = proveedor_valido["id"]

            for r in materiales:
                try:
                    r[1].master.destroy()
                except:
                    pass
            materiales.clear()

            mats = listar_materiales_activos()
            mats = [m for m in mats if m.id_proveedor == idp]

            if not mats:
                messagebox.showinfo("Sin materiales", "El proveedor no tiene materiales activos.")
                return

            for m in mats:
                row = ctk.CTkFrame(frame_mats, fg_color=colors["FRAME"], corner_radius=10)
                row.pack(pady=8, padx=50, fill="x")

                lbl = ctk.CTkLabel(row, text=m.nombre)
                lbl.grid(row=0, column=0, padx=10)

                e_qty = ctk.CTkEntry(row, width=90, placeholder_text="Cantidad")
                e_qty.grid(row=0, column=1, padx=10)
                
                materiales.append((m.id_material, e_qty))

        ctk.CTkButton(frame_prov, text="Cargar Materiales del Proveedor", fg_color=colors["BUTTON"],
                    command=cargar_materiales_del_proveedor).grid(row=0, column=2, padx=5, pady=5)

        def guardar():
            if not proveedor_valido["ok"]:
                messagebox.showerror("Error", "Debe seleccionar un proveedor válido.")
                return

            idp = proveedor_valido["id"]
            detalles = []

            try:
                for id_mat, e_qty in materiales:
                    cant = int(e_qty.get())
                    if cant <= 0:
                        raise ValueError
                    detalles.append(RemitoDetalle(id_material=id_mat, cantidad=cant))
                    Carga_Materiales_delRemito(id_mat, cant)

                crear_remito(datetime.date.today().strftime("%Y-%m-%d"), idp, detalles)
                registrar(usuario, "Remito creado con éxito.", "REMITO")
                cargar_datos()
                mini.destroy()

                messagebox.showinfo("Éxito", "Remito cargado correctamente.")
            except ValueError:
                messagebox.showerror("Error", "Ingrese cantidades válidas en todos los materiales.")

        ctk.CTkButton(mini, text="Guardar Remito", fg_color=colors["BUTTON"], command=guardar).pack(pady=10)
    
    # Frame de botones
    frame_botones = ctk.CTkFrame(main, fg_color=colors["FRAME"])
    frame_botones.pack(fill="x", pady=5)

    # Frame de centrar botones
    botones_center = ctk.CTkFrame(frame_botones, fg_color="transparent")
    botones_center.pack(anchor="center")

    # Botones
    ctk.CTkButton(botones_center, text="Buscar Nombre",   fg_color=colors["BUTTON"], command=buscar_nombre_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Agregar",    fg_color=colors["BUTTON"], command=agregar_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Modificar",  fg_color=colors["BUTTON"], command=modificar_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Baja",       fg_color=colors["BUTTON"], command=baja_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Alta",       fg_color=colors["BUTTON"], command=alta_mat).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(botones_center, text="Remito",     fg_color=colors["BUTTON"], command=cargar_remito_view).pack(side="left", padx=10, pady=10)

    # inicial
    filtro.configure(command=lambda _: cargar_datos())
    cargar_datos()