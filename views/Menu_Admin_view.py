import tkinter as tk

def abrir_menu_admin(usuario):
    win = tk.Toplevel()
    win.title("Menú Administrador")
    tk.Label(win, text=f"Bienvenido {usuario.nombre} (Admin)").pack(pady=20)
    tk.Button(win, text="Gestionar Usuarios").pack(pady=5)
    tk.Button(win, text="Cerrar Sesión", command=win.destroy).pack(pady=5)