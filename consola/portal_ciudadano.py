from gestor import procesar_ticket
from modelo.utilidades import fecha_valida

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
        entidad = "No aplica"
    else:
        tipo_doc = "RUC"
        num_doc = input("Ingrese su RUC: ")
        nombre = input("Ingrese su nombre completo: ")
        entidad = input("Ingrese el nombre de la entidad (ONPE, JNE, JEE, ODPE u otra): ")
    return tipo_doc, num_doc, nombre, entidad

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
        "1": "Entrega de documentos",
        "2": "Tramitación de excusas y justificaciones",
        "3": "Registro y control de correspondencia",
        "4": "Derivación interna",
        "5": "Información y orientación al usuario"
    }
    return descripciones[opcion]

def seleccionar_fecha():
    print("\n--- ESCOJA LA FECHA ---")
    print("Horario referencial: 8:00 a. m. - 1:00 p. m. y 2:00 p. m. - 5:00 p. m.")
    print("La simulación permite hasta 16 reservas por fecha.")
    fecha = input("Ingrese día/mes/año (solo números, ej. 01/01/2026): ")
    return fecha

def ejecutar_portal():
    print("\n=== PORTAL WEB - TICKET MESA DE PARTES ===")
    
    # 1. Recolectar datos (solo preguntas, sin lógica)
    tipo_doc, num_doc, nombre, entidad = identificar_usuario()
    odpe, direccion = seleccionar_odpe()
    tramite = seleccionar_tramite()
    fecha = seleccionar_fecha()
    
    # 2. Crear el diccionario y pasarlo al gestor
    datos = {
        "tipo_doc": tipo_doc,
        "nombre": nombre,
        "num_doc": num_doc,
        "entidad": entidad,
        "odpe": odpe,
        "direccion": direccion,
        "tramite": tramite,
        "fecha": fecha
    }
    
    # 3. El gestor lo gestiona (validar, contar cupos, guardar)
    resultado = procesar_ticket(datos)
    
    # 4. Mostrar el resultado
    if resultado["exito"]:
        t = resultado["ticket"]
        print("\n==============================================")
        print("           TICKET DE RESERVA - ONPE")
        print("==============================================")
        print(f"Código: {t['codigo']}")
        print(f"Fecha: {t['fecha']}")
        print(f"Hora: {t['hora']}")
        print(f"Trámite: {t['tramite']}")
        print(f"ODPE: {t['odpe']}")
        print("==============================================")
    else:
        print(f"\nError: {resultado['mensaje']}")