import os                                               #módulo de la biblioteca estándar os, crear carpetas windows

ARCHIVO = "datos/reservas.txt"                          #se escribe la ruta completa encapsulando en la variable ARCHIVO
                                                
def asegurar_archivo():                                 #main linea 3
    """Crea la carpeta y el archivo si no existen."""   #Docstring, documentacion describiendo la funcion
    os.makedirs("datos", exist_ok=True)                 #creador de carpeta datos, con condicion verdadero si existe
    if not os.path.exists(ARCHIVO):                     #si no existe en la path=ruta datos/reservas.txt
        open(ARCHIVO, "w", encoding="utf-8").close()    #abre el txt y sobrescribir/tilde y cierra.
                                                        
def cargar_reservas():                                 #gestor linea 35
    """Lee el archivo y devuelve una lista de diccionarios."""
    asegurar_archivo()                                  
    reservas = []                                       #se crea una lista vacia para reservas
    with open(ARCHIVO, "r", encoding="utf-8") as f:     #lee el archivo txt
        for linea in f:                                 
            linea = linea.strip()                       
            if linea == "":                             
                continue                                
            campos = linea.split(";")                   #separa cada elemento
            if len(campos) == 10:                       
                reservas.append({                       #para convertir cada ticket/linea en diccionario
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
    return reservas                                     #almacenada en la lista otras funciones lo podran usar

def guardar_reserva(reserva):                           #gestor linea 62
    """Agrega una reserva al archivo (una línea por reserva)."""
    asegurar_archivo()
    with open(ARCHIVO, "a", encoding="utf-8") as f:     #se repite la primera funcion
        linea = ";".join([                              #separar los datos ;
            reserva["codigo"], reserva["nombre"], reserva["tipo_doc"], 
            reserva["num_doc"], reserva["entidad"], reserva["odpe"],
            reserva["direccion"], reserva["tramite"], reserva["fecha"],
            reserva["hora"]
        ])
        f.write(linea + "\n")                           #guardar tickets con sus datos registrados en el txt
                                                        
def contar_tickets_por_letra(letra):                    #gestor linea 41
    """Cuenta cuántos tickets empiezan con 'C' o 'R'."""
    reservas = cargar_reservas()
    return sum(1 for r in reservas if r["codigo"].startswith(letra)) #funcion para generar cod correlativo
                                                        
def formatear_dos_digitos(numero):                      #gestor linea 42
    """Devuelve '01', '02', ..., '10', etc."""
    return f"{numero:02d}"                              #devolver codigo con 2 digitos, decimal

def fecha_valida(fecha):                                #gestor linea 18
    """Valida formato dd/mm/aaaa (10 caracteres, barras en pos 2 y 5)."""
    if len(fecha) != 10:                                #Que tenga exactamente 10 caracteres.
        return False
    if fecha[2] != "/" or fecha[5] != "/":              #Que las barras estén en las posiciones 2 y 5
        return False
    partes = fecha.split("/")                           #Que al dividirla por barras, cada parte (día, mes, año) sea un número
    return all(p.isdigit() for p in partes)             #proposito fecha cumpla con el formato antes de guardar.