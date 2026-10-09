from datetime import date
import copy

#Codigo de unidades de conteo
UNIDADES_VALIDAS = {"UFC/g", "UFC/ml", "UFC/swab", "NMP/g", "NMP/ml"}
UNIDADES_VALIDAS_MINUSCULAS = {unidad.lower() for unidad in UNIDADES_VALIDAS}

#Codigos de clientes registrados
CLIENTES_REGISTRADOS = {"0042", "1234", "5678"}

def es_cliente_valido(cliente):
    return len(cliente) == 4 and cliente.isdigit() and cliente in CLIENTES_REGISTRADOS 

def es_unidad_valida(unidad):
    return unidad.lower() in UNIDADES_VALIDAS_MINUSCULAS

def generar_id(numero):
    return f"M-{numero:04d}"

def validar_muestra(datos_muestra):
    cliente = datos_muestra["cliente"] 
    descripcion = datos_muestra["descripcion"]
    analisis = datos_muestra["analisis"]
    lista_errores = []

    if not descripcion.strip():
        lista_errores.append("La muestra necesita obligatoriamente una descripcion")

    if not cliente.isdigit():
        lista_errores.append("El codigo del cliente ingresado no es numerico")

    elif len(cliente) != 4:
        lista_errores.append("El codigo del cliente debe ser de 4 digitos")

    elif not cliente in CLIENTES_REGISTRADOS:
        lista_errores.append("El codigo del cliente no corresponde a un cliente registrado en la base de datos")

    if len(analisis) == 0:
        lista_errores.append("La muestras creadas deben tener asociado minimo un analisis para registrarse")
    
    for analisis_individual in analisis:

        if  not analisis_individual["nombre"].strip():
            lista_errores.append("Todos los analisis ingresados deben tener nombre")

        if analisis_individual["limite"] < 0:
            lista_errores.append("El limite de conteo ingresado debe ser mayor o igual a 0")

        if not es_unidad_valida(analisis_individual["unidad"]):
            lista_errores.append(f"La unidad de conteo del analisis {analisis_individual["nombre"]} ingresados no esta registrada")

    return lista_errores


def agregar_muestra(lista_muestras, datos_muestra):
    
    lista_errores = validar_muestra(datos_muestra)
    
    if not lista_errores:
        nueva_muestra = copy.deepcopy(datos_muestra)
        nueva_muestra.update({
            "id": generar_id(len(lista_muestras)+1),
            "estado": "enviada",
            "fecha_ingreso": date.today().isoformat()
        })
        lista_muestras.append(nueva_muestra)
        return (nueva_muestra["id"],lista_errores)
    
    return(None, lista_errores)
    

def listar_muestras(lista_muestras):
    if len(lista_muestras) == 0:
        print("No se encuentran muestras registradas en la base de datos")
    else:
        for muestra in lista_muestras:
            print(
                f"id: {muestra['id']} || cliente: {muestra['cliente']} || descripcion: {muestra['descripcion']} ||"
                f" estado: {muestra['estado']} || fecha: {muestra['fecha_ingreso']}"
                )
            for analisis in muestra["analisis"]:
                print(f"Nombre analisis: {analisis['nombre']} || Limite conteo: {analisis['limite']} || Unidad: {analisis['unidad']}")
            print("")
    return


def mostrar_menu():
    print("\n--------   Registro de muestras   --------")
    print("1. Agregar muestra")
    print("2. Listar muestras")
    print("3. Salir")

def generar_diccionario_analisis():
    """Solicita los datos al usuario y genera un diccionario con la información"""
    nombre_analisis = input("Ingrese nombre de análisis: \n")
    unidad_conteo = input("Ingrese la unidad del conteo ej: UFC/g ...\n")
    while True:
        limite_conteo = input("Ingrese el limite de conteo para el análisis: \n").strip()
        if limite_conteo.isdigit():
            limite_conteo = int(limite_conteo)
            break
        else:
            print("Error: Limite de conteo debe ser un numero, ingresar nuevamente")
    datos_analisis = {
        "nombre" : nombre_analisis,
        "limite" : limite_conteo,
        "unidad" : unidad_conteo
        }
    return datos_analisis

def pedir_analisis():
    """Pide al usuario uno o mas análisis y devuleve la lista de estos"""
    lista_analisis = []
    datos_analisis = generar_diccionario_analisis()
    lista_analisis.append(datos_analisis)
    while True:
        opcion_usuario = input("¿Agregar otro análisis? (s/n)\n").strip().lower()
        if opcion_usuario == "s":
            datos_analisis = generar_diccionario_analisis()
            lista_analisis.append(datos_analisis)
        elif opcion_usuario == "n":
            break
        else:
            print("Opcion ingresada invalida, opciones posibles: S | N")
    return lista_analisis

def pedir_datos_muestra():
    cliente_muestra = input("Ingresar codigo de cliente (cuatro digitos, anteponiendo 0):\n").strip()
    descripcion_muestra = input("Ingresar descripción de la muestra:\n").strip()
    analisis_muestra = pedir_analisis()
    datos_muestra = {
        "cliente": cliente_muestra,
        "descripcion": descripcion_muestra,
        "analisis": analisis_muestra
    }
    return datos_muestra

def main():
    lista_muestras = []
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            id_nuevo, errores = agregar_muestra(lista_muestras,pedir_datos_muestra())
            if errores:
                print("La muestra no ha podido ser creada")
                for error in errores:
                    print(f"ERROR AL CREAR LA MUESTRA: {error}")
                    
            else:
                print("Muestra agregada con exito")
                print(f"ID de la muestra: {id_nuevo}")
        elif opcion == "2":
            listar_muestras(lista_muestras)
        elif opcion == "3":
            print("Adios...")
            input("Presiones enter para continuar...")
            break
        else:
            print("Opcion invalida, pruebe nuevamente")

if __name__ == "__main__":
    main()
