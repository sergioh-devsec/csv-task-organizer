# CSV Task Organizer · CyberSerchMX

Automatización local terminada en Python 3.10+, sin dependencias ni servicios externos. Convierte CSV en un plan limpio y descargable. No sube archivos ni envía correos.

## Caso reproducible

La muestra ficticia contiene 6 registros: 1 duplicado, 1 tarea completada y 1 fecha inválida. El resultado contiene 3 pendientes, ordenados por prioridad y fecha; `Preparar informe` aparece primero.

```sh
python organizer.py sample.csv --output plan.csv
python -m unittest -v
```

El archivo de salida debe ser nuevo: nunca se sobrescribe la entrada ni un archivo existente. Un resumen JSON en la terminal explica los descartes. Máximo 200 registros y 20 KB. Cabecera `tarea,responsable,prioridad,fecha,estado`; también admite `task,owner,priority,due,status`. Prioridad alta/media/baja; estado pendiente/en curso/completada. Fechas AAAA-MM-DD reales.

Los duplicados se comparan por los cinco campos normalizados. Tareas del mismo nombre con responsable diferente se conservan. Admite comillas CSV. Neutraliza prefijos de fórmulas en la exportación; revisa la configuración de tu hoja de cálculo antes de abrir archivos de origen desconocido.

## Límites

No es un gestor de proyectos ni sincroniza servicios. Las filas inválidas se descartan y se informan por número de registro CSV (no por línea física si una celda tiene saltos de línea). Revisa el resumen antes de usar el plan. No publiques datos reales de clientes.

Demostración web relacionada: https://sergioh-devsec.github.io/#automation. Este repositorio contiene la versión CLI en Python.
