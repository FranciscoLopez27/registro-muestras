from datetime import date
import copy

#Catalogos

CATALOGO_CLIENTES = {
    "0042": {"nombre": "FrutasNorte S.A."},
    "0044": {"nombre": "CarnesSur S.A."},
    "0047": {"nombre": "VerdurasCentro S.A."},
}

CATALOGO_ANALISIS = {
    "A012": {"nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidades": ["UFC/g", "UFC/ml"]},
    "A013": {"nombre": "Conteo Coliformes", "norma": "ISO 4832", "unidades": ["UFC/ml"]},
    "A019": {"nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2", "unidades": ["UFC/g", "UFC/ml"]},
}

ESTADOS_POSIBLES = ("enviada","confirmada","liberada")

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

    elif cliente not in CATALOGO_CLIENTES:
        lista_errores.append("El codigo del cliente no corresponde a un cliente registrado en la base de datos")

    if len(analisis) == 0:
        lista_errores.append("La muestras creadas deben tener asociado minimo un analisis para registrarse")

    lista_codigos_analisis = [analisis_individual["codigo"] for analisis_individual in analisis]
    if len(lista_codigos_analisis) != len(set(lista_codigos_analisis)):
        lista_errores.append("No pueden haber analisis repetidos para una muestra")

    for analisis_individual in analisis:

        if not analisis_individual["nombre"].strip():
            lista_errores.append("Todos los analisis ingresados deben tener nombre")

        if analisis_individual["limite"] < 0:
            lista_errores.append("El limite de conteo ingresado debe ser mayor o igual a 0")

        codigo_analisis = analisis_individual["codigo"]
        if codigo_analisis not in CATALOGO_ANALISIS:
            lista_errores.append(f"El codigo: {codigo_analisis} no es un analisis registrado en la base de datos")
            continue

        unidades_permitidas = CATALOGO_ANALISIS[codigo_analisis]["unidades"]
        if analisis_individual["unidad"] not in unidades_permitidas:
            lista_errores.append(f"La unidad de conteo {analisis_individual["unidad"]} del analisis de {analisis_individual["nombre"]} ingresados no esta registrada para ese analisis")

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
        print("\nNo se encuentran muestras registradas en la base de datos")
    else:
        for muestra in lista_muestras:
            codigo_cliente = muestra['cliente']
            nombre_cliente = CATALOGO_CLIENTES.get(codigo_cliente, {}).get('nombre', "Cliente desconocido")
            print(
                f"\nID: {muestra['id']} || Cliente: {codigo_cliente} - {nombre_cliente} || "
                f" Descripcion: {muestra['descripcion']} || Estado: {muestra['estado']} || Fecha: {muestra['fecha_ingreso']}\n"
                )
            print("Analisis asociados a la muestra: ")
            for analisis in muestra["analisis"]:
                print(f"\nNombre analisis: {analisis['nombre']} || Codigo: {analisis['codigo']} || Norma: {analisis['norma']} || "
                      f"Limite conteo: {analisis['limite']} || Unidad: {analisis['unidad']}")
            print("")
            print("-------------------O--------------------")
    return

def mostrar_menu():
    print("\n--------   Registro de muestras   --------")
    print("1. Agregar muestra")
    print("2. Listar muestras")
    print("3. Buscar muestra")
    print("4. Salir\n")

def pedir_analisis():
    """Pide al usuario uno o mas análisis y devuleve la lista de estos"""
    lista_analisis = []
    datos_analisis = pedir_analisis_catalogo(lista_analisis)
    lista_analisis.append(datos_analisis)
    while True:
        if len(lista_analisis) == len(CATALOGO_ANALISIS):
            print("\nTodos los analisis del catalogo han sido registrados para la muestra")
            return lista_analisis
        opcion_usuario = input("¿Agregar otro análisis? (s/n): \n").strip().lower()
        if opcion_usuario == "s":
            datos_analisis = pedir_analisis_catalogo(lista_analisis)
            lista_analisis.append(datos_analisis)
        elif opcion_usuario == "n":
            break
        else:
            print("\nOpcion ingresada invalida, opciones posibles: S | N")
    return lista_analisis

