from modelo.utilidades import (
    fecha_valida, contar_reservas_por_fecha, contar_tickets_por_letra,
    formatear_dos_digitos, guardar_reserva, cargar_reservas
)

def procesar_ticket(datos):
    # 1. Validar campos vacíos
    if not datos.get("nombre") or not datos.get("fecha") or not datos.get("num_doc"):
        return {"exito": False, "mensaje": "Complete los campos obligatorios."}
    
    # 2. Validar DNI/RUC
    num_doc = datos["num_doc"]
    tipo_doc = datos["tipo_doc"]
    if not num_doc.isdigit() or len(num_doc) != (8 if tipo_doc == "DNI" else 11):
        return {"exito": False, "mensaje": "El DNI debe tener 8 dígitos y el RUC 11 dígitos."}
    
    # 3. Validar fecha
    if not fecha_valida(datos["fecha"]):
        return {"exito": False, "mensaje": "Formato de fecha inválido."}
    
    # 4. Validar HORARIO seleccionado
    hora_seleccionada = datos.get("hora")
    if not hora_seleccionada:
        return {"exito": False, "mensaje": "Seleccione un horario de atención."}
    
    # 5. Convertir a formato 24h
    horarios_24h = {
        "8 AM": "08:00", "9 AM": "09:00", "10 AM": "10:00",
        "11 AM": "11:00", "12 PM": "12:00", "2 PM": "14:00",
        "3 PM": "15:00", "4 PM": "16:00"
    }
    hora_24h = horarios_24h.get(hora_seleccionada, "")
    
    # 6. Verificar que ese horario no esté ocupado para esa fecha
    reservas = cargar_reservas()
    if any(r["fecha"] == datos["fecha"] and r["hora"] == hora_24h for r in reservas):
        return {"exito": False, "mensaje": "Este horario ya está reservado. Seleccione otro."}
    
    # 7. Generar código y nombre en mayúsculas
    letra = "C" if tipo_doc == "DNI" else "R"
    num_ticket = contar_tickets_por_letra(letra) + 1
    codigo = letra + formatear_dos_digitos(num_ticket)
    
    datos["nombre"] = datos["nombre"].upper()
    if tipo_doc == "RUC" and datos.get("entidad"):
        datos["entidad"] = datos["entidad"].upper()
    
    # 8. Crear el diccionario y guardarlo
    reserva = {
        "codigo": codigo,
        "nombre": datos["nombre"],
        "tipo_doc": tipo_doc,
        "num_doc": num_doc,
        "entidad": datos.get("entidad", "No aplica"),
        "odpe": datos.get("odpe", ""),
        "direccion": datos.get("direccion", ""),
        "tramite": datos.get("tramite", ""),
        "fecha": datos["fecha"],
        "hora": hora_24h  # <-- Guardamos en formato 24h
    }
    
    guardar_reserva(reserva)
    
    return {"exito": True, "mensaje": "Ticket generado con éxito", "ticket": reserva}

def obtener_reservas_sgd():
    """Devuelve la lista de reservas para que el SGD la muestre."""
    return cargar_reservas()