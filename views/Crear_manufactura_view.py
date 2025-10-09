import customtkinter as ctk
from tkinter import ttk, messagebox
from assets.Themes import themes
from controllers.ManufacturaControllers import (crear_manufactura, listar_manufactura, listar_pasos, Buscar_manufactura_por_nombre, modificar_manufactura, crear_paso,modificar_paso)
from controllers.MaterialControllers import (verificar_existencia)

def gestion_crear_manufactura(parent_frame):
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


    # Setear columnas
    dgv = ttk.Treeview(frame_tree, columns=("ID", "Nombre"), show="headings", yscrollcommand=scrollbar_y.set)
    for col in ("ID", "Nombre"):
        dgv.heading(col, text=col, command=lambda c=col: ordenar_por_columna(c))
        dgv.column(col, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    scrollbar_y.configure(command=dgv.yview)

    def cargar_todos():
        dgv.delete(*dgv.get_children())
        for r in listar_manufactura():
            dgv.insert("", "end", values=(r.id_manufactura, r.nombre))
    
    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una Manufactura")
            return None
        return dgv.item(sel)["values"]

    def agregar_manufactura():
        mini = ctk.CTkToplevel(main)
        mini.title("Nueva Manufactura")
        mini.transient(main)
        mini.grab_set()
        mini.geometry("250x200")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(frame_center)
        entry_nombre.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Debe ingresar un nombre")
                return
            crear_manufactura(nombre)
            cargar_todos()
            mini.destroy()

        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=10)
    
    def buscarXNombre():
        mini = ctk.CTkToplevel(main); mini.transient(main); mini.grab_set()
        mini.title("Buscar Manufactura")
        mini.geometry("250x200")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre Manufactura").pack(pady=5)
        entry_nombre = ctk.CTkEntry(frame_center); entry_nombre.pack(pady=5)

        def go():
            try:
                mfnom = entry_nombre.get()
                dgv.delete(*dgv.get_children())
                resultados = Buscar_manufactura_por_nombre(mfnom)
                if resultados:
                    for mf in resultados:
                        dgv.insert("", "end", values=(mf.id_manufactura, mf.nombre))
                else:
                    messagebox.showinfo("Buscar", f"No existe Manufactura {mfnom}")
                mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            
        ctk.CTkButton(frame_center, text="Buscar", fg_color=colors["BUTTON"], command=go).pack(pady=10)

    
    def modificar():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(main)
        mini.title("Modificar Manufactura"); mini.transient(main); mini.grab_set()
        mini.geometry("250x200")

        frame_center = ctk.CTkFrame(mini, fg_color="transparent")
        frame_center.pack(expand=True)

        ctk.CTkLabel(frame_center, text="Nombre").pack(pady=5)
        entry_nom = ctk.CTkEntry(frame_center); entry_nom.insert(0, datos[1]); entry_nom.pack(pady=5)

        def guardar():
            try:
                modificar_manufactura(int(datos[0]), entry_nom.get())
                cargar_todos(); mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        ctk.CTkButton(frame_center, text="Guardar", fg_color=colors["BUTTON"], command=guardar).pack(pady=10)
    
    def ver_pasos():
        datos = get_sel()
        if not datos:
            return
        id_manuf = datos[0]

        mini = ctk.CTkToplevel(main)
        mini.title(f"Pasos - Manufactura {id_manuf}")
        mini.geometry("600x500")
        mini.transient(main)
        mini.grab_set()

        frame_pasos = ctk.CTkFrame(mini, fg_color=colors["FRAME"])
        frame_pasos.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar_y = ctk.CTkScrollbar(frame_pasos, orientation="vertical")
        scrollbar_y.pack(side="right", fill="y")

        columnas_p = ("Paso", "ID Material", "Nombre Material", "Cantidad Necesaria")
        tree_pasos = ttk.Treeview(frame_pasos, columns=columnas_p, show="headings", yscrollcommand=scrollbar_y.set)
        for c in columnas_p:
            tree_pasos.heading(c, text=c)
            tree_pasos.column(c, anchor="center", width=120)
        tree_pasos.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar_y.configure(command=tree_pasos.yview)

        def cargar_pasos():
            tree_pasos.delete(*tree_pasos.get_children())
            for p in listar_pasos(id_manuf):
                tree_pasos.insert("", "end",
                                values=(p.id_paso, p.id_material, p.nombre, p.cantidad_necesaria))

        # -------- Botones dentro de la ventana de pasos --------
        btn_frame = ctk.CTkFrame(mini, fg_color=colors["FRAME"])
        btn_frame.pack(fill="x", pady=5)

        def agregar_paso_view():
            win = ctk.CTkToplevel(mini)
            win.title("Agregar Paso")
            win.transient(mini)
            win.grab_set()
            win.geometry("400x350")

            rows = []  # guarda (entry_id, entry_qty)

            frame_rows = ctk.CTkFrame(win)
            frame_rows.pack(pady=10)

            def add_row():
                # si ya hay filas, exigir que la última no esté vacía
                if rows:
                    e_id_last, e_qty_last = rows[-1]
                    if not e_id_last.get().strip() or not e_qty_last.get().strip():
                        messagebox.showwarning("Atención",
                                            "Complete el material anterior antes de agregar otro.")
                        return

                row = ctk.CTkFrame(frame_rows)
                row.pack(pady=5)

                e_id = ctk.CTkEntry(row, width=80, placeholder_text="ID Material")
                e_id.grid(row=0, column=0, padx=5)
                e_qty = ctk.CTkEntry(row, width=80, placeholder_text="Cantidad")
                e_qty.grid(row=0, column=1, padx=5)

                # botón para eliminar la fila
                def remove_row():
                    rows.remove((e_id, e_qty))
                    row.destroy()

                ctk.CTkButton(row, text="❌", width=25, fg_color="#ff4d4d",
                            command=remove_row).grid(row=0, column=2, padx=5)

                rows.append((e_id, e_qty))

            def guardar_pasos():
                try:
                    # validar que la última fila no esté vacía
                    if rows and (not rows[-1][0].get().strip() or not rows[-1][1].get().strip()):
                        messagebox.showwarning("Atención",
                                            "Complete todos los campos antes de guardar.")
                        return

                    # determinar el próximo número de paso una sola vez
                    pasos_existentes = listar_pasos(id_manuf)
                    nuevo_paso = max([p.id_paso for p in pasos_existentes], default=0) + 1

                    for e_id, e_qty in rows:
                        id_material = int(e_id.get())
                        cantidad = int(e_qty.get())
                        if not verificar_existencia(id_material):
                            messagebox.showerror("Error", f"El material {id_material} no existe.")
                            return

                        # todos los materiales de esta carga comparten el mismo paso
                        crear_paso(id_manuf, nuevo_paso, id_material, cantidad)


                    cargar_pasos()
                    win.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

            # Botones en la ventana de agregar
            ctk.CTkButton(win, text="Agregar Material", fg_color=colors["BUTTON"],
                        command=add_row).pack(pady=5)
            ctk.CTkButton(win, text="Guardar", fg_color=colors["BUTTON"],
                        command=guardar_pasos).pack(pady=5)

            # Comienza con una fila inicial
            add_row()

        def modificar_paso_view():
            sel = tree_pasos.focus()
            if not sel:
                messagebox.showwarning("Atención", "Seleccione un paso para modificar")
                return
            valores = tree_pasos.item(sel)["values"]
            paso_nro, mat_actual, nombre_material, cant_actual = valores
            mat_original = mat_actual

            win = ctk.CTkToplevel(mini)
            win.title(f"Modificar Paso {paso_nro}")
            win.transient(mini)
            win.grab_set()
            win.geometry("400x350")

            frame_center = ctk.CTkFrame(win, fg_color="transparent")
            frame_center.pack(expand=True)

            ctk.CTkLabel(frame_center, text="ID Material:").pack(pady=5)
            entry_mat = ctk.CTkEntry(frame_center)
            entry_mat.insert(0, mat_actual)
            entry_mat.pack(pady=5)

            ctk.CTkLabel(frame_center, text="Cantidad Necesaria:").pack(pady=5)
            entry_cant = ctk.CTkEntry(frame_center)
            entry_cant.insert(0, cant_actual)
            entry_cant.pack(pady=5)

            def guardar_modificacion():
                try:
                    id_material = int(entry_mat.get())
                    cantidad = int(entry_cant.get())
                    modificar_paso(id_manuf, paso_nro, mat_original, id_material, cantidad)
                    cargar_pasos()
                    win.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Datos inválidos")

            ctk.CTkButton(frame_center, text="Guardar Cambios", fg_color=colors["BUTTON"],
                        command=guardar_modificacion).pack(pady=10)

        cargar_pasos()

        ctk.CTkButton(btn_frame, text="Agregar Paso", fg_color=colors["BUTTON"],
                    command=agregar_paso_view).pack(side="left", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Modificar Paso", fg_color=colors["BUTTON"],
                    command=modificar_paso_view).pack(side="left", padx=10, pady=10)



    # barra de botones
    fb = ctk.CTkFrame(main, fg_color=colors["FRAME"])
    fb.pack(fill="x", pady=5)
    ctk.CTkButton(fb, text="Ver Manufacturas", fg_color=colors["BUTTON"], command=cargar_todos).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Agregar Manufacturas", fg_color=colors["BUTTON"], command=agregar_manufactura).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Buscar Nombre", fg_color=colors["BUTTON"], command=buscarXNombre).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Modificar Manufactura", fg_color=colors["BUTTON"], command=modificar).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(fb, text="Ver Pasos", fg_color=colors["BUTTON"], command=ver_pasos).pack(side="left", padx=10, pady=10)

    cargar_todos()