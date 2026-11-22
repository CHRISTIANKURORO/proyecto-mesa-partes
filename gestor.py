# gestor.py (Ubicado en la raíz)
from modelo.utilidades import (
    fecha_valida, contar_reservas_por_fecha, contar_tickets_por_letra,
    formatear_dos_digitos, obtener_hora_por_turno, guardar_reserva, cargar_reservas
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
    
    # 4. Convertir nombre a mayúsculas
    datos["nombre"] = datos["nombre"].upper()
    # (Si es RUC, también la entidad)
    if tipo_doc == "RUC" and datos.get("entidad"):
        datos["entidad"] = datos["entidad"].upper()

def obtener_reservas_sgd():
    """Devuelve la lista de reservas para que el SGD la muestre."""
    return cargar_reservas()