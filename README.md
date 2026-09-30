# Registro de muestras de laboratorio

## Problema
La informacion relacionada a las muestras que se procesan en un laboratorio a traves del tiempo puede llegar a ser masiva, por lo que tratar de realizar alguna trazabilidad y optimizar el flujo de informacion relacionado a estos es un desafio. Para ello es necesario un sistema que permita albergar toda la informacion generada de cada muestra procesada en un solo lugar y que pueda consultarse de manera agil y facil.

## Usuarios
Personal del equipo de microbiologia encargado de registrar las muestras que son procesadas en su laboratorio.

## Datos de una muestra
Numero de identificacion de la muestra
Fecha de ingreso
Fecha de termino de tiempo de respuesta
Analistas que llevan a cabo el analisis
Analisis que son solicitados para la muestra
Resultados por analisis
Usuario que carga los resultados
Comentario por parte de los analisitas (si es necesario)

## Funcionalidades
Ingreso de usuario
Ingreso de muestras
Generacion de id muestras
Asignacion de analisis para cada muestra
Registro de dia de inicio de analisis
Registro de resultado por analisis de muestra
Definicion de fecha limite para reporte


## Reglas
Una muestra se encuentra fuera de norma cuando el limite de conteo es superior al indicado por el cliente o el RSA
Una muestra puede estar en estado de enviada, confirmada por el laboratior (entro a anlsis) y liberada.


## Fuera del alcance (por ahora)
Agrupacion de muestras por analisis y por dia de analisis
Ingreso de usuarios diferenciado por cargo.
Generacion de informe con los resultados para cliente
Generacion de tiempo fin de reporte de forma automatica en base a analisis.