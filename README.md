# Ordena tareas CSV

Soy Serch. Una lista repetida o mal ordenada puede robar más tiempo que una tarea difícil. Hice esta herramienta para explicar y automatizar esa limpieza.

## Por qué y para qué
Apliqué diseño de software separando lectura, validación, deduplicación y exportación. Desde la seguridad añadí neutralización de fórmulas y salidas que no sobrescriben archivos. Las filas descartadas quedan identificadas, para no esconder errores bajo un resultado limpio.

Lo estoy incorporando a mi laboratorio como parte de mi práctica profesional y mi curiosidad por construir herramientas útiles. Esta es una herramienta de muestra, no una historia de resultados de clientes.

## Pruébalo
Python 3.10 o posterior, sin dependencias externas. Desde esta carpeta:

    python organizer.py sample.csv --output tareas-ordenadas.csv
    python -m unittest -v

También puedes usar la [versión ligera en el navegador](https://sergioh-devsec.github.io/herramientas.html#csv), sin enviar el archivo a un servidor.

## Proceso
1. Definí la entrada y sus límites antes de programar.
2. Separé lógica de procesamiento y argumentos de la terminal.
3. Preparé una muestra ficticia y pruebas de entradas válidas e inválidas.
4. Añadí exportación y mensajes de error que permiten revisar el resultado.

## Alcance honesto
Admite un esquema concreto ES/EN, 200 tareas y 20 KB. Las fechas usan AAAA-MM-DD. Quita completadas, no integra agendas ni servicios remotos. Revisa los descartes antes de usar el resultado.

El archivo original no se modifica. No se recoge telemetría ni se envían datos. No publiques registros reales en incidencias. El próximo paso es ampliar formatos conservando las validaciones.

— Serch · CyberSerchMX
