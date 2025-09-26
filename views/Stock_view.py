# views/Stock_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.MaterialControllers import listar_materiales, crear_material, modificar_material, alta_material,baja_material,Carga_Materiales_delRemito,listar_materiales_escasos,listar_materiales_inactivos,buscar_id
from controllers.RemitosControllers import crear_remito
from controllers.ProveedorControllers import listar_proveedores
from entities.RemitosEntity import RemitoDetalle
import datetime

def gestion_stock():
    Wstock = tk.Toplevel()
    Wstock.title("Gestión de Stock")
    Wstock.geometry("800x500")

    # --- Tabla ---
    columnas = ("ID", "Nombre", "Stock", "ID Proveedor", "Proveedor", "Max Ingreso", "Activo")
    dgv = ttk.Treeview(Wstock, columns=columnas, show="headings", height=15)
    for col in columnas:
        dgv.heading(col, text=col)
        dgv.column(col, width=100)
    dgv.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Funciones internas ---
    def refrescar(lista):
        dgv.delete(*dgv.get_children())
        for m in lista:
            dgv.insert("", tk.END, values=(
                m.id_material, m.nombre, m.stock_disponible,
                m.id_proveedor, m.nombre_proveedor,
                m.max_ingreso, m.activo
            ))

    def mostrar_activos():
        refrescar(listar_materiales())

    def mostrar_inactivos():
        refrescar(listar_materiales_inactivos())

    def mostrar_escasos():
        refrescar(listar_materiales_escasos())

    def buscarID():
        mini = tk.Toplevel()
        mini.title("Buscar ID")

        tk.Label(mini, text="ID Material").pack()
        entry_id = tk.Entry(mini) 
        entry_id.pack() 

        def guardarID():
            try:
                idmat = int(entry_id.get().strip())
                dgv.delete(*dgv.get_children())
                material = buscar_id(idmat)

                if material:
                    dgv.insert("", tk.END, values=(
                    material.id_material, 
                    material.nombre, 
                    material.stock_disponible,
                    material.id_proveedor, 
                    material.nombre_proveedor,
                    material.max_ingreso, 
                    material.activo
                    ))
                else:
                    messagebox.showinfo("Buscar", f"No existe un material con ID {idmat}")

            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        tk.Button(mini, text="Buscar", command=guardarID).pack(pady=10)

    def agregar_mat():
        mini = tk.Toplevel(Wstock)
        mini.title("Nuevo Material")

        tk.Label(mini, text="Nombre").pack()
        entry_nombre = tk.Entry(mini); entry_nombre.pack()

        tk.Label(mini, text="ID Proveedor").pack()
        entry_prov = tk.Entry(mini); entry_prov.pack()

        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                id_prov = int(entry_prov.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", str(e))

            if not nombre or not id_prov:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Verificar que exista el proveedor
            proveedores = listar_proveedores()
            if not any(p.id_proveedor == id_prov for p in proveedores):
                messagebox.showerror("Error", f"No existe un proveedor con ID {id_prov}")
                return
            
            respuesta = messagebox.askyesno(
                "Confirmación",
                "¿Está seguro de que desea agregar este material?"
            )
            if not respuesta:
                return
            
            crear_material(nombre, id_prov)
            mostrar_activos()
            mini.destroy()

        tk.Button(mini, text="Guardar", command=guardar).pack(pady=10)

    def modificar():
        selected = dgv.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un material")
            return
        datos = dgv.item(selected[0], "values")

        mini = tk.Toplevel(Wstock)
        mini.title("Modificar Material")

        tk.Label(mini, text="Nombre").pack()
        entry_nombre = tk.Entry(mini); entry_nombre.insert(0, datos[1]); entry_nombre.pack()

        tk.Label(mini, text="Stock").pack()
        entry_stock = tk.Entry(mini); entry_stock.insert(0, datos[2]); entry_stock.pack()

        tk.Label(mini, text="ID Proveedor").pack()
        entry_prov = tk.Entry(mini); entry_prov.insert(0, datos[3]); entry_prov.pack()

        def guardar():
            try:
                nombre = entry_nombre.get()
                stock = int(entry_stock.get())
                id_prov = int(entry_prov.get())
                idmat = int(datos[0])
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            
            if not nombre or not stock or not id_prov:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            respuesta = messagebox.askyesno(
                "Confirmación",
                "¿Está seguro de que desea realizar estos cambios?"
            )
            if not respuesta:
                return

            try:
                modificar_material(idmat,nombre, stock, id_prov)
                mostrar_activos()
                mini.destroy()
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(mini, text="Guardar", command=guardar).pack(pady=10)

    def baja():
        selected = dgv.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un material")
            return
        datos = dgv.item(selected[0], "values")

        respuesta = messagebox.askyesno(
            "Confirmación",
            "¿Está seguro de que desea realizar estos cambios?"
            )
        if not respuesta:
            return
        
        baja_material(int(datos[0]))
        mostrar_activos()

    def alta():
        selected = dgv.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un material")
            return
        datos = dgv.item(selected[0], "values")

        respuesta = messagebox.askyesno(
            "Confirmación",
            "¿Está seguro de que desea realizar estos cambios?"
            )
        if not respuesta:
            return

        alta_material(int(datos[0]))
        mostrar_activos()

    def cargar_remito_view():
        mini = tk.Toplevel(Wstock)
        mini.title("Cargar Remito")

        materiales = []

        tk.Label(mini, text="Proveedor").pack()
        entry_prov = tk.Entry(mini)
        entry_prov.pack(pady=5)
        
        frame = tk.Frame(mini)
        frame.pack(pady=10)

        def eliminar_fila(row, entry_pair):
            materiales.remove(entry_pair)
            row.destroy()

        def agregar():
            # Si ya hay materiales cargados, validar el último antes de permitir uno nuevo
            if materiales:
                last_id, last_stock = materiales[-1]
                if not last_id.get().strip() or not last_stock.get().strip():
                    messagebox.showerror("Error", "Complete el material anterior antes de agregar otro")
                    return
                try:
                    int(last_id.get())
                    int(last_stock.get())
                except ValueError:
                    messagebox.showerror("Error", "El ID y la cantidad deben ser números")
                    return

            # Si pasó la validación, agregar un nuevo par de entries
            row = tk.Frame(frame)
            row.pack(pady=5)

            tk.Label(row, text="ID Material").grid(row=0, column=0, padx=5)
            entry_id = tk.Entry(row, width=10)
            entry_id.grid(row=0, column=1, padx=5)

            tk.Label(row, text="Cantidad").grid(row=0, column=2, padx=5)
            entry_stock = tk.Entry(row, width=10)
            entry_stock.grid(row=0, column=3, padx=5)

            btn_borrar = tk.Button(row, text="❌", fg="red", command=lambda r=row, e=(entry_id, entry_stock): eliminar_fila(r, e))
            btn_borrar.grid(row=0, column=4, padx=5)

            materiales.append((entry_id, entry_stock))

        def guardar():
            try:
                id_proveedor = int(entry_prov.get())
                proveedores = listar_proveedores()
                if not any(p.id_proveedor == id_proveedor for p in proveedores):
                    messagebox.showerror("Error", f"No existe un proveedor con ID {id_proveedor}")
                    return
                
                fecha = datetime.date.today().strftime("%Y-%m-%d")
                detalles = []

                for entry_id, entry_stock in materiales:
                    id_mat = int(entry_id.get())
                    cant = int(entry_stock.get())
                    detalles.append(RemitoDetalle(id_material=id_mat, cantidad=cant))
                    Carga_Materiales_delRemito(id_mat, cant)

                respuesta = messagebox.askyesno(
                    "Confirmación",
                    "¿Está seguro de que desea realizar estos cambios?"
                    )
                if not respuesta:
                    return

                crear_remito(fecha, id_proveedor, detalles)
                mostrar_activos()
                messagebox.showinfo("Éxito", "Remito cargado correctamente")
                mini.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un problema: {e}")

        tk.Button(mini, text="Agregar Material", command=agregar).pack(pady=5)
        tk.Button(mini, text="Guardar Remito", command=guardar).pack(pady=5)

    # Los distintos Botones
    barra = tk.Frame(Wstock); barra.pack(pady=5)

    tk.Button(barra, text="Activos", command=mostrar_activos).grid(row=0, column=0, padx=5)
    tk.Button(barra, text="Inactivos", command=mostrar_inactivos).grid(row=0, column=1, padx=5)
    tk.Button(barra, text="Buscar por ID", command=buscarID).grid(row=0, column=2, padx=5)
    tk.Button(barra, text="Escasos", command=mostrar_escasos).grid(row=0, column=3, padx=5)
    tk.Button(barra, text="Agregar", command=agregar_mat).grid(row=0, column=4, padx=5)
    tk.Button(barra, text="Modificar", command=modificar).grid(row=0, column=5, padx=5)
    tk.Button(barra, text="Baja", command=baja).grid(row=0, column=6, padx=5)
    tk.Button(barra, text="Alta", command=alta).grid(row=0, column=7, padx=5)
    tk.Button(barra, text="Remito", command=cargar_remito_view).grid(row=0, column=8, padx=5)
    
    mostrar_activos()
