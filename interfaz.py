import tkinter as tk
from tkinter import ttk, messagebox
from utilidades import cargar_reservas, contar_reservas_por_fecha, contar_tickets_por_letra, formatear_dos_digitos, obtener_hora_por_turno, fecha_valida, guardar_reserva
class AplicacionONPE:
    def __init__(self, root):
        self.root = root
        self.root.title("ONPE - Mesa de Partes")
        self.root.geometry("600x200") # Tamaño aproximado de la ventana 1
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
        self.root.withdraw()
        
        self.ventana_form = tk.Toplevel()
        self.ventana_form.title("Formulario - Ticket Mesa de Partes")
        self.ventana_form.geometry("650x400")
        self.ventana_form.configure(bg="white")

        # --- SECCIÓN 1: IDENTIFICACIÓN ---
        frame_ident = tk.Frame(self.ventana_form, bg="white")
        frame_ident.pack(fill="x", padx=15, pady=10)

        # Fila 1: Tipo doc, Nombres, Entidad
        self.combo_tipo = ttk.Combobox(frame_ident, values=["DNI", "RUC"], state="readonly", width=8)
        self.combo_tipo.set("DNI")
        self.combo_tipo.grid(row=0, column=0, padx=5, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.cambiar_tipo_doc)

        tk.Label(frame_ident, text="Nombres y apellidos:", bg="white").grid(row=1, column=1, sticky="w", padx=5)
        self.entry_nombre = tk.Entry(frame_ident, width=30, relief="solid", bd=1)
        self.entry_nombre.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_ident, text="Entidad si escoge RUC:", bg="white").grid(row=1, column=2, sticky="w", padx=5)
        self.entry_entidad = tk.Entry(frame_ident, width=30, relief="solid", bd=1, state="disabled")
        self.entry_entidad.grid(row=2, column=2, padx=5, pady=2)

        # --- SECCIÓN 2: ODPE ---
        frame_odpe = tk.Frame(self.ventana_form, bg="white")
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
        frame_tram = tk.Frame(self.ventana_form, bg="white")
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

        # --- SECCIÓN 4: FECHA Y HORA ---
        frame_fecha = tk.Frame(self.ventana_form, bg="white")
        frame_fecha.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_fecha, text="Fecha (dd/mm/aaaa)", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_fecha = tk.Entry(frame_fecha, width=15, relief="solid", bd=1)
        self.entry_fecha.grid(row=1, column=0, padx=5, pady=2)

        tk.Label(frame_fecha, text="Horario de atención 8 am – 1 pm y 2 pm - 5 pm,\nsi están reservados en el día elegido deberá reservar otro", 
                 bg="white", font=("Arial", 8)).grid(row=1, column=1, padx=10)
        
        self.entry_hora = tk.Entry(frame_fecha, width=15, relief="solid", bd=1, state="readonly")
        self.entry_hora.grid(row=1, column=2, padx=5)

        # --- BOTONES ---
        frame_botones = tk.Frame(self.ventana_form, bg="white")
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="Generar Ticket", bg="#4a90e2", fg="white", 
                  font=("Arial", 10, "bold"), padx=10, pady=5, command=self.generar_ticket).pack(side="left", padx=10)
        
        tk.Button(frame_botones, text="Volver al inicio", command=self.volver_al_inicio_form).pack(side="left", padx=10)

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

    def volver_al_inicio_form(self):
        self.ventana_form.destroy()
        self.root.deiconify()

    def generar_ticket(self):
        # 1. Recolectar datos de la interfaz
        tipo_doc = self.combo_tipo.get()
        nombre = self.entry_nombre.get().strip()
        num_doc = "00000000" # Simulado por ahora
        entidad = self.entry_entidad.get().strip()
        odpe = self.combo_odpe.get()
        direccion = self.entry_direccion.get()
        tramite = self.combo_tramite.get()
        fecha = self.entry_fecha.get().strip()

        # 2. Validaciones básicas
        if not nombre or not odpe or not tramite or not fecha:
            messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios.")
            return

        if not fecha_valida(fecha):
            messagebox.showerror("Error", "Formato de fecha inválido. Use dd/mm/aaaa.")
            return

        if tipo_doc == "RUC" and not entidad:
            messagebox.showerror("Error", "Si elige RUC, debe ingresar el nombre de la entidad.")
            return

        # 3. Lógica de cupos (usando utilidades.py)
        cantidad_reservas = contar_reservas_por_fecha(fecha)
        if cantidad_reservas >= 16:
            messagebox.showerror("Error", "No hay cupos disponibles para este día. Registre otro día.")
            return

        hora_asignada = obtener_hora_por_turno(cantidad_reservas + 1)
        
        # 4. Generar Código (C01, R01, etc.)
        letra = "C" if tipo_doc == "DNI" else "R"
        cantidad_tickets = contar_tickets_por_letra(letra)
        codigo_ticket = letra + formatear_dos_digitos(cantidad_tickets + 1)

        # 5. Crear el diccionario de la reserva y guardarlo
        reserva = {
            "codigo": codigo_ticket,
            "nombre": nombre,
            "tipo_doc": tipo_doc,
            "num_doc": "00000000", # Simulado por ahora
            "entidad": entidad if tipo_doc == "RUC" else "No aplica",
            "odpe": odpe,
            "direccion": direccion,
            "tramite": tramite,
            "fecha": fecha,
            "hora": hora_asignada
        }
        
        guardar_reserva(reserva)
        # 6. Cerrar formulario y abrir ventana del ticket
        self.ventana_form.destroy()
        self.abrir_ventana_ticket(reserva)

    def abrir_ventana_ticket(self, reserva):
        self.ventana_ticket = tk.Toplevel()
        self.ventana_ticket.title("Ticket Generado")
        self.ventana_ticket.geometry("450x350")
        self.ventana_ticket.configure(bg="white")

        # Diseño del Ticket
        tk.Label(self.ventana_ticket, text="ONPE - TICKET DE ATENCIÓN", 
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        frame_info = tk.Frame(self.ventana_ticket, bg="white", bd=2, relief="groove")
        frame_info.pack(padx=20, pady=10, fill="both", expand=True)

        # Datos del ticket
        tk.Label(frame_info, text=f"Código: {reserva['codigo']}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)
        tk.Label(frame_info, text=f"Solicitante: {reserva['nombre']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"Fecha y Hora: {reserva['fecha']} - {reserva['hora']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"Trámite: {reserva['tramite']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"ODPE: {reserva['odpe']}", bg="white").pack(anchor="w", padx=10)
        tk.Label(frame_info, text=f"Dirección: {reserva['direccion']}", bg="white").pack(anchor="w", padx=10)

        # Botones
        frame_btn = tk.Frame(self.ventana_ticket, bg="white")
        frame_btn.pack(pady=10)
        
        tk.Button(frame_btn, text="Volver al inicio", command=self.volver_desde_ticket).pack(side="left", padx=10)

    def volver_desde_ticket(self):
        self.ventana_ticket.destroy()
        self.root.deiconify() # Vuelve a mostrar la ventana principal
    def abrir_sgd(self):
        self.root.withdraw()
        
        self.ventana_sgd = tk.Toplevel()
        self.ventana_sgd.title("SGD - Recepción de Documentos")
        self.ventana_sgd.geometry("850x400")
        self.ventana_sgd.configure(bg="white")

        tk.Label(self.ventana_sgd, text="Registro de Reservas - Tickets", 
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame_tabla = tk.Frame(self.ventana_sgd)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("Codigo", "Nombre", "TipoDoc", "ODPE", "Tramite", "Fecha", "Hora")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("Codigo", text="Código")
        self.tabla.column("Codigo", width=70, anchor="center")
        
        self.tabla.heading("Nombre", text="Nombre / Entidad")
        self.tabla.column("Nombre", width=180)
        
        self.tabla.heading("TipoDoc", text="Tipo Doc.")
        self.tabla.column("TipoDoc", width=80, anchor="center")
        
        self.tabla.heading("ODPE", text="ODPE")
        self.tabla.column("ODPE", width=130)
        
        self.tabla.heading("Tramite", text="Trámite")
        self.tabla.column("Tramite", width=180)
        
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.column("Fecha", width=80, anchor="center")
        
        self.tabla.heading("Hora", text="Hora")
        self.tabla.column("Hora", width=60, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.cargar_datos_tabla()

        tk.Button(self.ventana_sgd, text="Volver al inicio", 
                  command=self.volver_desde_sgd).pack(pady=10)

    def cargar_datos_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        reservas = cargar_reservas()
        if not reservas:
            self.tabla.insert("", "end", values=("No hay reservas", "", "", "", "", "", ""))
        else:
            for r in reservas:
                nombre_mostrar = r['nombre'] if r['tipo_doc'] == 'DNI' else f"{r['entidad']} - {r['nombre']}"
                self.tabla.insert("", "end", values=(
                    r['codigo'], nombre_mostrar, r['tipo_doc'], 
                    r['odpe'], r['tramite'], r['fecha'], r['hora']
                ))

    def volver_desde_sgd(self):
        self.ventana_sgd.destroy()
        self.root.deiconify()
# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionONPE(root)
    root.mainloop()