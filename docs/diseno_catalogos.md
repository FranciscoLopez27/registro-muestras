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
    "A012": {"nombre":"Conteo Enterobacterias", "norma":"ISO 21528-2", "unidades":["UFC/g","UFC/ml"]},  
    "A013": {"nombre":"Conteo Coliformes", "norma":"ISO 4832", "unidades":["UFC/ml"]}, 
    "A019": {"nombre":"Conteo Mohos y levaduras", "norma":"ISO 21527-2", "unidades":["UFC/g","UFC/ml"]},  
}  

Posibles mejoras:  
- Dias: Dias minimo que toma realizar el metodo en una muestra  
 

## Qué guarda cada muestra de sus análisis
Cada análisis de una muestra es un objeto de la clase `Analisis`, que guarda:
- Código: identificador del análisis de manera interna del laboratorio.
- Nombre: nombre identificador del método analítico, copiado del catálogo.
- Norma: norma internacional o interna asociada al análisis, copiada del catálogo.
- Unidad: unidad elegida al solicitar el análisis, entre las permitidas para el método.
- Límite: límite declarado por el cliente para saber si el resultado está fuera de especificación.
- Resultado: None hasta que se registra, protegido para que solo cambie mediante el registro de resultados de la muestra.

El nombre y la norma se copian del catálogo al momento de registrar la muestra, y la unidad y el límite se guardan junto a ellos, porque los métodos microbiológicos internacionales se actualizan cada cierto tiempo: puede cambiar su alcance, o una unidad que era válida en su momento puede dejar de serlo. Guardar estos datos permite conservar con qué versión del método se analizó cada muestra.

Al registrar un análisis para una muestra, la unidad se elige de la lista de unidades válidas del método; si no es válida, se solicita nuevamente.

Ejemplo:
Analisis("A012", "Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)

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
En una muestra no pueden haber métodos repetidos: cada método solo puede solicitarse una vez por muestra. La comparación se hace por el código del análisis, ya que cada código identifica un único método en el catálogo. Si se intenta agregar un método que ya está en la muestra, se rechaza y se informa al usuario que hay duplicidad de métodos, solicitando ingresar nuevamente la información.

Esta regla se aplica en tres niveles:
- **Al elegir los análisis en el menú:** el sistema no permite seleccionar un método que ya fue agregado a la muestra que se está registrando.
- **Al validar los datos ingresados** (`validar_muestra`): se revisa nuevamente que no haya códigos repetidos, como respaldo, ya que en el futuro los datos podrían provenir de un archivo y no del menú.
- **Al agregar el análisis a la muestra** (`Muestra.agregar_analisis`): la propia muestra rechaza un código repetido, por lo que la regla se cumple aunque se intente agregar un análisis por otro camino.

- Fuera de alcance: En los catálogos solo se puede ingresar una vez un método o un cliente. Para ello, cuando se quiera ingresar un nuevo cliente, se debe comparar si ya existe uno con el mismo nombre (ya que los códigos los asignará el sistema automáticamente). En el caso de los métodos, se debe comparar el nombre y la norma internacional o interna asociada, ya que son identificadores únicos del método. Todo esto con el fin de evitar duplicidad en la información.

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

Parte 3: Pedir un análisis desde el catálogo (40 minutos)

Una función que arme el análisis tal como lo definiste en tu diseño:

Elige el código del análisis con elegir_codigo.
Obtiene sus datos del catálogo.
Elige la unidad entre las permitidas para ese análisis.
Pide el límite (puedes reutilizar el ciclo que ya tienes en generar_diccionario_analisis).
Devuelve el diccionario con la copia de los datos vigentes: código, nombre, norma, unidad y límite.

Pruébala a mano desde el intérprete, igual que la primera.

Todavía no la conectes con pedir_analisis ni borres nada: eso será el siguiente paso. Al terminar, ejecuta py test_registro.py para confirmar que no rompiste nada, y haz commit y push.

Muéstrame cada función cuando la tengas.