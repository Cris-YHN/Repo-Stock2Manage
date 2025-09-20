import tkinter as tk
from tkinter import ttk, messagebox
from controllers.UsuarioControllers import (
    listar_usuarios, listar_solicitudes,
    aprobar_usuario, rechazar_usuario,
    baja_usuario, alta_usuario, modificar_usuario, buscar_id, listar_inactivos
)

def abrir_menu_admin(usuario):
    menuadm = tk.Tk()
    menuadm.title("Menú Administrador")
    menuadm.geometry("800x500")
    menuadm.configure(bg="#004643")

    tk.Label(menuadm, text=f"Bienvenido {usuario.nombre} (Admin)", bg="#f9bc60", font=("Arial", 16)).pack(pady=20)

    # Botón para abrir gestión de usuarios
    tk.Button(menuadm, text="Gestionar Usuarios", command=lambda: gestion_usuarios(menuadm)).pack(pady=5)
    tk.Button(menuadm, text="Cerrar Sesión", command=menuadm.destroy).pack(pady=5)

    menuadm.mainloop()

def gestion_usuarios(parent):
    pop = tk.Toplevel(parent)
    pop.title("Gestión de Usuarios")
    pop.geometry("900x500")
    pop.configure(bg="#004643")

    # Tabla
    dgv = ttk.Treeview(pop, columns=("ID", "Nombre", "Apellido", "Puesto", "Activo"), show="headings")
    for col in ("ID", "Nombre", "Apellido", "Puesto", "Activo"):
        dgv.heading(col, text=col)
    dgv.pack(fill=tk.BOTH, expand=True)

    def cargar_todos():
        dgv.delete(*dgv.get_children())  #Borra datos que estaban en el treeview
        for u in listar_usuarios(): #Llama a la funcion listar usuarios del controller
            dgv.insert("", tk.END, values=(u.id_usuario, u.nombre, u.apellido, u.puesto, u.activo))

    def cargar_solicitudes():
        dgv.delete(*dgv.get_children())
        for u in listar_solicitudes():
            dgv.insert("", tk.END, values=(u.id_usuario, u.nombre, u.apellido, u.puesto, u.activo))

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un usuario")
            return None
        return dgv.item(sel)["values"]

    def aprobar():
        datos = get_sel()
        if datos: 
            aprobar_usuario(datos[0])
            cargar_solicitudes()

    def rechazar():
        datos = get_sel()
        if datos: 
            rechazar_usuario(datos[0])
            cargar_solicitudes()

    def dar_baja():
        datos = get_sel()
        if datos: 
            baja_usuario(datos[0])
            cargar_todos()

    def dar_alta():
        datos = get_sel()
        if datos: 
            alta_usuario(datos[0])
            cargar_todos()

    def modificar():
        datos = get_sel()
        if not datos: return

        mini = tk.Toplevel(pop)
        mini.title("Modificar Usuario")

        tk.Label(mini, text="Nombre").pack()
        entry_nombre = tk.Entry(mini); entry_nombre.insert(0, datos[1]); entry_nombre.pack()

        tk.Label(mini, text="Apellido").pack()
        entry_apellido = tk.Entry(mini); entry_apellido.insert(0, datos[2]); entry_apellido.pack()

        tk.Label(mini, text="Puesto").pack()
        combo_puesto = ttk.Combobox(mini, values=["admin", "operario", "supervisor"], state="readonly")
        combo_puesto.set(datos[3]); combo_puesto.pack()

        def guardarMod():
            modificar_usuario(datos[0], entry_nombre.get(), entry_apellido.get(), combo_puesto.get())
            messagebox.showinfo("Éxito", "Usuario actualizado")
            mini.destroy()
            cargar_todos()

        tk.Button(mini, text="Guardar", command=guardarMod).pack(pady=10)
    
    def buscarID():
        mini = tk.Toplevel(pop)
        mini.title("Buscar ID")

        tk.Label(mini, text="ID Usuario").pack()
        entry_id = tk.Entry(mini) 
        entry_id.pack() 

        def guardarID():
            iduser = entry_id.get()
            dgv.delete(*dgv.get_children())
            for u in buscar_id(iduser):
                dgv.insert("", tk.END, values=(u.id_usuario, u.nombre, u.apellido, u.puesto, u.activo))
        
        tk.Button(mini, text="Buscar", command=guardarID).pack(pady=10)

    def cargar_inactivos():
        dgv.delete(*dgv.get_children())  
        for u in listar_inactivos(): 
            dgv.insert("", tk.END, values=(u.id_usuario, u.nombre, u.apellido, u.puesto, u.activo))


    # Frame de los botones
    frame_btns = tk.Frame(pop, bg="#004643")
    frame_btns.pack(pady=10)

    # Botones de acciones
    tk.Button(frame_btns, text="Ver Todos", command=cargar_todos).grid(row=0, column=0, padx=5)
    tk.Button(frame_btns, text="Busqueda por ID", command=buscarID).grid(row=0, column=1, padx=5)
    tk.Button(frame_btns, text="Modificar", command=modificar).grid(row=0, column=2, padx=5)
    tk.Button(frame_btns, text="Baja", command=dar_baja).grid(row=0, column=3, padx=5)
    tk.Button(frame_btns, text="Ver Usuarios Inactivos", command=cargar_inactivos).grid(row=0, column=4, padx=40)
    tk.Button(frame_btns, text="Alta", command=dar_alta).grid(row=0, column=5, padx=5)
    tk.Button(frame_btns, text="Ver Solicitudes", command=cargar_solicitudes).grid(row=0, column=6, padx=40)
    tk.Button(frame_btns, text="Aprobar", command=aprobar).grid(row=0, column=7, padx=5)
    tk.Button(frame_btns, text="Rechazar", command=rechazar).grid(row=0, column=8, padx=5)

    cargar_todos()