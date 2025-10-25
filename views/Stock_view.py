import customtkinter as ctk
from tkinter import ttk, messagebox
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
        dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
        dgv.column(col, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

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
        proveedor_valido = {"ok": False}

        frame_prov = ctk.CTkFrame(mini, fg_color="transparent")
        frame_prov.pack(pady=10)

        ctk.CTkLabel(frame_prov, text="ID Proveedor").grid(row=0, column=0, padx=5, pady=5)
        e_prov = ctk.CTkEntry(frame_prov, width=150)
        e_prov.grid(row=0, column=1, padx=5, pady=5)

        def verificar_proveedor():
            try:
                idp = int(e_prov.get().strip())
                proveedores = listar_proveedores()
                prov = next((p for p in proveedores if p.id_proveedor == idp), None)
                if prov:
                    messagebox.showinfo("Proveedor encontrado", f"✅ {prov.nombre_proveedor} (ID: {prov.id_proveedor})")
                    proveedor_valido["ok"] = True
                else:
                    messagebox.showerror("Error", "Proveedor inexistente")
                    proveedor_valido["ok"] = False
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número de proveedor válido")
                proveedor_valido["ok"] = False

        ctk.CTkButton(frame_prov, text="Verificar", fg_color=colors["BUTTON"],
                    text_color=colors["BUTTON_TXT"], width=100,
                    command=verificar_proveedor).grid(row=0, column=2, padx=5, pady=5)
        
        frame = ctk.CTkFrame(mini)
        frame.pack(pady=10)

        def add_row():
            # si ya hay filas, exigir que la última no esté vacía
            if materiales:
                e_id_last, e_qty_last = materiales[-1]
                if not e_id_last.get().strip() or not e_qty_last.get().strip():
                    messagebox.showwarning("Atención",
                                        "Complete el material anterior antes de agregar otro.")
                    return
            row = ctk.CTkFrame(frame, fg_color=colors["FRAME"], corner_radius=10)
            row.pack(pady=8, padx=15, fill="x")
            e_id = ctk.CTkEntry(row, width=100, placeholder_text="ID Material")
            e_id.grid(row=0, column=0, padx=10, pady=5)

            e_qty = ctk.CTkEntry(row, width=100, placeholder_text="Cantidad")
            e_qty.grid(row=0, column=1, padx=10, pady=5)
            ctk.CTkButton(row, text="❌", width=20, fg_color="#ff4d4d",
                          command=lambda r=row: (materiales.remove((e_id,e_qty)), r.destroy())
            ).grid(row=0, column=2, padx=5)
            materiales.append((e_id,e_qty))

        def guardar():
            try:
                idp = int(e_prov.get())
                if not proveedor_valido["ok"]:
                    messagebox.showerror("Error", "Debe verificar el proveedor antes de continuar.")
                    return
                detalles = []
                for e_id, e_qty in materiales:
                    id_mat = int(e_id.get())
                    cant = int(e_qty.get())
                    if not verificar_material_proveedor(id_mat, idp):
                        messagebox.showerror(
                            "Error de Proveedor",
                            f"El material con ID {id_mat} no pertenece al proveedor {idp}."
                        )
                        return
                    detalles.append(RemitoDetalle(id_material=id_mat, cantidad=cant))
                    Carga_Materiales_delRemito(id_mat, cant)
                crear_remito(datetime.date.today().strftime("%Y-%m-%d"), idp, detalles)
                messagebox.showinfo("Éxito","Remito cargado")
                registrar(usuario, "Remito creado con exito.", "REMITO")
                cargar_datos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        ctk.CTkButton(mini, text="Agregar Material", fg_color=colors["BUTTON"], command=add_row).pack(pady=5)
        ctk.CTkButton(mini, text="Guardar Remito", fg_color=colors["BUTTON"], command=guardar).pack(pady=5)
    
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