import tkinter as tk
from views.Stock_view import gestion_stock
from views.Proveedores_view import gestion_proveedores
from views.Remitos_view import Gestion_Remitos

def abrir_menu_supervisor(usuario):
    menusup = tk.Tk()
    menusup.title("Menú Supervisor")
    menusup.geometry("800x500")
    menusup.configure(bg= "#004643")
    
    tk.Label(menusup, text=f"Bienvenido {usuario.nombre} (Supervisor)", bg="#f9bc60", font=("Arial", 16)).pack(pady=20)

    tk.Button(menusup, text="Consultar Stock", command=gestion_stock).pack(pady=5)
    tk.Button(menusup, text="Consultar Proveedores", command=gestion_proveedores).pack(pady=5)
    tk.Button(menusup, text="Consultar Remitos", command=Gestion_Remitos).pack(pady=5)
    tk.Button(menusup, text="Consultar Manufactura").pack(pady=5)
    tk.Button(menusup, text="Cerrar Sesión", command=menusup.destroy).pack(pady=5)

    menusup.mainloop()
