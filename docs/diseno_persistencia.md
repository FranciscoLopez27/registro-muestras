# Diseño de la persistencia

## Objetivo
Que las muestras registradas no se pierdan al cerrar el programa. Las muestras se guardan en un archivo JSON (`muestras.json`) y se cargan al iniciar.

## Guardar
Cada clase sabe convertirse a sí misma en un diccionario con sus datos, mediante el método `a_diccionario`. La muestra delega en cada uno de sus análisis la conversión de sus propios datos. La función `guardar_muestras` de `storage.py` convierte todas las muestras y escribe la lista completa en el archivo, reemplazando su contenido anterior.

No se guarda el fuera de especificación de cada análisis: es una propiedad calculada a partir del resultado y el límite, que ya están guardados. Así, nunca puede quedar en el archivo un valor que contradiga al resultado.

El archivo de datos no se sube al repositorio (está en `.gitignore`), porque contiene los datos del laboratorio y no el código.

## Cargar: restaurar, no repetir el flujo
Al cargar, cada muestra se reconstruye directamente con su estado y sus resultados tal como están en el archivo, mediante el método de clase `desde_diccionario`. Se descartó reconstruirlas llevándolas de nuevo por el flujo del laboratorio (agregar análisis, confirmar, registrar resultados, liberar), por dos razones:

- **Cargar no es repetir el trabajo.** Si cada carga volviera a ejecutar cada paso, cuando exista un registro de trazabilidad, cada apertura del programa generaría registros falsos de cambios que ya ocurrieron.
- **Las reglas pueden cambiar.** Una muestra liberada correctamente con las reglas de su momento no debe quedar imposible de cargar si después se agrega una nueva condición para liberar.

## Validación al cargar: integridad, no reglas de negocio
El archivo es una puerta de entrada que no pasa por las reglas de las clases, por ejemplo si alguien lo edita manualmente. Por eso, al cargar se revisa la **integridad** de cada registro: lo que debe ser cierto siempre, con cualquier versión de las reglas. Por ejemplo:

- Que estén todas las claves necesarias.
- Que el estado sea uno de los estados existentes.
- Que cada resultado sea None o un número no negativo.

No se revisan las reglas de negocio que podrían cambiar en el tiempo.

## Registros con problemas: cuarentena
Si un registro no pasa la validación, se consideraron tres opciones:

1. **Cargar las demás muestras y descartar las inválidas con un aviso.** Permite seguir trabajando, pero al guardar, el archivo se sobrescribe sin esos registros y se pierden para siempre.
2. **No cargar nada y detener el programa.** Protege los datos, pero detiene todo el trabajo por un problema que puede afectar a una sola muestra.
3. **Cuarentena**, la opción elegida, inspirada en el manejo de productos con resultados dudosos en el laboratorio:
   - Las muestras válidas se cargan, para que el trabajo siga.
   - Los registros con problemas no se descartan: se conservan intactos, aparte.
   - Al guardar, se escriben tanto las muestras válidas como los registros en cuarentena, sin modificarlos, para que nunca se pierdan.
   - Mientras haya registros en cuarentena, el programa muestra una alerta cada vez que se abre, para que el problema no quede olvidado hasta que alguien lo revise y lo corrija.

## Mejoras futuras
- Proteger el archivo de datos con permisos de acceso y detectar si fue modificado fuera del programa.
- Reemplazar el archivo por una base de datos, en la etapa de SQL.