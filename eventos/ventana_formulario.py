import tkinter as tk
from tkinter import ttk, messagebox
from gestor import procesar_ticket

class VentanaFormulario:
    def __init__(self, root, ventana_principal):
        self.root = root
        self.ventana_principal = ventana_principal
        
        self.ventana = tk.Toplevel()
        self.ventana.title("Formulario - Ticket Mesa de Partes")
        self.ventana.geometry("650x400")
        self.ventana.configure(bg="white")

        # --- SECCIÓN 1: IDENTIFICACIÓN ---
        frame_ident = tk.Frame(self.ventana, bg="white")
        frame_ident.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_ident, text="Tipo Doc.", bg="white").grid(row=0, column=0, padx=5, sticky="w")
        self.combo_tipo = ttk.Combobox(frame_ident, values=["DNI", "RUC"], state="readonly", width=8)
        self.combo_tipo.set("DNI")
        self.combo_tipo.grid(row=1, column=0, padx=5, pady=2)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.cambiar_tipo_doc)

        tk.Label(frame_ident, text="Número de Doc:", bg="white").grid(row=0, column=1, padx=5, sticky="w")
        self.entry_dni = tk.Entry(frame_ident, width=15, relief="solid", bd=1)
        self.entry_dni.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_ident, text="Nombres y apellidos:", bg="white").grid(row=0, column=2, padx=5, sticky="w")
        self.entry_nombre = tk.Entry(frame_ident, width=25, relief="solid", bd=1)
        self.entry_nombre.grid(row=1, column=2, padx=5, pady=2)

        tk.Label(frame_ident, text="Entidad si escoge RUC:", bg="white").grid(row=0, column=3, padx=5, sticky="w")
        self.entry_entidad = tk.Entry(frame_ident, width=25, relief="solid", bd=1, state="disabled")
        self.entry_entidad.grid(row=1, column=3, padx=5, pady=2)

        # --- SECCIÓN 2: ODPE ---
        frame_odpe = tk.Frame(self.ventana, bg="white")
        frame_odpe.pack(fill="x", padx=15, pady=5)
        
        tk.Label(frame_odpe, text="Escoja la ODPE para su atención", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(frame_odpe, text="La ubicación es:", bg="white").grid(row=0, column=1, sticky="w", padx=5)

        self.combo_odpe = ttk.Combobox(frame_odpe, values=[
            "ODPE Independencia", "ODPE Comas", "ODPE Los Olivos", "ODPE San Martín"
        ], state="readonly", width=25)
        self.combo_odpe.grid(row=1, column=0, padx=5, pady=2)
        self.combo_odpe.bind("<<ComboboxSelected>>", self.actualizar_direccion)

        self.entry_direccion = tk.Entry(frame_odpe, width=40, relief="solid", bd=1, state="readonly")
        self.entry_direccion.grid(row=1, column=1, padx=5, pady=2)

        # --- SECCIÓN 3: TRÁMITE ---
        frame_tram = tk.Frame(self.ventana, bg="white")
        frame_tram.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_tram, text="Tipo de trámite", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(frame_tram, text="Información:", bg="white").grid(row=0, column=1, sticky="w", padx=5)

        self.combo_tramite = ttk.Combobox(frame_tram, values=[
            "1. Entrega de documentos", "2. Tramitación de excusas", 
            "3. Registro y control", "4. Derivación interna", "5. Información y orientación"
        ], state="readonly", width=25)
        self.combo_tramite.grid(row=1, column=0, padx=5, pady=2)
        self.combo_tramite.bind("<<ComboboxSelected>>", self.actualizar_info_tramite)

        self.entry_info = tk.Entry(frame_tram, width=45, relief="solid", bd=1, state="readonly")
        self.entry_info.grid(row=1, column=1, padx=5, pady=2)

                # --- SECCIÓN 4: FECHA Y HORA (MEJORADA) ---
        frame_fecha = tk.Frame(self.ventana, bg="white")
        frame_fecha.pack(fill="x", padx=15, pady=10)

        # Columna 0: Fecha
        tk.Label(frame_fecha, text="Fecha (dd/mm/aaaa)", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_fecha = tk.Entry(frame_fecha, width=15, relief="solid", bd=1)
        self.entry_fecha.grid(row=1, column=0, padx=5, pady=2)

        # Columna 1: Horarios de atención (3 Labels bonitos)
        tk.Label(frame_fecha, text="HORARIOS DE ATENCIÓN:", bg="white", 
                 font=("Arial", 9, "bold")).grid(row=0, column=1, padx=10)
        tk.Label(frame_fecha, text="8 AM - 1 PM\n2 PM - 5 PM", 
                 bg="white", font=("Arial", 9)).grid(row=1, column=1, padx=10)
        tk.Label(frame_fecha, text="Si están reservados, elija otro.", 
                 bg="white", font=("Arial", 8)).grid(row=2, column=1, padx=10)

        # Columna 2: Combobox para seleccionar hora
        tk.Label(frame_fecha, text="HORARIO:", bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.combo_hora = ttk.Combobox(frame_fecha, values=[
            "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", 
            "2 PM", "3 PM", "4 PM"
        ], state="readonly", width=13)
        self.combo_hora.grid(row=1, column=2, padx=5, pady=2)
        self.combo_hora.set("8 AM")  # <--- ESTO ES LO QUE FALTA

        # --- BOTONES ---
        frame_botones = tk.Frame(self.ventana, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="Generar Ticket", bg="#4a90e2", fg="white", 
                  font=("Arial", 10, "bold"), padx=10, pady=5, command=self.generar).pack(side="left", padx=10)
        
        tk.Button(frame_botones, text="Volver al inicio", command=self.volver).pack(side="left", padx=10)

    # --- FUNCIONES DE APOYO VISUAL ---
    def cambiar_tipo_doc(self, event):
        if self.combo_tipo.get() == "DNI":
            self.entry_entidad.config(state="normal")
            self.entry_entidad.delete(0, tk.END)
            self.entry_entidad.config(state="disabled")
        else:
            self.entry_entidad.config(state="normal")

    def actualizar_direccion(self, event):
        direcciones = {
            "ODPE Independencia": "AV. TUPAC AMARU 1234",
            "ODPE Comas": "AV. TUPAC AMARU 65432",
            "ODPE Los Olivos": "AV. LOS ALISOS 1234",
            "ODPE San Martín": "AV. CALLAO 1234"
        }
        seleccion = self.combo_odpe.get()
        self.entry_direccion.config(state="normal")
        self.entry_direccion.delete(0, tk.END)
        self.entry_direccion.insert(0, direcciones.get(seleccion, ""))
        self.entry_direccion.config(state="readonly")

    def actualizar_info_tramite(self, event):
        info = {
            "1. Entrega de documentos": "Recibe cartas, solicitudes, oficios y expedientes.",
            "2. Tramitación de excusas": "Recibe solicitudes de miembros de mesa.",
            "3. Registro y control": "Asigna número de expediente y trazabilidad.",
            "4. Derivación interna": "Remite documentos a áreas correspondientes.",
            "5. Información y orientación": "Brinda información básica al usuario."
        }
        seleccion = self.combo_tramite.get()
        self.entry_info.config(state="normal")
        self.entry_info.delete(0, tk.END)
        self.entry_info.insert(0, info.get(seleccion, ""))
        self.entry_info.config(state="readonly")

    def generar(self):
        # Recolectar datos
        datos = {
            "tipo_doc": self.combo_tipo.get(),
            "nombre": self.entry_nombre.get().strip(),
            "num_doc": self.entry_dni.get().strip(),
            "entidad": self.entry_entidad.get().strip(),
            "odpe": self.combo_odpe.get(),
            "direccion": self.entry_direccion.get(),
            "tramite": self.combo_tramite.get(),
            "fecha": self.entry_fecha.get().strip(),
            "hora": self.combo_hora.get()  # <-- AÑADIDO: "8 AM", "9 AM", etc.
        }
        
        # Llamar al gestor
        resultado = procesar_ticket(datos)
        
        if resultado["exito"]:
            self.ventana.destroy()
            from eventos.ventana_ticket import VentanaTicket
            VentanaTicket(self.root, self.ventana_principal, resultado["ticket"])
        else:
            messagebox.showerror("Error", resultado["mensaje"])