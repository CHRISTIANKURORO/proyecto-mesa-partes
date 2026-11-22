# utilidades.py
import os #Sin import os, Python no sabría cómo crear carpetas

ARCHIVO = "datos/reservas.txt"                  #variable global,en lugar de escribir la ruta completa simplemente usamos la variable ARCHIVO
                                                #solo es texto por el momento.
def asegurar_archivo():                         #herramienta asegurar archivo con estas instrucciones: (utilidades main interfaz)
    """Crea la carpeta y el archivo si no existen.""" #esto es Docstring, solo texto describiendo la funcion
    os.makedirs("datos", exist_ok=True)         #crear carpeta, 1 nombre, 2 si existe continue no error, mode/permisos*no se puso
    if not os.path.exists(ARCHIVO):             #path=ruta, si no existe el archivo datos/reservas.txt
        open(ARCHIVO, "w", encoding="utf-8").close() #abre la ruta y escribe,aceptañ y tilde, y cierra.
                                                        #si existe el archivo no se cumple el if y no se vacio lo guardado
def cargar_reservas():                          #herramienta cargarreservas con estas instrucciones: (utilidades sgd_personal interfaz)
    """Lee el archivo y devuelve una lista de diccionarios."""
    asegurar_archivo()                          #invocandolo/reutilizando/se va al principio para crear archivo etc..., retornando con:
    reservas = []                               #se crea una caja vacia para reservas en python 
    with open(ARCHIVO, "r", encoding="utf-8") as f:     #abre y lee el archivo y apoda ese proceso como f
        for linea in f:                         #en cada leida de linea del txt se recorre en linea
            linea = linea.strip()               #cada recorrido se usa strip/\n saltos para que no este junto en una linea
            if linea == "":                     #si la primera,la segunda,.... linea esta vacia, entonces
                continue                        #contua leyendo la siguiente linea
            campos = linea.split(";")           #separa cada elemento de la linea mediante split/cortes ejem: c juan sosa
            if len(campos) == 10:               #cuenta cuántos elementos (pedazos de texto) hay
                reservas.append({               #es el centro de guardado de todo, la lista reservas se agrega:
                    "codigo": campos[0],        # por ejem la primera fila y se guardaran cada pedazo que cortamos
                    "nombre": campos[1],        #en los diccionarios palabras en comillas, osea segun el ejem
                    "tipo_doc": campos[2],      #c iria en codigo, juan en nombre, etc. recordar diccionario
                    "num_doc": campos[3],       #llevan corchetes inicio fin.
                    "entidad": campos[4],       #y como tiene for se repite cada linea del txt con sus 10 elementos
                    "odpe": campos[5],          # cortados por el split y nominados por el diccionario.
                    "direccion": campos[6],        #ademas que se alamcena en reservas, donde se lee el archivo 
                    "tramite": campos[7],          #txt y se sobreescribe segun la ruta que especificamos en 
                    "fecha": campos[8],         #nuestro primer funcion
                    "hora": campos[9],
                })
    return reservas                             #devolvera los campos llenados. 

def guardar_reserva(reserva):                   #llamado por interfaz y portal_ciudadano (portal_ciudadano interfaz)
    """Agrega una reserva al archivo (una línea por reserva)."""
    asegurar_archivo()
    with open(ARCHIVO, "a", encoding="utf-8") as f:  #a de append, enla ultima linea agregara mas datos
        linea = ";".join([                      #la primera linea esta separado mendiante ;
            reserva["codigo"], reserva["nombre"], reserva["tipo_doc"], #igual paraa cada elemento
            reserva["num_doc"], reserva["entidad"], reserva["odpe"],
            reserva["direccion"], reserva["tramite"], reserva["fecha"],
            reserva["hora"]
        ])
        f.write(linea + "\n")                   #a ese archivo lo guarda conwrite y genera un espacio de linea

def contar_reservas_por_fecha(fecha_buscada):   #cuenta con parametro fechabuscada, osea el texto de fecha (portal_ciudadano  interfaz)
    """Cuenta cuántas reservas hay en una fecha específica."""
    reservas = cargar_reservas()                #llama/LEE de cargareservas, lo almacena en reservas
    return sum(1 for r in reservas if r["fecha"] == fecha_buscada) #SI ESA RESERVAS QUE SE HA RECORRIDO SE ENCUENTRA
                                                #DENTRO DEL RECorrido y ademas es igual a la fecha que busco, dale 1 y suma todo los 1 (son ticket)
def contar_tickets_por_letra(letra):            #(portal_ciudadano interfaz)
    """Cuenta cuántos tickets empiezan con 'C' o 'R'."""
    reservas = cargar_reservas()
    return sum(1 for r in reservas if r["codigo"].startswith(letra))  #si codigo coincide con la letra q busco ok
                                                # y suma 1, llamado por modulo portal_ciudadan y interfaz
def formatear_dos_digitos(numero):              #(portal_ciudadano interfaz)
    """Devuelve '01', '02', ..., '10', etc."""
    return f"{numero:02d}"                      #rellena el codigo nuemro con 0 mas 2 digitos mas que sea decimal

def obtener_hora_por_turno(numero_turno):       #(portal_ciudadano  interfaz)
    """Turno 1 -> 08:00, turno 2 -> 08:30, ... turno 16 -> 16:30."""
    horas = [
        "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
        "11:00", "11:30", "12:00", "12:30",
        "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
    ]
    if 1 <= numero_turno <= 16:                 #Si el número de turno está entre 1 y 16 (ambos incluidos)
        return horas[numero_turno - 1]          #Devuelve la hora correspondiente de la lista
    return ""                                   #-1 xq python cuenta de zero, si no esta en el rango devuelve cadena vacia

def fecha_valida(fecha):                        #(portal_ciudadano  interfaz)
    """Valida formato dd/mm/aaaa (10 caracteres, barras en pos 2 y 5)."""
    if len(fecha) != 10:
        return False
    if fecha[2] != "/" or fecha[5] != "/":
        return False
    partes = fecha.split("/")
    return all(p.isdigit() for p in partes)
                                                #"Para validar la fecha:
                                                #1. Que tenga exactamente 10 caracteres.
                                                #2. Que las barras estén en las posiciones 2 y 5.
                                                #3. Que al dividirla por barras, cada parte (día, mes, año) sea un número.
                                                #Si todo se cumple, devuelve Verdadero. Si algo falla, devuelve Falso."