import tkinter as tk
from eventos.ventana_formulario import VentanaFormulario
from eventos.ventana_sgd import VentanaSGD

class AplicacionONPE:
    def __init__(self, root):
        self.root = root
        self.root.title("ONPE - Mesa de Partes")
        self.root.geometry("600x200")
        self.root.configure(bg="white")

        # --- BARRA SUPERIOR (URL) ---
        self.frame_url = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        self.frame_url.pack(fill="x", padx=10, pady=(10, 0))
        
        self.lbl_url = tk.Label(self.frame_url, text="https://www.gob.pe/onpe", 
                                fg="blue", bg="white", font=("Arial", 10))
        self.lbl_url.pack(side="left", padx=5, pady=2)

        # --- BARRA DE MENÚ (Home, SGD, Consultorías, Ticket) ---
        self.frame_menu = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        self.frame_menu.pack(fill="x", padx=10, pady=5)

        # Textos estáticos
        tk.Label(self.frame_menu, text="Home", bg="white").pack(side="left", padx=10, pady=5)
        
        # Botón SGD (Navegación a Ventana 3)
        self.btn_sgd = tk.Button(self.frame_menu, text="SGD", bg="white", relief="flat", 
                                 command=self.abrir_sgd)
        self.btn_sgd.pack(side="left", padx=10)

        tk.Label(self.frame_menu, text="Consultorías", bg="white").pack(side="left", padx=10, pady=5)

        # Botón Ticket Mesa de Partes (Navegación a Ventana 2)
        self.btn_ticket = tk.Button(self.frame_menu, text="Ticket mesa de partes", 
                                    bg="#e0e0e0", relief="solid", bd=1,
                                    command=self.abrir_formulario)
        self.btn_ticket.pack(side="right", padx=10, pady=2)

    # --- FUNCIONES DE NAVEGACIÓN ---
    def abrir_formulario(self):
        self.root.withdraw()  # Oculta la ventana principal
        VentanaFormulario(self.root, self)  # Llama a la ventana del formulario

    def abrir_sgd(self):
        self.root.withdraw()  # Oculta la ventana principal
        VentanaSGD(self.root, self)  # Llama a la ventana del SGD

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionONPE(root)
    root.mainloop()