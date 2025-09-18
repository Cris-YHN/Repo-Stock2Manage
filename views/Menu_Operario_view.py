import tkinter as tk

def abrir_menu_operario(usuario):
    win = tk.Toplevel()
    win.title("Menú Operario")
    tk.Label(win, text=f"Bienvenido {usuario.nombre} (Operario)").pack(pady=20)
    tk.Button(win, text="Registrar Remito").pack(pady=5)
    tk.Button(win, text="Cerrar Sesión", command=win.destroy).pack(pady=5)