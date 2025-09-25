import tkinter as tk
from tkinter import ttk, messagebox
from controllers.CPControllers import Buscar_proveedor_por_nombre,listar_cp
from controllers.ProveedorControllers import listar_proveedores, Buscar_proveedor_por_id, crear_proveedor, modificar_proveedor

def gestion_proveedores():
    Wprov = tk.Toplevel()
    Wprov.title("Gestion Proveedores")
    Wprov.geometry("800x500")
    Wprov.configure(bg="#004643")

    # Tabla
    dgv = ttk.Treeview(Wprov, columns=("ID", "Nombre", "Codigo Postal", "Localidad", "provincia", "Calle", "Numero", "Telefono"), show="headings")
    for col in ("ID", "Nombre", "Codigo Postal", "Localidad", "provincia", "Calle", "Numero", "Telefono"):
        dgv.heading(col, text=col)
    dgv.pack(fill=tk.BOTH, expand=True)

    def cargar_todos():
        dgv.delete(*dgv.get_children())  #Borra datos que estaban en el treeview
        for p in listar_proveedores(): #Llama a la funcion listar usuarios del controller
            dgv.insert("", tk.END, values=(p.id_proveedor, p.nombre_proveedor, p.codigo_postal, p.localidad, p.provincia, p.calle, p.numero, p.telefono))


    def buscarID():
        mini = tk.Toplevel()
        mini.title("Buscar ID")

        tk.Label(mini, text="ID Proveedor").pack()
        entry_id = tk.Entry(mini) 
        entry_id.pack() 

        def guardarID():
            try:
                idprov = int(entry_id.get())
                dgv.delete(*dgv.get_children())
                for p in Buscar_proveedor_por_id(idprov):
                    dgv.insert("", tk.END, values=(p.id_proveedor, p.nombre_proveedor, p.codigo_postal, p.calle, p.numero, p.telefono))
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")
        
        tk.Button(mini, text="Buscar", command=guardarID).pack(pady=10)
    
    def agregar_proveedor():
        mini = tk.Toplevel(Wprov)
        mini.title("Nuevo Proveedor")

        tk.Label(mini, text="Nombre").pack()
        entry_nombre = tk.Entry(mini); entry_nombre.pack()

        tk.Label(mini, text="Codigo Postal").pack()
        entry_cp = tk.Entry(mini); entry_cp.pack()

        tk.Label(mini, text="Calle").pack()
        entry_calle = tk.Entry(mini); entry_calle.pack()

        tk.Label(mini, text="Numero").pack()
        entry_numero = tk.Entry(mini); entry_numero.pack()

        tk.Label(mini, text="Telefono").pack()
        entry_telefono = tk.Entry(mini); entry_telefono.pack()

        def guardar():
            try:
                crear_proveedor(entry_nombre.get(), entry_cp.get(), entry_calle.get(), entry_numero.get(), entry_telefono.get())
                cargar_todos()
                mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(mini, text="Guardar", command=guardar).pack(pady=10)
    
    def modificar_prov():
        datos = get_sel()
        if not datos:
            messagebox.showerror("Error", "Seleccione un proveedor")
            return

        mini = tk.Toplevel(Wprov)
        mini.title("Modificar Proveedor")

        tk.Label(mini, text="Nombre").pack()
        entry_nombre = tk.Entry(mini); entry_nombre.insert(0, datos[1]); entry_nombre.pack()

        tk.Label(mini, text="Codigo Postal").pack()
        entry_cp = tk.Entry(mini); entry_cp.insert(0, datos[2]); entry_cp.pack()

        tk.Label(mini, text="Calle").pack()
        entry_calle = tk.Entry(mini); entry_calle.insert(0, datos[5]); entry_calle.pack()

        tk.Label(mini, text="Numero").pack()
        entry_numero = tk.Entry(mini); entry_numero.insert(0, datos[6]); entry_numero.pack()

        tk.Label(mini, text="Telefono").pack()
        entry_telefono = tk.Entry(mini); entry_telefono.insert(0, datos[7]); entry_telefono.pack()

        def guardar():
            try:
                modificar_proveedor(
                    int(datos[0]),                   # id_proveedor
                    entry_nombre.get(),              # nombre
                    entry_cp.get(),                  # codigo_postal
                    entry_calle.get(),               # calle
                    entry_numero.get(),              # numero
                    entry_telefono.get()             # telefono
                )
                cargar_todos()  # refrescar la tabla
                mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(mini, text="Guardar", command=guardar).pack(pady=10)
    
    def ver_cp():
        mini = tk.Toplevel()
        mini.title("Ver Codigos Postales")
        mini.geometry("800x500")

        # Frame contenedor para treeview + scrollbar
        frame_tabla = tk.Frame(mini)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        # Scrollbar vertical
        scrollbar_y = tk.Scrollbar(frame_tabla, orient="vertical")
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal
        scrollbar_x = tk.Scrollbar(frame_tabla, orient="horizontal")
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview con scroll
        dgvmini = ttk.Treeview(
            frame_tabla,
            columns=("Codigo", "Ciudad", "Provincia", "Pais"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set)
        for col in ("Codigo", "Ciudad", "Provincia", "Pais"):
            dgvmini.heading(col, text=col)
            dgvmini.column(col, width=150)  # ancho fijo para que se vea ordenado

        dgvmini.pack(fill=tk.BOTH, expand=True)

        # Configurar scrollbars
        scrollbar_y.config(command=dgvmini.yview)
        scrollbar_x.config(command=dgvmini.xview)

        def cargar_todos():
            dgvmini.delete(*dgvmini.get_children())  #Borra datos que estaban en el treeview
            for cp in listar_cp(): #Llama a la funcion listar usuarios del controller
                dgvmini.insert("", tk.END, values=(cp.codigo_postal, cp.ciudad, cp.provincia, cp.pais))
        
        def cargar_busqueda():
            
            mini = tk.Toplevel()
            mini.title("Buscar Ciudad")

            tk.Label(mini, text="Ciudad").pack()
            entry_ciudad = tk.Entry(mini) 
            entry_ciudad.pack() 

            def guardarciudad():
                try:
                    ciudad = entry_ciudad.get()
                    dgvmini.delete(*dgvmini.get_children())  #Borra datos que estaban en el treeview
                    for cp in Buscar_proveedor_por_nombre(ciudad): #Llama a la funcion listar usuarios del controller
                        dgvmini.insert("", tk.END, values=(cp.codigo_postal, cp.ciudad, cp.provincia, cp.pais))
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un problema: {e}")
            
            tk.Button(mini, text="Buscar", command=guardarciudad).pack(pady=10)
                
        
        # Frame de los botones
        frame_btns_mini = tk.Frame(mini, bg="#004643")
        frame_btns_mini.pack(pady=10)

        # Botones de acciones
        tk.Button(frame_btns_mini, text="Ver Todos", command=cargar_todos).grid(row=0, column=0, padx=5)
        tk.Button(frame_btns_mini, text="Buscar Ciudad", command=cargar_busqueda).grid(row=0, column=1, padx=5)

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un usuario")
            return None
        return dgv.item(sel)["values"]

    
    # Frame de los botones
    frame_btns = tk.Frame(Wprov, bg="#004643")
    frame_btns.pack(pady=10)

    # Botones de acciones
    tk.Button(frame_btns, text="Ver Todos", command=cargar_todos).grid(row=0, column=0, padx=5)
    tk.Button(frame_btns, text="Busqueda por ID", command=buscarID).grid(row=0, column=1, padx=5)
    tk.Button(frame_btns, text="Agregar Proveedor", command=agregar_proveedor).grid(row=0, column=2, padx=20)
    tk.Button(frame_btns, text="Modificar Proveedor", command=modificar_prov).grid(row=0, column=3, padx=5)
    tk.Button(frame_btns, text="Ver Codigos Postales", command=ver_cp).grid(row=0, column=4, padx=50)

    cargar_todos()