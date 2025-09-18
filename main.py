import tkinter as tk
from database.Database import crear_todas_tablas
from views.login_view import ventana_login

if __name__ == "__main__":
    crear_todas_tablas()  # crea tablas si no existen
    app = ventana_login()
