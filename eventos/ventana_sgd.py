import tkinter as tk
from tkinter import ttk
from gestor import obtener_reservas_sgd

class VentanaSGD:
    def __init__(self, root, ventana_principal):
        self.root = root
        self.ventana_principal = ventana_principal
        
        self.ventana = tk.Toplevel()
        self.ventana.title("SGD - Recepción de Documentos")
        self.ventana.geometry("850x400")
        self.ventana.configure(bg="white")

        # Título
        tk.Label(self.ventana, text="Registro de Reservas - Tickets", 
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Contenedor de la tabla
        frame_tabla = tk.Frame(self.ventana)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("Codigo", "Nombre", "TipoDoc", "ODPE", "Tramite", "Fecha", "Hora")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        # Configurar columnas
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

        # Barra de desplazamiento
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Cargar datos desde el gestor
        self.cargar_tabla()

        # Botón para volver
        tk.Button(self.ventana, text="Volver al inicio", command=self.volver).pack(pady=10)

    def cargar_tabla(self):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        reservas = obtener_reservas_sgd()
        if not reservas:
            self.tabla.insert("", "end", values=("No hay reservas", "", "", "", "", "", ""))
        else:
            for r in reservas:
                nombre_mostrar = r['nombre'] if r['tipo_doc'] == 'DNI' else f"{r['entidad']} - {r['nombre']}"
                self.tabla.insert("", "end", values=(
                    r['codigo'], nombre_mostrar, r['tipo_doc'], 
                    r['odpe'], r['tramite'], r['fecha'], r['hora']
                ))

    def volver(self):
        self.ventana.destroy()
        self.root.deiconify()