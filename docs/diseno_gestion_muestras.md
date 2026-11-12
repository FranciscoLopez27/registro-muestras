# Diseño de la gestión de muestras

## Búsqueda de muestras por ID
Para realizar una busqueda de determinada muestra en la base de datos se necesita el ID con el que fue asignado en el sistema al momento de crear la muestra. Si encuentra coincidencia devuelve un diccionario con los datos de la muestra, y en caso contrario un valor None.
Para esto el usuario digita el ID de la muestra que busca que tiene el formato de una letra en mayuscula seguido de un guión y una combinacion de 4 digitos, como se muestra el siguiente ejemplo:
- "M-0001; M-0012; M-0111"
El texto ingresado por el usuario se le aplica una transformación de formato para que las letras se cambien a mayusculas y se eliminen todos los espacios que estuvieran en medio-inicio-fin, para coincidir con el formato de los ID para mayor casos de input de los usuarios.
En caso de que el usuario no ingrese nada o solo espacios vacios, la funcion devuelve None.

## Resultado de cada análisis
El resultado de cada analisis se guarda como una clave en el diccionario respectivo, en la lista de analisis de cada muestra como "resultado". Al momento de la creacion de la muestra, este valor se asigna como None por defecto y cuando los resultados estan listos se modifica, Esta decision de dejar None y no utilizar algun valor numerico como 0, se define para evitar problemas por mala interpretacion o calculos al poder ser un valor que tomaria un resultado real cuando no se tiene conteo.
Ejemplo:
{"codigo": "A012", "nombre": "...", "norma": "...", "unidad": "UFC/g", "limite": 100, "resultado": ..., "fuera_especificacion": ...}

## Cuando se pueden registrar los resultados
Los resultados es posible ingresarlos, en el momento que la muestra se encuentra en estado de "confirmada" por el laboratorio, que significa que se encuentra actualmente en proceso de analisis y reporte de resultados. 
Mientras las muestras se encuentre en estado de "confirmada", los resultados no seran enviado o seran visibles para los clientes, ademas de poder modificar los resultados para corrección.
Posterior a liberar la muestra los resultados quedan bloqueados, y no deberia ser posible modificar los resultados.

## Fuera de norma
Para un analisis se calcula si esta fuera de norma o especificación respecto al resultado cada vez que se consulta, como una propiedad de la clase. Puede tener un estado de None si es que no se a registrado ningun resultado (el resultado tiene el valor None almacenado), False si el resultado es menor o igual al limite de aceptacion definido para el analisis, y true si el valor del resultado es mayor al del limite.Este diseño se planteo en el sistema, para que este valor nunca pudiera quedar desactualizado y que solo se tenga una forma de consultarlo.

## Cambio de estado
Las muestras pueden tener cuatro estados posibles, que son enviadas, confirmadas, liberadas y canceladas.
- Enviada: Las muestras fueron creadas en el sistema y, se encuentran en proceso de llegar al laboratorio y/o de entrar a proceso de analisis.
- Confirmada: Las muestras fueron confirmadas que ingresaron a los respectivos analisis solicitados. En el momento de generar este cambio de estado, se empieza a contar la fecha fin para el reporte de resultados.
- Liberada: Las muestras ya tienen todos los resultados y fueron revisados para verificar que estuvieran correctamente cargadas, liberando los resultados para que sea visible al cliente o se pueda emitir el informe con todos los resultados. Si algun resultado se encuentra en None no es posible liberar la muestra.
- Canceladas: Los clientes pueden solicitar cancelar determinada muestra, por distintos motivos. No se continuan o empiezan los analisis que estuvieran asociadas a esa muestra. Para modificar a este estatus debe ser previamente conversado y solicitado con jefatura.
La trancision es lineal desde enviada luego a confirmada y finalmente a liberada, no siendo posible devolver a un estado anterior, manteniendo congruencia en el flujo de trabajo. Desde el estado de enviada y confirmada, puede modificarse a cancelada, pero una muestra liberada no puede ser cancelada ya que se completaron todos los analisis.

## Listar muestras que se encuentran fuera de norma
Se pueden listar las muestras que tengan resultado, y a su vez cumplan con la condicion de que supere el limite establecido, estando "fuera de especificacion", lo que se ve reflejado en la clave fuera_especificacion como un True. Se muestran todas las muestras en sistema que tengan a lo menos un analisis que cumplan la condición de especificación, sin importar el estado en que se encuentren (esto por temas de trazabilidad). Se agrupan en base al estado en que se encuentran en el sistema, teniendo el siguiente flujo confirmada->liberada->cancelada, y listada para una facil trazabilidad. En caso de que algun estado no tenga ninguna muestra fuera de especificación, no se muestra.
Al listar se muestra toda la información de la muestra, incluido todos los analisis. Esto es asi, principalmente para que el analista o encargado de laboratorio pueda analizar la situacion de las muestras fuera de especificación en su totalidad, para tener criterio si es necesario contactar al cliente para informar o realizare repeticiones de analisis debido a indicios extraños en los resultados.

## Pseudocódigo

## Funcion que devuelve el siguiente estatus al que es ingresado
Algoritmo: siguiente_estado
Entrada: El estado actual de la muestra.
Salida: El estado que continua en la secuencia lineal, o None si ya esta en el ultimo estado o es una muestra cancelada.

estados <- ("enviada","confirmada","liberada")
PARA CADA indice y estado EN estados:
    SI estado es igual A estado_actual ENTONCES:
        SI indice es igual A largo(estados)-1 ENTONCES:
            DEVOLVER None
        FIN SI
        estado_nuevo <- estados[indice+1]
        DEVOLVER estado_nuevo
    FIN SI
FIN PARA
DEVOLVER None

## Busca una muestra en la base de datos
Algoritmo: buscar_muestra.
Entrada: Un texto del codigo de una muestra, y la lista de muestras del sistema.
Salida: Los datos de la muestra encontrada, o None si no hay coincidencia.

id_buscado <- Aplicar mayusculas y eliminar espacios de id_muestra
PARA muestra EN lista_muestras HACER:
    SI muestra["id"] == id_buscado ENTONCES:
        DEVOLVER muestra
    FIN SI
FIN PARA
DEVOLVER None
