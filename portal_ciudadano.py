# portal_ciudadano.py
from utilidades import (
    cargar_reservas, guardar_reserva, contar_reservas_por_fecha,
    contar_tickets_por_letra, formatear_dos_digitos,
    obtener_hora_por_turno, fecha_valida
)

def identificar_usuario():
    print("\n--- IDENTIFICACIÓN DEL USUARIO ---")
    print("1. DNI")
    print("2. RUC")
    opcion = input("Seleccione una opción: ")

    while opcion not in ("1", "2"):
        print("Opción inválida. Seleccione 1 o 2.")
        opcion = input("Seleccione una opción: ")

    if opcion == "1":
        tipo_doc = "DNI"
        num_doc = input("Ingrese su DNI: ")
        nombre = input("Ingrese su nombre completo: ")
        letra = "C"
        entidad = "No aplica"
    else:
        tipo_doc = "RUC"
        num_doc = input("Ingrese su RUC: ")
        nombre = input("Ingrese su nombre completo: ")
        entidad = input("Ingrese el nombre de la entidad (ONPE, JNE, JEE, ODPE u otra): ")
        letra = "R"

    return tipo_doc, num_doc, nombre, entidad, letra

def seleccionar_odpe():
    print("\n--- ESCOJA SU ODPE PARA LA ATENCIÓN ---")
    print("1. ODPE Independencia")
    print("2. ODPE Comas")
    print("3. ODPE Los Olivos")
    print("4. ODPE San Martín")
    opcion = input("Seleccione una opción: ")

    while opcion not in ("1", "2", "3", "4"):
        print("Opción inválida. Seleccione una ODPE del menú.")
        opcion = input("Seleccione una opción: ")

    if opcion == "1":
        odpe, direccion = "ODPE Independencia", "AV. TUPAC AMARU 1234"
    elif opcion == "2":
        odpe, direccion = "ODPE Comas", "AV. TUPAC AMARU 65432"
    elif opcion == "3":
        odpe, direccion = "ODPE Los Olivos", "AV. LOS ALISOS 1234"
    else:
        odpe, direccion = "ODPE San Martín", "AV. CALLAO 1234"

    print(f"{odpe} SE UBICA EN {direccion}")
    return odpe, direccion

def seleccionar_tramite():
    print("\n--- QUÉ DESEA TRAMITAR ---")
    print("1. Entrega de documentos")
    print("2. Tramitación de excusas y justificaciones")
    print("3. Registro y control de correspondencia")
    print("4. Derivación interna")
    print("5. Información y orientación al usuario")
    opcion = input("Seleccione una opción: ")

    while opcion not in ("1", "2", "3", "4", "5"):
        print("Opción inválida. Seleccione una opción del menú.")
        opcion = input("Seleccione una opción: ")

    descripciones = {
        "1": ("Entrega de documentos",
              "Recibe cartas, solicitudes, oficios y expedientes presentados por ciudadanos, personeros de agrupaciones políticas, autoridades o instituciones públicas."),
        "2": ("Tramitación de excusas y justificaciones",
              "Recibe solicitudes de ciudadanos sorteados como miembros de mesa que presentan excusa o dispensa, con sus documentos probatorios."),
        "3": ("Registro y control de correspondencia",
              "Asigna número de expediente, fecha y hora de ingreso para facilitar el seguimiento y la trazabilidad."),
        "4": ("Derivación interna",
              "Remite los documentos recibidos a las áreas correspondientes de la ODPE para su atención."),
        "5": ("Información y orientación al usuario",
              "Brinda información básica sobre los requisitos de presentación de expedientes y el estado de los mismos."),
    }
    tramite, descripcion = descripciones[opcion]
    print(f"INFO: {descripcion}")
    return tramite

def seleccionar_fecha_y_hora():
    print("\n--- ESCOJA LA FECHA ---")
    print("Horario referencial: 8:00 a. m. - 1:00 p. m. y 2:00 p. m. - 5:00 p. m.")
    print("La simulación permite hasta 16 reservas por fecha, con intervalos de 30 minutos.")
    print("Si la fecha tiene 16 reservas, deberá elegir otro día.")

    hora_asignada = ""
    fecha = ""
    while hora_asignada == "":
        fecha = input("Ingrese día/mes/año (solo números, ej. 01/01/2026): ")
        if not fecha_valida(fecha):
            print("Formato inválido. Use dd/mm/aaaa.")
            continue
        cantidad = contar_reservas_por_fecha(fecha)
        if cantidad >= 16:
            print("Error, registre otro día")
        else:
            hora_asignada = obtener_hora_por_turno(cantidad + 1)

    print(f"Hora asignada: {hora_asignada}")
    return fecha, hora_asignada

def generar_ticket(tipo_doc, num_doc, nombre, entidad, letra, odpe, direccion, tramite, fecha, hora):
    cantidad_codigo = contar_tickets_por_letra(letra)
    numero_ticket = cantidad_codigo + 1
    codigo_ticket = letra + formatear_dos_digitos(numero_ticket)

    reserva = {
        "codigo": codigo_ticket,
        "nombre": nombre,
        "tipo_doc": tipo_doc,
        "num_doc": num_doc,
        "entidad": entidad,
        "odpe": odpe,
        "direccion": direccion,
        "tramite": tramite,
        "fecha": fecha,
        "hora": hora,
    }
    guardar_reserva(reserva)

    print("\n==============================================")
    print("           TICKET DE RESERVA - ONPE")
    print("==============================================")
    print(f"Código: {codigo_ticket}")
    print(f"Fecha: {fecha}")
    print(f"Hora: {hora}")
    print(f"Trámite: {tramite}")
    print(f"ODPE: {odpe}")
    print("==============================================")
    print("[SGD] Reserva guardada en el registro compartido.")
    print("[SGD] El personal de Mesa de Partes podrá visualizarla.")

def ejecutar_portal():
    print("\n=== PORTAL WEB - TICKET MESA DE PARTES ===")
    tipo_doc, num_doc, nombre, entidad, letra = identificar_usuario()
    odpe, direccion = seleccionar_odpe()
    tramite = seleccionar_tramite()
    fecha, hora = seleccionar_fecha_y_hora()
    generar_ticket(tipo_doc, num_doc, nombre, entidad, letra,
                   odpe, direccion, tramite, fecha, hora)