def pedir_datos_muestra():
    cliente_muestra = elegir_codigo(CATALOGO_CLIENTES, "\nElegir codigo de cliente: ")
    descripcion_muestra = input("\nIngresar descripción de la muestra: ").strip()
    analisis_muestra = pedir_analisis()
    datos_muestra = {
        "cliente": cliente_muestra,
        "descripcion": descripcion_muestra,
        "analisis": analisis_muestra
    }
    return datos_muestra

def normalizar_codigo(texto, catalogo):
    """Limpia el texto ingresado y devuelve el código si existe en el catálogo, o None si no."""
    codigo = texto.strip().upper()
    return codigo if codigo in catalogo else None

def elegir_codigo(catalogo, titulo):
    """Muestra las opciones del catálogo y pide un código hasta que sea válido. Devuelve el código."""
    print(titulo)
    for codigo, datos in catalogo.items():
        nombre_elemento = datos["nombre"]
        print(f"\n{codigo}: {nombre_elemento}")
    while True:
        codigo_ingresado = input("\nIngresar un codigo valido en la lista: ").strip()
        if len(codigo_ingresado) == 0:
            print("\nEl codigo ingresado no puede estar vacio, favor digitar uno valido de la lista")
            continue
        codigo_normalizado = normalizar_codigo(codigo_ingresado,catalogo)
        if codigo_normalizado is None:
            print("\nEl codigo ingresado no se encuentra en la lista")
            print("\nFavor volver a intentar con un codigo valido en la lista")
            continue
        return codigo_normalizado

def unidad_desde_opcion(texto,unidades):
    opcion_usuario = texto.strip()
    if opcion_usuario.isdigit():
        opcion_transformada = int(opcion_usuario)
        if opcion_transformada <= 0 or opcion_transformada > len(unidades):
            return None
        unidad_elegida = unidades[opcion_transformada - 1]
        return unidad_elegida        
    return None

def elegir_unidad(unidades):
    """Muestra las unidades numeradas y pide una opción hasta que sea válida.
    Devuelve la unidad elegida."""
    print("\nLas unidades disponibles para este analisis son: ")
    for indice, unidad in enumerate(unidades, start=1):
        print(f"{indice}: [{unidad}]")
    print("\nSi necesita el reporte con otra unidad favor contactar a jefatura")
    while True:
        eleccion_usuario = input("Ingrese el numero que representa a la unidad que necesita: \n")
        eleccion_unidad = unidad_desde_opcion(eleccion_usuario, unidades)
        if eleccion_unidad is None:
            print("\nLa eleccion digitada no es valida")
            if len(unidades)==1:
                print("Favor ingresar 1 para elegir la unica unidad")
                continue
            print(f"\nFavor ingresar un numero entre 1 y {len(unidades)}")
            continue
        return eleccion_unidad

def pedir_analisis_catalogo(lista_analisis_agregados):
    while True:
        codigo_del_analisis = elegir_codigo(CATALOGO_ANALISIS, "\nSeleccione el análisis: ")
        if codigo_ya_agregado(lista_analisis_agregados, codigo_del_analisis):
            print("La muestra ya tiene registrado ese analisis, favor seleccionar otro")
            continue
        break
    datos_analisis = CATALOGO_ANALISIS[codigo_del_analisis]
    nombre_analisis = datos_analisis["nombre"]
    norma_analisis = datos_analisis["norma"]
    lista_unidad_analisis = datos_analisis["unidades"]
    unidad_seleccionada = elegir_unidad(lista_unidad_analisis)
    while True:
        limite_conteo = input("Ingrese el limite de conteo para el análisis: \n").strip()
        if limite_conteo.isdigit():
            limite_conteo = int(limite_conteo)
            break
        else:
            print("\nError: Limite de conteo debe ser un numero entero mayor o igual a 0")
            print("Ingresar nuevamente\n")
    analisis_final = {
        "codigo": codigo_del_analisis,
        "nombre": nombre_analisis,
        "norma": norma_analisis,
        "unidad": unidad_seleccionada,
        "limite": limite_conteo
    }
    return analisis_final

