# gestor.py (Ubicado en la raíz)
from modelo.utilidades import (
    fecha_valida, contar_reservas_por_fecha, contar_tickets_por_letra,
    formatear_dos_digitos, obtener_hora_por_turno, guardar_reserva, cargar_reservas
)

def procesar_ticket(datos):
    """
    Recibe un diccionario con los datos del formulario.
    Valida, calcula y guarda. Devuelve un diccionario con el resultado.
    """
    # 1. Validaciones básicas
    if not datos.get("nombre") or not datos.get("fecha") or not datos.get("num_doc"):
        return {"exito": False, "mensaje": "Complete los campos obligatorios (Nombre, Documento, Fecha)."}
    
    if not fecha_valida(datos["fecha"]):
        return {"exito": False, "mensaje": "Formato de fecha inválido. Use dd/mm/aaaa."}
    
    # 2. Control de cupos
    cantidad = contar_reservas_por_fecha(datos["fecha"])
    if cantidad >= 16:
        return {"exito": False, "mensaje": "No hay cupos disponibles para este día."}
    
    # 3. Asignar hora y generar código
    hora = obtener_hora_por_turno(cantidad + 1)
    letra = "C" if datos["tipo_doc"] == "DNI" else "R"
    num_ticket = contar_tickets_por_letra(letra) + 1
    codigo = letra + formatear_dos_digitos(num_ticket)
    
    # 4. Crear el diccionario final del ticket y guardarlo
    reserva = {
        "codigo": codigo,
        "nombre": datos["nombre"],
        "tipo_doc": datos["tipo_doc"],
        "num_doc": datos["num_doc"],
        "entidad": datos.get("entidad", "No aplica"),
        "odpe": datos.get("odpe", ""),
        "direccion": datos.get("direccion", ""),
        "tramite": datos.get("tramite", ""),
        "fecha": datos["fecha"],
        "hora": hora
    }
    
    guardar_reserva(reserva)
    
    return {"exito": True, "mensaje": "Ticket generado con éxito", "ticket": reserva}

def obtener_reservas_sgd():
    """Devuelve la lista de reservas para que el SGD la muestre."""
    return cargar_reservas()