import customtkinter as ctk 
from frontend.config import COLORS

class AppSidebar(ctk.CTkFrame): 
    def __init__(self, master, on_navigate): 
        super().__init__(master, width=200, corner_radius=0) 
        self.on_navigate = on_navigate 
        self.buttons = {} 
        title_label = ctk.CTkLabel(self, text="Menú", font=ctk.CTkFont(size=20, weight="bold")) 
        title_label.pack(padx=20, pady=(20, 10)) 
        nav_items = [("Productos", "products"), ("Clientes", "customers"), ("Ventas", "sales")] 
        for text, key in nav_items: 
            btn = ctk.CTkButton( 
            self, 
            text=text, 
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), 
            anchor="w", 
            command=lambda k=key: self.on_navigate(k) 
                    ) 
            btn.pack(fill="x", padx=10, pady=5) 
            self.buttons[key] = btn 

    def set_active_button(self, view_name: str): 
        for key, btn in self.buttons.items(): 
            if key == view_name: 
                btn.configure(fg_color=COLORS["primary"]) 
            else: 
                btn.configure(fg_color="transparent") 