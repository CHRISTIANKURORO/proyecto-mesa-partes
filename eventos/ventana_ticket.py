import tkinter as tk

class VentanaTicket:
    def __init__(self, root, ventana_principal, reserva):
        self.root = root
        self.ventana_principal = ventana_principal
        self.ventana = tk.Toplevel()
        self.ventana.title("Ticket Generado")
        self.ventana.geometry("450x350")
        self.ventana.configure(bg="white")

        # Título
        tk.Label(self.ventana, text="ONPE - TICKET DE ATENCIÓN", 
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        # Cuadro de información
        frame_info = tk.Frame(self.ventana, bg="white", bd=2, relief="groove")
        frame_info.pack(padx=20, pady=10, fill="both", expand=True)

        # Datos del ticket
        tk.Label(frame_info, text=f"Código: {reserva['codigo']}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)
        tk.Label(frame_info, text=f"Solicitante: {reserva['nombre']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"Fecha y Hora: {reserva['fecha']} - {reserva['hora']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"Trámite: {reserva['tramite']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"ODPE: {reserva['odpe']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"Dirección: {reserva['direccion']}", bg="white").pack(anchor="w", padx=10)

        # Botón para volver
        tk.Button(self.ventana, text="Volver al inicio", command=self.volver).pack(pady=10)

    def volver(self):
        self.ventana.destroy()
        self.root.deiconify()  # Vuelve a mostrar la ventana principal