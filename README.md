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
    - Nombre (copiados del catalogo)
    - Norma  (copiados del catalogo)
    - Unidad (elegida entre las permitidas para el análisis)
    - Limite (definido por el cliente)
    - Resultado (vacío hasta que se registra)
    - Fuera de especificacion (se calcula al registrar el resultado)

## Funcionalidades

- Ingreso de muestras. (Implementado)
- Generación de id de muestras. (Implementado)
- Selección de clientes y análisis desde catálogos. (Implementado)
- Asignación de análisis para cada muestra desde el catálogo. (Implementado)
- Búsqueda de muestras por ID. (Implementado)
- Cambio de estado de la muestra, incluida la cancelación con confirmación. (Implementado)
- Registro de resultado por análisis de muestra. (Implementado)
- Cálculo automático de fuera de especificación. (Implementado)
- Despliegue de análisis y resultados de muestra. (Implementado)
- Listado de muestras fuera de norma. (Implementado)
- Registro de día de inicio de análisis. (Pendiente)
- Registro del analista encargado del análisis. (Pendiente)
- Definición de fecha límite para reporte. (Pendiente)

## Reglas

**Muestras y catálogos**
- ID de cada muestra es único.
- La descripción de todas las muestras no puede estar en blanco.
- El cliente debe existir en el catálogo de clientes.
- Cada análisis debe existir en el catálogo de análisis.
- La unidad debe estar entre las permitidas para ese análisis.
- Una muestra no puede tener el mismo análisis repetido.
- Al registrar una muestra, se guarda una copia de los datos vigentes del análisis (nombre, norma y unidad), para conservar la información aunque el catálogo cambie después.
- Se consideran solo análisis cuantitativos, es decir, se realizan conteos.
- El límite de conteo debe ser mayor o igual a 0.

**Estados**
- Los estados posibles son enviada, confirmada (entró a análisis), liberada y cancelada.
- Los estados solo avanzan linealmente: enviada, confirmada y liberada, sin volver atrás.
- Solo se pueden cancelar muestras enviadas o confirmadas, con confirmación explícita. Una muestra cancelada no puede cambiar de estado.
- No se puede liberar una muestra con resultados pendientes.
- Las muestras liberadas no pueden ser modificadas.

**Resultados**
- Los resultados solo se registran en muestras confirmadas, y pueden corregirse mientras la muestra siga confirmada.
- Un resultado debe ser un número entero mayor o igual a 0.
- Un análisis está fuera de especificación cuando su resultado es superior al límite indicado por el cliente (generalmente el del RSA).
- El fuera de especificación se recalcula cada vez que se registra o corrige un resultado.

## Fuera del alcance (por ahora)
- Agrupación de muestras por análisis y por día de análisis.
- Ingreso de usuarios diferenciado por cargo.
- Generación de informe con los resultados para cliente.
- Generación de tiempo fin de reporte de forma automática en base a análisis.
- Integrar análisis cualitativo para las muestras.
- Que el límite pueda quedar sin definir por el cliente.
- Casos de ID repetidos.
- Gestión de los catálogos (agregar clientes y análisis, y evitar duplicados).
- Búsqueda de análisis por norma o nombre.
- Aceptar códigos de cliente sin los ceros a la izquierda.
- Cambio de estado en lote para varias muestras a la vez.


## Cómo usar

Ejecutar el programa:

    py registro.py

Ejecutar las pruebas:

    py test_registro.py

## Documentación

- [Diseño de los catálogos de clientes y análisis](docs/diseno_catalogos.md)
- [Diseño de la gestión de muestras](docs/diseno_gestion_muestras.md)
- [Pseudocódigo de las funcionalidades](docs/pseudocodigo.md)