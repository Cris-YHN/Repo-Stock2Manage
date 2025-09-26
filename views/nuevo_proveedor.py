import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.CPControllers import Buscar_proveedor_por_nombre, listar_cp
from controllers.ProveedorControllers import (
    listar_proveedores, Buscar_proveedor_por_id,
    crear_proveedor, modificar_proveedor
)

COLOR_BG = "#16161a"
COLOR_FRAME = "#242629"
COLOR_TOP = "#2cb67d"
COLOR_BTN = "#7f5af0"

def gestion_proveedores(parent_frame):
    for w in parent_frame.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(parent_frame, fg_color=COLOR_BG)
    main.pack(fill="both", expand=True)

    # Treeview
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

    cols = ("ID","Nombre","Codigo Postal","Localidad","Provincia","Calle","Numero","Telefono")
    dgv = ttk.Treeview(frame_tree, columns=cols, show="headings")
    for c in cols:
        dgv.heading(c, text=c)
        dgv.column(c, anchor="center", width=120)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

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
        ctk.CTkLabel(mini, text="ID Proveedor").pack(pady=5)
        e = ctk.CTkEntry(mini); e.pack(pady=5)

        def go():
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
        ctk.CTkButton(mini, text="Buscar", fg_color=COLOR_BTN, command=go).pack(pady=10)

    def agregar_prov():
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Nuevo Proveedor")
        entries = {}
        for campo in ["Nombre","Codigo Postal","Calle","Numero","Telefono"]:
            ctk.CTkLabel(mini, text=campo).pack()
            e = ctk.CTkEntry(mini); e.pack(pady=2)
            entries[campo] = e
        def guardar():
            try:
                crear_proveedor(entries["Nombre"].get(), entries["Codigo Postal"].get(),
                                entries["Calle"].get(), entries["Numero"].get(),
                                entries["Telefono"].get())
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    def modificar_prov_view():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Modificar Proveedor")
        labels = ["Nombre","Codigo Postal","Calle","Numero","Telefono"]
        defaults = [datos[1], datos[2], datos[5], datos[6], datos[7]]
        entries = {}
        for lab,val in zip(labels, defaults):
            ctk.CTkLabel(mini, text=lab).pack()
            e = ctk.CTkEntry(mini); e.insert(0, val); e.pack()
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
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    def ver_cp():
        mini = ctk.CTkToplevel(main)
        mini.transient(main)
        mini.grab_set()
        mini.title("Códigos Postales")
        mini.geometry("800x500")

        # Frame contenedor del Treeview y Scrollbars
        frame_tabla = ctk.CTkFrame(mini)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

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

        scrollbar_y.config(command=dmini.yview)
        scrollbar_x.config(command=dmini.xview)

        def cargar_all():
            dmini.delete(*dmini.get_children())
            for cp in listar_cp():
                dmini.insert("", "end",
                            values=(cp.codigo_postal, cp.ciudad, cp.provincia, cp.pais))

        def buscar_ciudad():
            win = ctk.CTkToplevel(mini)
            win.title("Buscar Ciudad")
            ctk.CTkLabel(win, text="Ciudad:").pack(pady=5)
            entry = ctk.CTkEntry(win)
            entry.pack(pady=5)

            def go():
                dmini.delete(*dmini.get_children())
                for cp in Buscar_proveedor_por_nombre(entry.get()):
                    dmini.insert("", "end",
                                values=(cp.codigo_postal, cp.ciudad, cp.provincia, cp.pais))
                win.destroy()

            ctk.CTkButton(win, text="Buscar", fg_color=COLOR_BTN, command=go).pack(pady=10)

        # Barra inferior con botones
        fb = ctk.CTkFrame(mini, fg_color=COLOR_FRAME)
        fb.pack(fill="x", pady=5)
        ctk.CTkButton(fb, text="Ver Todos", fg_color=COLOR_BTN, command=cargar_all).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(fb, text="Buscar Ciudad", fg_color=COLOR_BTN, command=buscar_ciudad).pack(side="left", padx=10, pady=10)

        cargar_all()



    # barra
    fb = ctk.CTkFrame(main, fg_color=COLOR_FRAME)
    fb.pack(fill="x", pady=5)
    ctk.CTkButton(fb, text="Ver Todos", fg_color=COLOR_BTN, command=cargar_todos).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Buscar ID", fg_color=COLOR_BTN, command=buscarID).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Agregar", fg_color=COLOR_BTN, command=agregar_prov).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Modificar", fg_color=COLOR_BTN, command=modificar_prov_view).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Ver Códigos Postales", fg_color=COLOR_BTN, command=ver_cp).pack(side="left", padx=10, pady=10)

    cargar_todos()
