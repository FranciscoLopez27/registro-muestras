## Estructura del catálogo de clientes
Los datos de los clientes van a necesitar  
- Codigo: 4 digitos caracteristicos de cada cliente como identificador  
- Nombre: Para identificar facilmente de manera visual que cliente es y poder agregarlo en los posteriores reportes de resultados  


Para la estructura seran diccionarios anidados, donde cada cliente sera un diccionario y, cada codigo y datos son las key principales, donde el segundo tambien es un diccionario con las keys nombre, tipo cliente y contacto.

Ejemplo estructura:  
Clientes:{  
    "0042": {"nombre":"FrutasNorte S.A"},  
    "0044": {"nombre":"CarnesSur S.A"},  
    "0047": {"nombre":"VerdurasCentro S.A"}  
}  

Posibles mejoras:  
- Tipo cliente: Si es externo, interno o por licitación si tiene definido un contrato a largo plazo por servicios del laboratorio  
- Contacto: datos de contacto, numero y/o correo electronico  


## Estructura del catálogo de analisis  
Los datos del catalogo de analisis que va a trabajar el laboratorio sobre las muestras son:  
- Codigo: Identificador del analisis de manera interna del laboratorio  
- Nombre: Nombre de analisis a que microorganismo analiza   
- Unidad: Unidades en el conteo que pueden ser reportadas para este metodo  
- Norma: Identificador con el codigo que se le asigno como norma internacional o si es un metodo de manera interna  

Para la estructura del catalogo de analisis sera un diccionario con diccionarios anidados con cada uno con su key Codigo que tendra un diccionario interno de datos con las key Nombre, Norma y Unidad. Para unidad el valor sera una lista con todas las posibles unidades.  

Ejemplo estructura:  
Analisis:{  
    "A012": {"nombre":"Conteo Enterobacterias", "norma":"ISO-21528-2", "unidad":["UFC/g","UFC/ml"]},  
    "A013": {"nombre":"Conteo Coliformes", "norma":"ISO-4832", "unidad":["UFC/ml"]}, 
    "A019": {"nombre":"Conteo Mohos y levaduras", "norma":"ISO-21527-2", "unidad":["UFC/g","UFC/ml"]},  
}  

Posibles mejoras:  
- Dias: Dias minimo que toma realizar el metodo en una muestra  
 

## Que guarda cada muestra de sus análisis  
En las muestras creadas para analizar en el laboratorio se guardan los siguientes valores como un diccionario:  
- Codigo_analisis: Identificador del analisis de manera interna del laboratorio.  
- Nombre: Nombre identificador del metodo analitico.
- Norma: Norma internacional asociado al analisis.  
- Limite: Limite declarado por el cliente que solicita la muestra para saber si el resultado esta fuera de especificación.  
- Unidad: Unidad declarada por el cliente en el momento de solicitar el analisis para cuantificar el conteo obtenido.  

Es necesario guardar el limite y la unidad, ya que los metodos microbiologicos internacionales cada cierto periodo se actualizan y a veces se modifican el alcance del metodo cambiando, que puede influir en la unidad que se haya ocupado en su momento ya no sea valida, o el tipo de analito ya no sea valido en la actualidad, pero que cuando estaba vigente esa versión era correcto.  
Al registrar un analisis para una muestra, se debe elegir una unidad para el metodo y se debe verificar que este dentro de la lista de unidades validas. Enc aso de no estar se le pide nuevamente seleccionar una unidad valida.


Ejemplo estructura: 
MUESTRA = {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidad": "UFC/g", "limite": 100}

## Cómo elige el usuario los analisis  
El usuario debe elegir el analisis en base al codigo interno del método. Esta elección es mas robusta, aunque la idea final es que al momento de solicitar el analisis pueda desplegarlo en un cuadro con multiples selecciones donde pueden buscar visualmente el metodo que quieran o en una barra de busqueda donde puedan digitar la información.  

Fuera de alcance:
- Que pueda ser buscado tambien por norma y/o nombre del metodo.

## Qué pasa si falta algo en el catálogo  
Por simplificar la implementacion es fuera de alcance por ahora. Pero la propuesta es que si un cliente o analisis no aparece porque no estan en el catalogo, se le notificara al cliente que no existen en sistema, y se entrara a conversaciones con el jefe de laboratorio y encargado del sistema para agregarlo si es posible. Aunque previamente a recibir nuevos clientes y nuevas muestras con analisis que nunca se hayan hecho normalmente se deberia hablar con el encargado del laboratorio previamente para que cuando se haga la solicitud de analisis ya deberia estar todo resuelto previamente a solicitar analisis para alguna muestra.

## Casos borde de la selección  
- Vacio: Si la entrada que se le solicita al que esta creando la muestra es vacio, se le informa que su entrada no es valida por ser vacio y se le solicita ingresar nuevamente un valor o dato valido.
- Espacios en blanco: El sistema quita los espacios extremos en blanco para juntar el contenido en el caso de los codigos de los metodos o codigo de clientes.
- Mayúsculas en un codigo: Se modifica para que el texto ingresado se transforme en mayuscula todas las letras y desde esa data se busca en el catalogo
- Si se escibe un codigo que no exite: Se le notifica al usuario que el codigo digitado no existe dentro de la base de datos, y se le solicita ingresar nuevamente un codigo valido.

## Regla nueva  
Otra regla seria en que en una muestra no pueden haber metodos repetidos solicitados, el mismo metodo solo puede estar una vez para cada muestra. Para esto al momento de crearle un metodo se debe compara si hay otro identico en la muestra, y rechazar e informar al que esta creando la muestra que hay duplicidad de metodos y que no es posible, solicitando ingresar nuevamente la información.  

- Fuera de alcance: En los catalogos solo se puede ingresar una vez un metodo o un cliente. Para ello cuando se quiera ingresar un nuevo cliente, se debe comparar si ya existe uno con el mismo nombre (ya que los codigos van a asignarlos el sistema automaticamente). En el caso de los metodos, se debe compara el nombre y la norma internacional o interna asociada ya que son identificadores unicos del metodo. Todo esto con el fin de evitar duplicidad en la información.

## Pseudo codigo de seleccion en los catalogos

Algoritmo: seleccion_opcion_catalogo  
Entradas: Catalogo (de los clientes o de los analisis), titulo (puede ser "Seleccione el cliente:" o "Seleccione el analisis:") 
Salida: Codigo de la selección del usuario  

MOSTRAR titulo
PARA CADA codigo, datos EN catalogo:  
    nombre ← valor de la etiqueta nombre en datos
    MOSTRAR codigo: nombre 
FIN PARA
MIENTRAS VERDADERO:
    codigo_ingresado ← PEDIR "Ingrese el código :"
    codigo_ingresado ← QUITAR ESPACIOS EXTREMOS y PASAR A MAYUSCULA   
    SI codigo_ingresado ESTA VACIO:
        MOSTRAR "El codigo no puede ser vacio, favor digitar uno valido en la lista"
        CONTINUA
    FIN SI

    SI codigo_ingresado NO ESTA EN catalogo ENTONCES:
        MOSTRAR "El codigo ingresado no se encuentra en la lista, favor vuelva a intentar con un codigo valido en la lista"
        CONTINUA
    FIN SI
    DEVOLVER codigo_ingresado
FIN MIENTRAS