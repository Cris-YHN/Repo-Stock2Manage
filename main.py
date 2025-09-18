import tkinter as tk
from database.Database import crear_todas_tablas
from views.login_view import LoginView

if __name__ == "__main__":
    crear_todas_tablas()  # crea tablas si no existen
    root = tk.Tk()
    root.geometry("700x500")
    root.resizable(False, False)
    root.configure(bg="#004643")
    app = LoginView(root)
    root.mainloop()