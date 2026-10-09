# Registro de muestras de laboratorio

## Problema
La información relacionada a las muestras que se procesan en un laboratorio a través del tiempo puede llegar a ser masiva, por lo que tratar de realizar alguna trazabilidad y optimizar el flujo de información relacionado a estos es un desafío. Para ello es necesario un sistema que permita albergar toda la información generada de cada muestra procesada en un solo lugar y que pueda consultarse de manera ágil y fácil.

## Usuarios
Personal del equipo de microbiología encargado de registrar las muestras que son procesadas en su laboratorio.

## Datos de una muestra
- Nombre muestra
- Descripcion de la muestra
- Numero de identificación de la muestra.
- Estado de la muestra.
- Cliente que solicita análisis para la muestra.
- Limite de conteo para cada análisis de la muestra.
- Unidad del resultado.
- Fecha de ingreso.
- Fecha de término de tiempo de respuesta.
- Analistas que llevan a cabo el análisis.
- Análisis que son solicitados para la muestra
- Resultados por análisis.
- Usuario que carga los resultados.
- Comentario por parte de los analistas (si es necesario).


## Funcionalidades

- Ingreso de muestras.
- Generación de id muestras.
- Asignación de análisis para cada muestra.
- Registro de día de inicio de análisis.
- Registro del analista encargado del análisis.
- Registro de resultado por análisis de muestra.
- Definición de fecha límite para reporte.
- Busqueda de muestras por ID.
- Despliegue de análisis y resultados de muestra.
- Listado de muestras fuera de norma.

## Reglas
- Una muestra se encuentra fuera de norma cuando el resultado es superior al límite indicado por el cliente (generalmente el del RSA).
- Se consideran solo analisis Cuantitativos, es decir se ralizan conteos.
- Una muestra puede estar en estado de enviada, confirmada por el laboratorio (entro a análisis) y liberada.
- ID de cada muestra es único.
- Los estados de las muestras solo pueden cambiar linealmente de enviada a confirmada a liberada.
- Las muestras liberadas no pueden ser modificadas.
- La descripcion de todas las muestras no pueden estar en blanco
- Limite de conteo deben ser mayor o igual a 0


## Fuera del alcance (por ahora)
- Agrupación de muestras por análisis y por día de análisis
- Ingreso de usuarios diferenciado por cargo.
- Generación de informe con los resultados para cliente
- Generación de tiempo fin de reporte de forma automática en base a análisis.
- Integrar análisis cualitativo para las muestras.
- Limite pueda dejarse no definirse por el cliente (nunca estara fuera de especificacion)
- Casos de ID repetidos

## Cómo usar

Ejecutar el programa:

    py registro.py

Ejecutar las pruebas:

    py test_registro.py