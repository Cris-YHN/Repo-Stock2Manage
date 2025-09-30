# views/Crear_manufactura_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.ManufacturaControllers import (
    listar_manufactura, Buscar_manufactura_por_nombre,
    crear_manufactura, modificar_manufactura,
    listar_pasos, crear_paso, modificar_paso
)
from controllers.MaterialControllers import listar_materiales
from entities.ManufacturaEntity import PasoDetalle   # asumiendo que existe

COLOR_BG    = "#16161a"
COLOR_TOP   = "#2cb67d"
COLOR_FRAME = "#242629"
COLOR_BTN   = "#7f5af0"

def gestion_crear_manufactura(parent_frame):
    for w in parent_frame.winfo_children():
        w.destroy()

    main = ctk.CTkFrame(parent_frame, fg_color=COLOR_BG)
    main.pack(fill="both", expand=True)

    # ---- estilo del Treeview oscuro ----
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

    # ---- tabla principal de manufacturas ----
    frame_tree = ctk.CTkFrame(main, fg_color=COLOR_FRAME)
    frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

    columnas = ("ID", "Nombre")
    dgv = ttk.Treeview(frame_tree, columns=columnas, show="headings")
    for c in columnas:
        dgv.heading(c, text=c)
        dgv.column(c, anchor="center", width=250)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    # ---- funciones internas ----
    def cargar_manufacturas():
        dgv.delete(*dgv.get_children())
        for m in listar_manufactura():
            dgv.insert("", "end", values=(m.id_manufactura, m.nombre))

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una Manufactura")
            return None
        return dgv.item(sel)["values"]

    # ------------------- BOTONES ---------------------
    frame_btn = ctk.CTkFrame(main, fg_color=COLOR_FRAME)
    frame_btn.pack(fill="x", pady=5)

    # Botones principales
    btn_buscar = ctk.CTkButton(frame_btn, text="Buscar por Nombre", fg_color=COLOR_BTN)
    btn_agregar = ctk.CTkButton(frame_btn, text="Agregar Manufactura", fg_color=COLOR_BTN)
    btn_modificar = ctk.CTkButton(frame_btn, text="Modificar Manufactura", fg_color=COLOR_BTN)
    btn_ver_pasos = ctk.CTkButton(frame_btn, text="Ver Pasos", fg_color=COLOR_BTN)

    # Botones para modo pasos
    btn_volver = ctk.CTkButton(frame_btn, text="Volver a Manufacturas", fg_color=COLOR_BTN)
    btn_agregar_paso = ctk.CTkButton(frame_btn, text="Agregar Paso", fg_color=COLOR_BTN)
    btn_modificar_paso = ctk.CTkButton(frame_btn, text="Modificar Paso", fg_color=COLOR_BTN)

    for b in (btn_buscar, btn_agregar, btn_modificar, btn_ver_pasos):
        b.pack(side="left", padx=10, pady=10)

    # ---- comportamiento de botones ----
    def buscar_por_nombre():
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Buscar Manufactura")
        ctk.CTkLabel(mini, text="Nombre:").pack(pady=5)
        entry_nom = ctk.CTkEntry(mini); entry_nom.pack(pady=5)

        def buscar():
            nombre = entry_nom.get().strip()
            if not nombre:
                return
            dgv.delete(*dgv.get_children())
            mf = Buscar_manufactura_por_nombre(nombre)
            if mf:
                for m in mf:
                    dgv.insert("", "end", values=(m.id_manufactura, m.nombre))
            else:
                messagebox.showinfo("Buscar", f"No existe manufactura con nombre {nombre}")
            mini.destroy()

        ctk.CTkButton(mini, text="Buscar", fg_color=COLOR_BTN, command=buscar).pack(pady=10)

    btn_buscar.configure(command=buscar_por_nombre)

    def agregar_manufactura():
        mini = ctk.CTkToplevel(main); mini.title("Nueva Manufactura")
        ctk.CTkLabel(mini, text="Nombre:").pack(pady=5)
        e_nom = ctk.CTkEntry(mini); e_nom.pack(pady=5)

        def guardar():
            nom = e_nom.get().strip()
            if not nom:
                messagebox.showerror("Error", "Nombre requerido")
                return
            crear_manufactura(nom)
            cargar_manufacturas()
            mini.destroy()
        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    btn_agregar.configure(command=agregar_manufactura)

    def modificar_manuf():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main); mini.title("Modificar Manufactura")
        ctk.CTkLabel(mini, text="Nombre:").pack(pady=5)
        e_nom = ctk.CTkEntry(mini); e_nom.insert(0, datos[1]); e_nom.pack(pady=5)

        def guardar():
            nom = e_nom.get().strip()
            modificar_manufactura(int(datos[0]), nom)
            cargar_manufacturas()
            mini.destroy()
        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    btn_modificar.configure(command=modificar_manuf)

    # ----- modo PASOS -----
    def ver_pasos():
        datos = get_sel()
        if not datos: return
        id_manu = datos[0]

        # limpiar tabla y cambiar columnas a Pasos
        dgv.delete(*dgv.get_children())
        dgv["columns"] = ("ID Paso","Orden","Nombre Paso")
        for c in ("ID Paso","Orden","Nombre Paso"):
            dgv.heading(c, text=c); dgv.column(c, anchor="center", width=180)

        for p in listar_pasos(id_manu):
            dgv.insert("", "end", values=(p.id_paso, p.orden, p.nombre_paso))

        # cambiar botones visibles
        for b in (btn_buscar, btn_agregar, btn_modificar, btn_ver_pasos):
            b.pack_forget()
        for b in (btn_volver, btn_agregar_paso, btn_modificar_paso):
            b.pack(side="left", padx=10, pady=10)

        # ---------- acciones dentro de pasos ----------
        def volver():
            # restaurar columnas
            dgv.delete(*dgv.get_children())
            dgv["columns"] = ("ID","Nombre")
            for c in ("ID","Nombre"):
                dgv.heading(c, text=c); dgv.column(c, anchor="center", width=250)
            cargar_manufacturas()
            for b in (btn_volver, btn_agregar_paso, btn_modificar_paso):
                b.pack_forget()
            for b in (btn_buscar, btn_agregar, btn_modificar, btn_ver_pasos):
                b.pack(side="left", padx=10, pady=10)

        def agregar_paso():
            mini = ctk.CTkToplevel(main); mini.title("Agregar Paso")
            ctk.CTkLabel(mini, text="Orden:").pack(pady=5)
            e_orden = ctk.CTkEntry(mini); e_orden.pack(pady=5)
            ctk.CTkLabel(mini, text="Nombre Paso:").pack(pady=5)
            e_nom = ctk.CTkEntry(mini); e_nom.pack(pady=5)

            materiales = []
            frame = ctk.CTkFrame(mini); frame.pack(pady=5)

            def add_row():
                row = ctk.CTkFrame(frame); row.pack(pady=2)
                e_id = ctk.CTkEntry(row, width=60); e_id.grid(row=0, column=0, padx=3)
                e_qty= ctk.CTkEntry(row, width=60); e_qty.grid(row=0, column=1, padx=3)
                ctk.CTkButton(row, text="❌", width=20,
                              command=lambda r=row: (materiales.remove((e_id,e_qty)), r.destroy())
                              ).grid(row=0, column=2, padx=3)
                materiales.append((e_id,e_qty))

            def guardar_paso():
                try:
                    paso_id = crear_paso(int(e_orden.get()), e_nom.get(), id_manu)
                    for e_id,e_qty in materiales:
                        # Guardar materiales por paso
                        # se asume create_paso guarda y tenemos otro metodo para asignar materiales
                        # aquí podrias llamar crear_material_en_paso(paso_id, int(e_id.get()), int(e_qty.get()))
                        pass
                    messagebox.showinfo("Éxito","Paso creado")
                    ver_pasos()
                    mini.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            ctk.CTkButton(mini, text="Agregar Material", fg_color=COLOR_BTN, command=add_row).pack(pady=5)
            ctk.CTkButton(mini, text="Guardar Paso", fg_color=COLOR_BTN, command=guardar_paso).pack(pady=5)

        def modificar_paso_view():
            datos_p = get_sel()
            if not datos_p: return
            mini = ctk.CTkToplevel(main); mini.title("Modificar Paso")
            ctk.CTkLabel(mini, text="Nombre Paso:").pack(pady=5)
            e_nom = ctk.CTkEntry(mini); e_nom.insert(0, datos_p[2]); e_nom.pack(pady=5)

            def guardar():
                modificar_paso(int(datos_p[0]), e_nom.get())
                ver_pasos()
                mini.destroy()
            ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=5)

        btn_volver.configure(command=volver)
        btn_agregar_paso.configure(command=agregar_paso)
        btn_modificar_paso.configure(command=modificar_paso_view)

    btn_ver_pasos.configure(command=ver_pasos)

    cargar_manufacturas()
