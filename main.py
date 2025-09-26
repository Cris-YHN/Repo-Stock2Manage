from database.Database import crear_todas_tablas
from views.login_view import ventana_login

if __name__ == "__main__":
    crear_todas_tablas()  # crea tablas si no existen
    ventana_login() # abre la ventana login
