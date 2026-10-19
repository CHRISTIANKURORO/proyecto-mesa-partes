# utilidades.py
import os

ARCHIVO = "datos/reservas.txt"

def asegurar_archivo():
    """Crea la carpeta y el archivo si no existen."""
    os.makedirs("datos", exist_ok=True)
    if not os.path.exists(ARCHIVO):
        open(ARCHIVO, "w", encoding="utf-8").close()

def cargar_reservas():
    """Lee el archivo y devuelve una lista de diccionarios."""
    asegurar_archivo()
    reservas = []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea == "":
                continue
            campos = linea.split(";")
            if len(campos) == 10:
                reservas.append({
                    "codigo": campos[0],
                    "nombre": campos[1],
                    "tipo_doc": campos[2],
                    "num_doc": campos[3],
                    "entidad": campos[4],
                    "odpe": campos[5],
                    "direccion": campos[6],
                    "tramite": campos[7],
                    "fecha": campos[8],
                    "hora": campos[9],
                })
    return reservas

def guardar_reserva(reserva):
    """Agrega una reserva al archivo (una línea por reserva)."""
    asegurar_archivo()
    with open(ARCHIVO, "a", encoding="utf-8") as f:
        linea = ";".join([
            reserva["codigo"], reserva["nombre"], reserva["tipo_doc"],
            reserva["num_doc"], reserva["entidad"], reserva["odpe"],
            reserva["direccion"], reserva["tramite"], reserva["fecha"],
            reserva["hora"]
        ])
        f.write(linea + "\n")

def contar_reservas_por_fecha(fecha_buscada):
    """Cuenta cuántas reservas hay en una fecha específica."""
    reservas = cargar_reservas()
    return sum(1 for r in reservas if r["fecha"] == fecha_buscada)

def contar_tickets_por_letra(letra):
    """Cuenta cuántos tickets empiezan con 'C' o 'R'."""
    reservas = cargar_reservas()
    return sum(1 for r in reservas if r["codigo"].startswith(letra))

def formatear_dos_digitos(numero):
    """Devuelve '01', '02', ..., '10', etc."""
    return f"{numero:02d}"

def obtener_hora_por_turno(numero_turno):
    """Turno 1 -> 08:00, turno 2 -> 08:30, ... turno 16 -> 16:30."""
    horas = [
        "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
        "11:00", "11:30", "12:00", "12:30",
        "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
    ]
    if 1 <= numero_turno <= 16:
        return horas[numero_turno - 1]
    return ""

def fecha_valida(fecha):
    """Valida formato dd/mm/aaaa (10 caracteres, barras en pos 2 y 5)."""
    if len(fecha) != 10:
        return False
    if fecha[2] != "/" or fecha[5] != "/":
        return False
    partes = fecha.split("/")
    return all(p.isdigit() for p in partes)