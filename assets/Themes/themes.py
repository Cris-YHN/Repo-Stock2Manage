# themes.py
import darkdetect

LIGHT_MODE = {
    "BG": "#fffffe",
    "FRAME": "#f0f0f0",
    "TOP": "#3da9fc",
    "PARAGRAPH": "#5f6c7b",
    "BUTTON": "#3da9fc",
    "BUTTON_OFF": "#cccccc",
    "BUTTON_TXT": "#ffffff",
    "BUTTON_TXT_OFF": "#777777",
    "TEXT": "#094067"
}

DARK_MODE = {
    "BG": "#0f0e17",
    "FRAME": "#242629",
    "TOP": "#2cb67d",
    "PARAGRAPH": "#a7a9be",
    "BUTTON": "#7f5af0",
    "BUTTON_OFF": "#3a3a3a",
    "BUTTON_TXT": "#ffffff",
    "BUTTON_TXT_OFF": "#777777",
    "TEXT": "#ffffff"
}

# --- Estado global ---
current_mode = None
current_colors = None

def init_theme():
    """Detecta el tema del sistema y establece el inicial."""
    global current_mode, current_colors
    system_theme = darkdetect.theme()
    if system_theme == "Dark":
        current_mode = "dark"
        current_colors = DARK_MODE
    else:
        current_mode = "light"
        current_colors = LIGHT_MODE

def get_colors():
    """Devuelve el diccionario de colores actual."""
    return current_colors

def toggle_theme():
    """Cambia entre modo claro y oscuro."""
    global current_mode, current_colors
    if current_mode == "light":
        current_mode = "dark"
        current_colors = DARK_MODE
    else:
        current_mode = "light"
        current_colors = LIGHT_MODE
    return current_colors  # útil para actualizar vistas