def codigo_ya_agregado(lista_analisis, codigo):
    return any(analisis["codigo"] == codigo for analisis in lista_analisis)

def buscar_muestra(lista_muestras, id_muestra):
    id_muestra = id_muestra.upper().replace(" ","")
    return next((muestra for muestra in lista_muestras if id_muestra == muestra.get("id")), None)

def siguiente_estado(estado_actual):
    if estado_actual not in ESTADOS_POSIBLES:
        return None
    indice = ESTADOS_POSIBLES.index(estado_actual)
    if indice == len(ESTADOS_POSIBLES)-1:
        return None
    return ESTADOS_POSIBLES[indice+1]
    
    
    for indice, estado in enumerate(ESTADOS_POSIBLES):
        if estado == estado_actual:
            if indice == len(ESTADOS_POSIBLES)-1:
                return None
            return ESTADOS_POSIBLES[indice+1]
    return None

def main():
    lista_muestras = [
        {
            "id": "M-0001", "cliente": "0042", "descripcion": "Jugo de naranja lote 55",
            "estado": "enviada", "fecha_ingreso": "2026-10-27",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                 "unidad": "UFC/ml", "limite": 10, "resultado": None},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                 "unidad": "UFC/ml", "limite": 100, "resultado": None},
            ],
        },
        {
            "id": "M-0002", "cliente": "0044", "descripcion": "Carne molida lote 12",
            "estado": "confirmada", "fecha_ingreso": "2026-10-27",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                 "unidad": "UFC/g", "limite": 100, "resultado": 250},
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                 "unidad": "UFC/ml", "limite": 50, "resultado": None},
            ],
        },
        {
            "id": "M-0003", "cliente": "0047", "descripcion": "Lechuga escarola",
            "estado": "liberada", "fecha_ingreso": "2026-10-26",
            "analisis": [
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                 "unidad": "UFC/g", "limite": 1000, "resultado": 0},
            ],
        },
        {
            "id": "M-0004", "cliente": "0042", "descripcion": "Néctar de durazno",
            "estado": "cancelada", "fecha_ingreso": "2026-10-28",
            "analisis": [
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                 "unidad": "UFC/ml", "limite": 10, "resultado": None},
            ],
        },
    ]
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            id_nuevo, errores = agregar_muestra(lista_muestras,pedir_datos_muestra())
            if errores:
                print("La muestra no ha podido ser creada")
                for error in errores:
                    print(f"ERROR AL CREAR LA MUESTRA: {error}")
                input("Presione enter para continuar...")
            else:
                print("\nMuestra agregada con exito")
                print(f"\nID de la muestra: {id_nuevo}")
                input("Presione enter para continuar...")
        elif opcion == "2":
            listar_muestras(lista_muestras)
            input("Presione enter para continuar...")
        elif opcion == "3":
            id_muestra=input("Digite el ID  de la muestra a buscar: \n")
            resultado_encontrado = buscar_muestra(lista_muestras, id_muestra)
            if resultado_encontrado is None:
                print("La muestra digitada no se encuentra registrada...")
                input("Presione enter para continuar...")
                continue
            listar_muestras([resultado_encontrado])
            input("Presione enter para continuar...")
        elif opcion == "4":
            print("\nAdios...")
            input("Presione enter para continuar...")
            break
        else:
            print("\nOpcion invalida, pruebe nuevamente")
            input("Presione enter para continuar...")

if __name__ == "__main__":
    main()
