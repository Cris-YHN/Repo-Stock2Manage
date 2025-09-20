import tkinter as tk
from Stock_view import (gestion_materiales)

def abrir_menu_supervisor(usuario):
    menusup = tk.Toplevel()
    menusup.title("Menú Supervisor")
    menusup.geometry("800x500")
    menusup.configure(bg= "#004643")
    
    tk.Label(menusup, text=f"Bienvenido {usuario.nombre} (Supervisor)", bg="#f9bc60", font=("Arial", 16)).pack(pady=20)

    tk.Button(menusup, text="Consultar Stock", command=gestion_materiales()).pack(pady=5)
    tk.Button(menusup, text="Consultar Proveedores").pack(pady=5)
    tk.Button(menusup, text="Consultar Manufactura").pack(pady=5)
    tk.Button(menusup, text="Cerrar Sesión", command=menusup.destroy).pack(pady=5)

    menusup.mainloop()


