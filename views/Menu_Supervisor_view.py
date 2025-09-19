import tkinter as tk

def abrir_menu_supervisor(usuario):
    win = tk.Toplevel()
    win.title("Menú Supervisor")
    tk.Label(win, text=f"Bienvenido {usuario.nombre} (Supervisor)").pack(pady=20)
    tk.Button(win, text="Ver Reportes").pack(pady=5)
    tk.Button(win, text="Cerrar Sesión", command=win.destroy).pack(pady=5)