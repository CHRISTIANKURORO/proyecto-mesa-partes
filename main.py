# main.py
from portal_ciudadano import ejecutar_portal
from sgd_personal import ejecutar_sgd
from utilidades import asegurar_archivo

def main():
    asegurar_archivo()
    opcion = ""
    while opcion != "3":
        print("\n==============================================")
        print("   ONPE - TICKET MESA DE PARTES (EN LÍNEA)")
        print("==============================================")
        print("1. Portal Web del Ciudadano (generar ticket)")
        print("2. SGD - Recepción de Documentos (personal)")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ejecutar_portal()
        elif opcion == "2":
            ejecutar_sgd()
        elif opcion == "3":
            print("Saliendo del sistema...")
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()