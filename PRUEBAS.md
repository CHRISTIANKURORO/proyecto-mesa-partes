# Documentación de Casos de Prueba

Este documento evidencia las pruebas realizadas al prototipo del Sistema de Tickets para la mesa de partes de la ODPE, utilizando datos basados en la observación de campo.

## Caso de Prueba 1: Registro de un oficio derivado por el JEE (Flujo Real)
- **Contexto:** Según la bitácora, personal del JEE entrega un oficio al JODPE. En el sistema, esto corresponde a una entidad pública realizando una "Derivación interna".
- **Datos de entrada:** 
  - Tipo: RUC
  - Entidad: JEE
  - Nombre: Juan Pérez
  - ODPE: Independencia
  - Trámite: 4. Derivación interna
  - Fecha: 20/12/2026
- **Resultado esperado:** El sistema debe generar un ticket con código `R01`, asignando la hora `08:00`, guardar el registro y mostrarlo en la interfaz.
- **Resultado obtenido:** Éxito. Se generó el ticket `R01`, la hora fue la correcta y se visualizó en el SGD. 
- **Evidencia:** Ver carpeta `evidencias/`.

## Caso de Prueba 2: Límite de cupos por día (16 reservas)
- **Contexto:** El sistema está diseñado para recibir hasta 16 personas por día (10 en la mañana, 6 en la tarde, saltando el horario de 1pm a 2pm).
- **Datos de entrada:** Intentar generar un ticket para la fecha `21/12/2026` después de haber registrado 16 tickets para ese mismo día.
- **Resultado esperado:** El sistema debe bloquear el registro y mostrar un mensaje de error: *"No hay cupos disponibles para este día. Registre otro día."*
- **Resultado obtenido:** Éxito. El sistema bloqueó la reserva correctamente y mostró la ventana de alerta.

## Caso de Prueba 3: Validación de formato de fecha
- **Contexto:** El sistema debe evitar errores humanos al ingresar fechas.
- **Datos de entrada:** Escribir `1/1/26` o `hola` en el campo de fecha.
- **Resultado esperado:** El sistema debe mostrar un error indicando el formato correcto (`dd/mm/aaaa`).
- **Resultado obtenido:** Éxito. La función `fecha_valida` detectó el error y el mensaje de alerta apareció en pantalla.

## Caso de Prueba 4: Visualización en el módulo SGD
- **Contexto:** El personal de mesa de partes debe poder validar los tickets generados.
- **Datos de entrada:** Abrir el módulo SGD desde la interfaz gráfica.
- **Resultado esperado:** Se debe mostrar una tabla con todos los tickets generados previamente, incluyendo código, nombre, tipo de documento, ODPE, trámite, fecha y hora.
- **Resultado obtenido:** Éxito. La tabla (Treeview) cargó todos los datos del archivo `reservas.txt` correctamente.
- **Evidencia:** Ver carpeta `evidencias/`.

## Corrección de errores detectados durante el desarrollo
- **Error 1:** El botón "SGD" no abría la ventana porque faltaba la función `abrir_sgd`. **Solución:** Se agregó la función y la lógica de la tabla.
- **Error 2:** En el formulario faltaba el campo para escribir el número de DNI/RUC. **Solución:** Se agregó el campo `entry_dni` y se actualizó la lógica de guardado.