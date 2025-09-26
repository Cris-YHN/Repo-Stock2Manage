import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.UsuarioControllers import (
    listar_usuarios, listar_solicitudes,
    aprobar_usuario, rechazar_usuario,
    baja_usuario, alta_usuario, modificar_usuario, listar_inactivos
)

ctk.set_appearance_mode("dark")

COLOR_BG = "#16161a"
COLOR_TOP = "#2cb67d"        # Verde para panel superior
COLOR_BTN = "#7f5af0"        # Botones azul/violeta de la paleta
COLOR_TEXT = "#ffffff"
COLOR_FRAME = "#242629"

def abrir_menu_admin(usuario):
    menuadm = ctk.CTk()
    menuadm.title("Panel Administrador")
    menuadm.geometry("1000x600")
    menuadm.configure(fg_color=COLOR_BG)

    # -------- Panel superior (verde)
    top_panel = ctk.CTkFrame(menuadm, fg_color=COLOR_TOP, height=60)
    top_panel.pack(fill="x")

    lbl_titulo = ctk.CTkLabel(top_panel, text="Panel Administrador", font=("Arial", 20, "bold"),
                              text_color=COLOR_TEXT)
    lbl_titulo.pack(side="left", padx=20)

    lbl_usuario = ctk.CTkLabel(top_panel, text=f"{usuario.nombre} {usuario.apellido}",
                               font=("Arial", 16), text_color=COLOR_TEXT)
    lbl_usuario.pack(side="right", padx=20)

    # -------- Menú desplegable
    opciones = ["Usuarios Activos", "Usuarios Inactivos", "Solicitudes de Usuarios"]
    combo_opciones = ctk.CTkComboBox(menuadm, values=opciones, width=250)
    combo_opciones.set("Usuarios Activos")
    combo_opciones.pack(pady=15)

    # -------- Treeview
    frame_tree = ctk.CTkFrame(menuadm, fg_color=COLOR_FRAME)
    frame_tree.pack(fill="both", expand=True, padx=10, pady=(0,10))

    dgv = ttk.Treeview(frame_tree, columns=("ID","Nombre","Apellido","Puesto","Activo"), show="headings")
    for col in ("ID","Nombre","Apellido","Puesto","Activo"):
        dgv.heading(col, text=col)
        dgv.column(col, anchor="center", width=150)
    dgv.pack(fill="both", expand=True, padx=5, pady=5)

    # -------- Frame botones
    frame_botones = ctk.CTkFrame(menuadm, fg_color=COLOR_FRAME)
    frame_botones.pack(fill="x", pady=(5,10))

    # -------- Funciones internas
    def cargar_datos():
        dgv.delete(*dgv.get_children())
        sel = combo_opciones.get()
        if sel == "Usuarios Activos":
            for u in listar_usuarios():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,u.activo))
        elif sel == "Usuarios Inactivos":
            for u in listar_inactivos():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,u.activo))
        else:
            for u in listar_solicitudes():
                dgv.insert("", "end", values=(u.id_usuario,u.nombre,u.apellido,u.puesto,u.activo))

    def get_sel():
        sel = dgv.focus()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un usuario")
            return None
        return dgv.item(sel)["values"]

    def modificar():
        datos = get_sel()
        if not datos: return
        mini = ctk.CTkToplevel(menuadm)
        mini.title("Modificar Usuario")
        mini.geometry("300x300")
        ctk.CTkLabel(mini, text="Nombre:").pack(pady=5)
        entry_nombre = ctk.CTkEntry(mini); entry_nombre.insert(0, datos[1]); entry_nombre.pack(pady=5)
        ctk.CTkLabel(mini, text="Apellido:").pack(pady=5)
        entry_apellido = ctk.CTkEntry(mini); entry_apellido.insert(0, datos[2]); entry_apellido.pack(pady=5)
        ctk.CTkLabel(mini, text="Puesto:").pack(pady=5)
        combo_puesto = ctk.CTkComboBox(mini, values=["admin","operario","supervisor"])
        combo_puesto.set(datos[3]); combo_puesto.pack(pady=5)

        def guardar():
            modificar_usuario(datos[0], entry_nombre.get(), entry_apellido.get(), combo_puesto.get())
            messagebox.showinfo("Éxito", "Usuario actualizado")
            mini.destroy()
            cargar_datos()

        ctk.CTkButton(mini, text="Guardar", fg_color=COLOR_BTN, command=guardar).pack(pady=10)

    def baja():
        datos = get_sel()
        if datos:
            baja_usuario(datos[0])
            cargar_datos()

    def alta():
        datos = get_sel()
        if datos:
            alta_usuario(datos[0])
            cargar_datos()

    def aprobar():
        datos = get_sel()
        if datos:
            aprobar_usuario(datos[0])
            cargar_datos()

    def rechazar():
        datos = get_sel()
        if datos:
            rechazar_usuario(datos[0])
            cargar_datos()

    # -------- Botones
    ctk.CTkButton(frame_botones, text="Modificar", fg_color=COLOR_BTN, command=modificar).pack(side="left", padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="Dar Baja", fg_color=COLOR_BTN, command=baja).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Dar Alta", fg_color=COLOR_BTN, command=alta).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Aprobar", fg_color=COLOR_BTN, command=aprobar).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Rechazar", fg_color=COLOR_BTN, command=rechazar).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Cerrar Sesión", fg_color="#ff4d4d", command=menuadm.destroy).pack(side="right", padx=10)

    # -------- Inicial
    cargar_datos()
    combo_opciones.configure(command=lambda _: cargar_datos())

    menuadm.mainloop()
