# sgd_personal.py
from utilidades import cargar_reservas

def consultar_reservas_sgd():
    print("\n==============================================")
    print("   SGD - RECEPCIÓN DE DOCUMENTOS (MESA PARTES)")
    print("==============================================")

    reservas = cargar_reservas()
    if not reservas:
        print("No hay reservas registradas.")
        return

    for r in reservas:
        print(f"Código: {r['codigo']}")
        print(f"Nombre: {r['nombre']}")
        print(f"{r['tipo_doc']}: {r['num_doc']}")
        if r["tipo_doc"] == "RUC":
            print(f"Entidad: {r['entidad']}")
        print(f"ODPE: {r['odpe']}")
        print(f"Dirección: {r['direccion']}")
        print(f"Trámite: {r['tramite']}")
        print(f"Fecha: {r['fecha']}")
        print(f"Hora: {r['hora']}")
        print("-------------------------------")

def ejecutar_sgd():
    print("\n[SGD] Acceso exclusivo del personal autorizado.")
    consultar_reservas_sgd()