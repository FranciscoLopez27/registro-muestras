# Registro de muestras de laboratorio

## Problema
La información relacionada a las muestras que se procesan en un laboratorio a través del tiempo puede llegar a ser masiva, por lo que tratar de realizar alguna trazabilidad y optimizar el flujo de información relacionado a estos es un desafío. Para ello es necesario un sistema que permita albergar toda la información generada de cada muestra procesada en un solo lugar y que pueda consultarse de manera ágil y fácil.

## Usuarios
Personal del equipo de microbiología encargado de registrar las muestras que son procesadas en su laboratorio.

## Datos de una muestra
- ID muestra
- Descripcion de la muestra
- Codigo del cliente (elegido desde el catalogo)
- Estado de la muestra
- Fecha de ingreso
- Analistas (pendiente)  
- Fecha de termino (pendiente) 
- Comentarios (pendiente) 
- Analisis:
    - Codigo del analisis
    - Nombre
    - Norma  
    - Unidad  
    - Limite (copiados del catalogo)

## Funcionalidades

- Ingreso de muestras. (Implementado)  
- Generación de id muestras. (Implementado)  
- Asignación de análisis para cada muestra desde catalogo. (Implementado)  
- Registro de día de inicio de análisis. (Pendiente)
- Registro del analista encargado del análisis. (Pendiente)
- Registro de resultado por análisis de muestra. (Pendiente)
- Definición de fecha límite para reporte. (Pendiente)
- Busqueda de muestras por ID. (Pendiente)
- Despliegue de análisis y resultados de muestra. (Pendiente)
- Listado de muestras fuera de norma. (Pendiente)
- Seleccion de clientes y analisis desde catalogos. (Implementado) 

## Reglas
- Una muestra se encuentra fuera de norma cuando el resultado es superior al límite indicado por el cliente (generalmente el del RSA).  
- Se consideran solo analisis Cuantitativos, es decir se realizan conteos.  
- Una muestra puede estar en estado de enviada, confirmada por el laboratorio (entro a análisis) y liberada.  
- ID de cada muestra es único.  
- Los estados de las muestras solo pueden cambiar linealmente de enviada a confirmada a liberada.  
- Las muestras liberadas no pueden ser modificadas.  
- La descripcion de todas las muestras no pueden estar en blanco  
- Limite de conteo deben ser mayor o igual a 0.  
- El cliente debe existir en el catálogo de clientes.  
- Cada análisis debe existir en el catálogo de análisis.  
- La unidad debe estar entre las permitidas para ese análisis.  
- Una muestra no puede tener el mismo análisis repetido.  
- Al registrar una muestra, se guarda una copia de los datos vigentes del análisis (nombre, norma y unidad), para conservar la información aunque el catálogo cambie después.  


## Fuera del alcance (por ahora)
- Agrupación de muestras por análisis y por día de análisis.  
- Ingreso de usuarios diferenciado por cargo.  
- Generación de informe con los resultados para cliente.  
- Generación de tiempo fin de reporte de forma automática en base a análisis.  
- Integrar análisis cualitativo para las muestras.  
- Limite pueda dejarse no definirse por el cliente (nunca estara fuera de especificacion).  
- Casos de ID repetidos.  
- Gestión de los catálogos (agregar clientes y análisis, y evitar duplicados).  
- Búsqueda de análisis por norma o nombre.  
- Aceptar códigos de cliente sin los ceros a la izquierda.  

## Cómo usar

Ejecutar el programa:

    py registro.py

Ejecutar las pruebas:

    py test_registro.py

## Documentación

- [Diseño de los catálogos de clientes y análisis](docs/diseno_catalogos.md)
- [Pseudocódigo de las funcionalidades](docs/pseudocodigo.md)