import customtkinter as ctk

class CTkAutocompleteEntry(ctk.CTkEntry):
    def __init__(self, master=None, values=None, **kwargs):
        super().__init__(master, **kwargs)
        self.values = values or []
        self.dropdown = None
        self.bind("<KeyRelease>", self._on_keyrelease)

    def _on_keyrelease(self, event):
        texto = self.get().lower()

        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None

        if not texto:
            return

        matches = [v for v in self.values if texto in v.lower()]
        if matches:
            # Crear dropdown con width desde el inicio
            ancho = self.winfo_width()
            self.dropdown = ctk.CTkFrame(
                self.master,
                fg_color="#2b2b2b",
                corner_radius=8,
                width=ancho
            )

            for v in matches[:5]:
                lbl = ctk.CTkLabel(self.dropdown, text=v, anchor="w")
                lbl.pack(fill="x", padx=5, pady=2)
                lbl.bind("<Button-1>", lambda e, val=v: self._select(val))

            self.update_idletasks()
            x = self.winfo_x()
            y = self.winfo_y() + self.winfo_height()

            # Ahora solo se posiciona, no se asigna width aquí
            self.dropdown.place(x=x, y=y)

    def _select(self, value):
        self.delete(0, "end")
        self.insert(0, value)
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None
