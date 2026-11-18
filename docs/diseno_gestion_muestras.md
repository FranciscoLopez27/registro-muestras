# Diseño de la gestión de muestras

## Búsqueda de muestras por ID
Para realizar una busqueda de determinada muestra en la base de datos se necesita el ID con el que fue asignado en el sistema al momento de crear la muestra. Si encuentra coincidencia devuelve un diccionario con los datos de la muestra, y en caso contrario un valor None.
Para esto el usuario digita el ID de la muestra que busca que tiene el formato de una letra en mayuscula seguido de un guión y una combinacion de 4 digitos, como se muestra el siguiente ejemplo:
- "M-0001; M-0012; M-0111"
El texto ingresado por el usuario se le aplica una transformación de formato para que las letras se cambien a mayusculas y se eliminen todos los espacios que estuvieran en medio-inicio-fin, para coincidir con el formato de los ID para mayor casos de input de los usuarios.
En caso de que el usuario no ingrese nada o solo espacios vacios, la funcion devuelve None.

## Análisis de una muestra
Cada muestra tiene una lista de análisis, que son objetos de la clase `Analisis`. La muestra se crea sin análisis, y estos se agregan uno a uno mediante el método `agregar_analisis`, que es la única forma de modificarlos. Desde fuera de la clase, los análisis se pueden consultar, pero se entregan como tupla, para que no se puedan agregar ni quitar directamente.

Al agregar un análisis se aplican dos reglas:

- **Solo se agregan análisis mientras la muestra está en estado enviada.** Cuando la muestra pasa a confirmada, el laboratorio ya planificó el trabajo con los análisis que tenía asignados, por lo que agregar uno después alteraría ese plan. Además, agregar un análisis a una muestra liberada dejaría un análisis sin resultado en una muestra que ya fue reportada, lo que la regla de liberación busca impedir.
- **No se permiten dos análisis con el mismo código** en una misma muestra. La comparación se hace por el código del análisis, ya que cada código identifica un único método en el catálogo.

Si alguna regla no se cumple, el análisis no se agrega y el método devuelve una lista con el error correspondiente.

## Resultado de cada análisis
Cada análisis de una muestra es un objeto de la clase `Analisis`, que guarda una copia de los datos vigentes del catálogo (código, nombre, norma), la unidad elegida, el límite definido por el cliente y su resultado.

Al crear el análisis, el resultado se inicia en None. Se decidió usar None y no un valor numérico como 0, porque 0 es un recuento real posible: usarlo para indicar "sin resultado" llevaría a confundir un análisis pendiente con uno que no tuvo crecimiento.

El resultado está protegido: desde fuera de la clase se puede leer, pero solo cambia mediante el registro de resultados de la muestra, que aplica las reglas de estado y valida el valor.

## Cuando se pueden registrar los resultados
Los resultados es posible ingresarlos, en el momento que la muestra se encuentra en estado de "confirmada" por el laboratorio, que significa que se encuentra actualmente en proceso de analisis y reporte de resultados. 
Mientras las muestras se encuentre en estado de "confirmada", los resultados no seran enviado o seran visibles para los clientes, ademas de poder modificar los resultados para corrección.
Posterior a liberar la muestra los resultados quedan bloqueados, y no deberia ser posible modificar los resultados.
Los resultados siempre se registran mediante el método registrar_resultado de la muestra, buscando el analisis por el código respectivo y delegando el registro al metodo del mismo nombre propio de la clase Analisis, que evalua las reglas relacionadas al valor del resultado ingresado. El metodo de igual nombre que esta en la clase analisis, quedo como interno, con guion bajo, para que no se pueda registrar algun resultado saltándose la revisión del estado.

## Fuera de norma
Para un analisis se calcula si esta fuera de norma o especificación respecto al resultado cada vez que se consulta, como una propiedad de la clase. Puede tener un estado de None si es que no se a registrado ningun resultado (el resultado tiene el valor None almacenado), False si el resultado es menor o igual al limite de aceptacion definido para el analisis, y true si el valor del resultado es mayor al del limite.Este diseño se planteo en el sistema, para que este valor nunca pudiera quedar desactualizado y que solo se tenga una forma de consultarlo.

## Cambio de estado
Las muestras pueden tener cuatro estados posibles, que son enviadas, confirmadas, liberadas y canceladas.
- Enviada: Las muestras fueron creadas en el sistema y, se encuentran en proceso de llegar al laboratorio y/o de entrar a proceso de analisis.
- Confirmada: Las muestras fueron confirmadas que ingresaron a los respectivos analisis solicitados. En el momento de generar este cambio de estado, se empieza a contar la fecha fin para el reporte de resultados.
- Liberada: Las muestras ya tienen todos los resultados y fueron revisados para verificar que estuvieran correctamente cargadas, liberando los resultados para que sea visible al cliente o se pueda emitir el informe con todos los resultados. Si algun resultado se encuentra en None no es posible liberar la muestra.
- Canceladas: Los clientes pueden solicitar cancelar determinada muestra, por distintos motivos. No se continuan o empiezan los analisis que estuvieran asociadas a esa muestra. Para modificar a este estatus debe ser previamente conversado y solicitado con jefatura.
La trancision es lineal desde enviada luego a confirmada y finalmente a liberada, no siendo posible devolver a un estado anterior, manteniendo congruencia en el flujo de trabajo. Desde el estado de enviada y confirmada, puede modificarse a cancelada, pero una muestra liberada no puede ser cancelada ya que se completaron todos los analisis.
Una muestra sin análisis no puede avanzar de estado, por lo que una muestra enviada sin análisis asociado no puede pasar a confirmada (pero si podria ser cancelada).

## Listar muestras que se encuentran fuera de norma
Se listan todas las muestras que tienen a lo menos un análisis fuera de especificación, es decir, cuya propiedad `fuera_especificacion` vale True. Los análisis sin resultado (None) o dentro del límite (False) no hacen que la muestra aparezca. Una muestra con varios análisis fuera de especificación aparece una sola vez.

Se incluyen las muestras sin importar su estado, incluidas las liberadas y canceladas, por temas de trazabilidad: permite revisar el historial de un cliente o de un lote aunque la muestra ya no esté en proceso.

Las muestras se muestran agrupadas por estado, siguiendo el orden del flujo del laboratorio definido en `ESTADOS_EN_ORDEN`: enviada, confirmada, liberada y cancelada. En la práctica, una muestra enviada no puede aparecer, porque los resultados solo se registran en muestras confirmadas. Los estados que no tienen ninguna muestra fuera de especificación no se muestran.

De cada muestra se despliega toda su información, incluidos los análisis que están dentro de especificación, para poder contrastar los resultados ante posibles desviaciones en el procesamiento de la muestra.

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
