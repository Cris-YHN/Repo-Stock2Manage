import customtkinter as ctk
from tkinter import ttk, messagebox
from assets.Themes import themes
from controllers.LogsController import registrar
from controllers.CPControllers import Buscar_proveedor_por_nombre, listar_cp
from controllers.ProveedorControllers import (
    listar_proveedores, Buscar_proveedor_por_id,
    crear_proveedor, modificar_proveedor
)

def gestion_proveedores(parent_frame, usuario):
    colors = themes.get_colors()

    for w in parent_frame.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(parent_frame, fg_color=colors["BG"])
    main.pack(fill="both", expand=True)

    frame_tree = ctk.CTkFrame(main, fg_color=colors["FRAME"])
    frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

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

    cols = ("ID","Nombre","Codigo Postal","Localidad","Provincia","Calle","Numero","Telefono")
    dgv = ttk.Treeview(frame_tree, columns=cols, show="headings", yscrollcommand=scrollbar_y.set)
    for col in cols:
        dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
        dgv.column(col, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    scrollbar_y.configure(command=dgv.yview)

    def cargar_todos():
        dgv.delete(*dgv.get_children())
        for p in listar_proveedores():
            dgv.insert("", "end", values=(
                p.id_proveedor, p.nombre_proveedor, p.codigo_postal,
                p.localidad, p.provincia, p.calle, p.numero, p.telefono
            ))

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un proveedor")
            return None
        return dgv.item(sel)["values"]

    def buscarID():
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Buscar ID")
        mini.geometry("300x200")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="ID Proveedor").pack(pady=5)
        e = ctk.CTkEntry(frame_center); e.pack(pady=5)

        def buscar():
            try:
                pid = int(e.get())
                dgv.delete(*dgv.get_children())
                for p in Buscar_proveedor_por_id(pid):
                    dgv.insert("", "end", values=(
                        p.id_proveedor, p.nombre_proveedor, p.codigo_postal,
                        p.localidad, p.provincia, p.calle, p.numero, p.telefono
                    ))
                mini.destroy()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))
        ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=buscar).pack(pady=10)

    def agregar_prov():
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Nuevo Proveedor")
        mini.geometry("300x400")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        entries = {}
        for campo in ["Nombre","Codigo Postal","Calle","Numero","Telefono"]:
            ctk.CTkLabel(frame_center, text=campo).pack()
            e = ctk.CTkEntry(frame_center); e.pack(pady=2)
            entries[campo] = e
        def guardar():
            try:
                crear_proveedor(entries["Nombre"].get(), entries["Codigo Postal"].get(),
                                entries["Calle"].get(), entries["Numero"].get(),
                                entries["Telefono"].get())
                registrar(usuario, "Nuevo Proveedor creado con exito.", "PROVEEDOR")
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=10)

    def modificar_prov_view():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Modificar Proveedor")
        mini.geometry("350x450")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        labels = ["Nombre","Codigo Postal","Calle","Numero","Telefono"]
        defaults = [datos[1], datos[2], datos[5], datos[6], datos[7]]
        entries = {}
        for lab,val in zip(labels, defaults):
            ctk.CTkLabel(frame_center, text=lab).pack(pady=10)
            e = ctk.CTkEntry(frame_center); e.insert(0, val); e.pack()
            entries[lab] = e
        def guardar():
            try:
                modificar_proveedor(int(datos[0]),
                    entries["Nombre"].get(),
                    entries["Codigo Postal"].get(),
                    entries["Calle"].get(),
                    entries["Numero"].get(),
                    entries["Telefono"].get()
                )
                registrar(usuario, "Modificacion de proveedor.", "PROVEEDOR")
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=15)

    def ver_cp():
        mini = ctk.CTkToplevel(main)
        mini.transient(main)
        mini.grab_set()
        mini.title("Códigos Postales")
        mini.geometry("800x500")

        # Frame contenedor del Treeview y Scrollbars
        frame_tabla = ctk.CTkFrame(mini)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=(10,0))

        # Scrollbars
        scrollbar_y = ctk.CTkScrollbar(frame_tabla, orientation="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ctk.CTkScrollbar(frame_tabla, orientation="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        # Treeview
        cols = ("Codigo", "Ciudad", "Provincia", "Pais")
        dmini = ttk.Treeview(
            frame_tabla,
            columns=cols,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        for c in cols:
            dmini.heading(c, text=c)
            dmini.column(c, width=150, anchor="center")

        dmini.pack(fill="both", expand=True)

        scrollbar_y.configure(command=dmini.yview)
        scrollbar_x.configure(command=dmini.xview)

        def cargar_all():
            dmini.delete(*dmini.get_children())
            for cp in listar_cp():
                dmini.insert("", "end",
                            values=(cp.codigo_postal, cp.ciudad, cp.provincia, cp.pais))

        def buscar_ciudad():
            win = ctk.CTkToplevel(mini); win.transient(mini); win.grab_set()
            win.title("Buscar Ciudad")
            win.geometry("300x200")

            frame_center = ctk.CTkFrame(win, fg_color="transparent")
            frame_center.pack(expand=True)

            ctk.CTkLabel(frame_center, text="Ciudad:").pack(pady=5)
            entry = ctk.CTkEntry(frame_center)
            entry.pack(pady=5)

            def buscar():
                dmini.delete(*dmini.get_children())
                for cp in Buscar_proveedor_por_nombre(entry.get()):
                    dmini.insert("", "end",
                                values=(cp.codigo_postal, cp.ciudad, cp.provincia, cp.pais))
                win.destroy()

            ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=buscar).pack(pady=10)

        # Barra inferior con botones
        fb = ctk.CTkFrame(mini, fg_color=colors["FRAME"])
        fb.pack(fill="x", pady=5)
        ctk.CTkButton(fb, text="Ver Todos", fg_color=colors["BUTTON"], command=cargar_all).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(fb, text="Buscar Ciudad", fg_color=colors["BUTTON"], command=buscar_ciudad).pack(side="left", padx=10, pady=10)

        cargar_all()



    # barra
    fb = ctk.CTkFrame(main, fg_color=colors["FRAME"])
    fb.pack(fill="x", pady=5)
    ctk.CTkButton(fb, text="Ver Todos", fg_color=colors["BUTTON"], command=cargar_todos).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Buscar ID", fg_color=colors["BUTTON"], command=buscarID).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Agregar", fg_color=colors["BUTTON"], command=agregar_prov).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Modificar", fg_color=colors["BUTTON"], command=modificar_prov_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Ver Códigos Postales", fg_color=colors["BUTTON"], command=ver_cp).pack(side="left", padx=10, pady=10)

    cargar_todos()
