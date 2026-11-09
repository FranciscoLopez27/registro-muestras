from datetime import date
import copy
from constants import (
    CATALOGO_CLIENTES, CATALOGO_ANALISIS,
    ESTADOS_POSIBLES, ESTADOS_CANCELABLES, ESTADOS_EN_ORDEN,
)


TEXTOS_EN_BASE_A_RESULTADOS = {None: "|| Especificación: pendiente", 
                            True: "|| Especificación: fuera",
                            False: "|| Especificación: dentro"
                            }


def muestras_de_ejemplo():
    """Devuelve una lista de muestras de ejemplo para probar el programa."""
    return [
        {
            "id": "M-0001", "cliente": "0042", "descripcion": "Jugo de naranja lote 55",
            "estado": "enviada", "fecha_ingreso": "2026-10-27",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/ml", "limite": 10, "resultado": None, "fuera_especificacion": None},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/ml", "limite": 100, "resultado": None, "fuera_especificacion": None},
            ],
        },
        {
            "id": "M-0002", "cliente": "0044", "descripcion": "Carne molida lote 12",
            "estado": "confirmada", "fecha_ingreso": "2026-10-27",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 250, "fuera_especificacion": True},
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                "unidad": "UFC/ml", "limite": 50, "resultado": None, "fuera_especificacion": None},
            ],
        },
        {
            "id": "M-0003", "cliente": "0047", "descripcion": "Lechuga escarola",
            "estado": "liberada", "fecha_ingreso": "2026-10-26",
            "analisis": [
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 0, "fuera_especificacion": False},
            ],
        },
        {
            "id": "M-0004", "cliente": "0042", "descripcion": "Néctar de durazno",
            "estado": "cancelada", "fecha_ingreso": "2026-10-28",
            "analisis": [
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                "unidad": "UFC/ml", "limite": 10, "resultado": None, "fuera_especificacion": None},
            ],
        },
    ]

def muestras_de_ejemplo_ampliadas():
    """Devuelve más muestras de ejemplo, con varias fuera de especificación, para probar a mano."""
    return muestras_de_ejemplo() + [
        {
            "id": "M-0005", "cliente": "0047", "descripcion": "Queso fresco lote 7",
            "estado": "confirmada", "fecha_ingreso": "2026-11-02",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 80, "fuera_especificacion": False},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 1500, "fuera_especificacion": True},
            ],
        },
        {
            "id": "M-0006", "cliente": "0044", "descripcion": "Hamburguesa de vacuno lote 3",
            "estado": "liberada", "fecha_ingreso": "2026-10-30",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 400, "fuera_especificacion": True},
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                "unidad": "UFC/ml", "limite": 50, "resultado": 120, "fuera_especificacion": True},
            ],
        },
        {
            "id": "M-0007", "cliente": "0042", "descripcion": "Yogur natural lote 21",
            "estado": "liberada", "fecha_ingreso": "2026-10-29",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 30, "fuera_especificacion": False},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 200, "fuera_especificacion": False},
            ],
        },
        {
            "id": "M-0008", "cliente": "0047", "descripcion": "Frutillas congeladas lote 9",
            "estado": "cancelada", "fecha_ingreso": "2026-11-01",
            "analisis": [
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 5000, "fuera_especificacion": True},
            ],
        },
    ]

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
        for analisis in nueva_muestra["analisis"]:
            analisis["resultado"] = None
            analisis["fuera_especificacion"] = None
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
                print(f"\n--> Nombre analisis: {analisis['nombre']} || Codigo: {analisis['codigo']} || Norma: {analisis['norma']} || "
                    f"Limite conteo: {analisis['limite']} || Unidad: {analisis['unidad']}")
                texto_resultado = "no registrado" if analisis["resultado"] is None else analisis["resultado"]
                print(f"\nResultado: {texto_resultado} {TEXTOS_EN_BASE_A_RESULTADOS[analisis['fuera_especificacion']]}")
            print("")
            print("-------------------O--------------------")
    return

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
    limite_conteo = pedir_entero("Ingrese el limite de conteo para el análisis: \n")
    
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

def tiene_resultado_pendiente(muestra):
    return any(analisis["resultado"] is None for analisis in muestra["analisis"])

def avanzar_estado(muestra):
    lista_errores = []
    estado_actual = muestra["estado"]
    nuevo_estado = siguiente_estado(estado_actual)
    if nuevo_estado is None:
        lista_errores.append(f"El estado actual de la muestra se encuentra {estado_actual}, por lo que no se puede modificar")
        return lista_errores
    if nuevo_estado == "liberada" and tiene_resultado_pendiente(muestra):
        lista_errores.append("No todos los analisis tienen resultado, por lo que no puede ser liberada")
    if len(lista_errores) == 0:
        muestra["estado"] = nuevo_estado
    return lista_errores

def cancelar_muestra(muestra):
    lista_errores = []
    estado_actual = muestra["estado"]
    if estado_actual not in ESTADOS_CANCELABLES:
        lista_errores.append(f"La muestra no puede ser cancelada ya que se encuentra en estado: {estado_actual}")
    if len(lista_errores) == 0:
        muestra["estado"] = "cancelada"
    return lista_errores

def pausar():
    input("Presione enter para continuar...")

def mostrar_errores(titulo, errores):
    print(titulo)
    for error in errores:
        print(error)

def pedir_muestra_existente(lista_muestras, mensaje):
    id_muestra=input(mensaje)
    resultado_encontrado = buscar_muestra(lista_muestras, id_muestra)
    if resultado_encontrado is None:
        print("La muestra digitada no se encuentra registrada...")
        pausar()
    return resultado_encontrado

def esta_fuera_de_especificacion(analisis):
    return analisis["resultado"] is not None and analisis["resultado"] > analisis["limite"]

def registrar_resultado(muestra, codigo_analisis, resultado):
    lista_errores = []
    if muestra["estado"] != "confirmada":
        lista_errores.append("La muestra debe estar en estado confirmada para asociarle resultados")
        return lista_errores
    if resultado < 0:
        lista_errores.append("El resultado tiene que ser un valor mayor o igual a 0")
    analisis_buscado = next((analisis for analisis in muestra["analisis"] if codigo_analisis == analisis.get("codigo")), None)
    if analisis_buscado is None:
        lista_errores.append("La muestra ingresada no tiene el analisis registrado")
    if len(lista_errores) != 0:
        return lista_errores
    analisis_buscado["resultado"] = resultado
    analisis_buscado["fuera_especificacion"] = esta_fuera_de_especificacion(analisis_buscado)
    return lista_errores
    
def pedir_entero(mensaje):
    while True:
        valor_entero = input(mensaje).strip()
        if valor_entero.isdigit():
            return int(valor_entero)
        print("\nError: Valor ingresado debe ser un numero entero mayor o igual a 0")
        print("Ingresar nuevamente\n")

def muestras_fuera_norma(lista_muestras):
    return [muestra for muestra in lista_muestras 
            if any(esta_fuera_de_especificacion(analisis) for analisis in muestra["analisis"])
    ]

def agrupar_por_estado(lista_muestras):
    por_estado = {}
    for muestra in lista_muestras:
        por_estado.setdefault(muestra["estado"], []).append(muestra)
    ordenado = {estado: por_estado[estado] for estado in ESTADOS_EN_ORDEN if estado in por_estado}
    return ordenado

def mostrar_menu():
    print("\n--------   Registro de muestras   --------")
    print("1. Agregar muestra")
    print("2. Listar muestras")
    print("3. Buscar muestra")
    print("4. Cambiar estado de muestra")
    print("5. Registrar resultado")
    print("6. Listar muestras fuera de especificación")
    print("7. Salir\n")

def opcion_agregar_muestra(lista_muestras):
    id_nuevo, errores = agregar_muestra(lista_muestras,pedir_datos_muestra())
    if errores:
        mostrar_errores("La muestra no ha podido ser creada", errores)
        
    else:
        print("\nMuestra agregada con exito")
        print(f"\nID de la muestra: {id_nuevo}")
    pausar()

def opcion_listar_muestras(lista_muestras):
    listar_muestras(lista_muestras)
    pausar()

def opcion_buscar_muestra(lista_muestras):
    muestra_encontrada = pedir_muestra_existente(lista_muestras, "Digite el ID  de la muestra a buscar: \n")
    if muestra_encontrada is None:
        return
    listar_muestras([muestra_encontrada])
    pausar()

def opcion_cambiar_estado(lista_muestras):
    muestra_encontrada = pedir_muestra_existente(lista_muestras, "Digite el ID de la muestra que se quiere modificar el estado: \n")
    if muestra_encontrada is None:
        return
    print(f"El estado actual de la muestra es: {muestra_encontrada['estado']}")
    print("¿Que desea realizar con el estado de la muestra?")
    opcion_estado = input("1. Avanzar a siguiente estado.\n"
    "2. Cancelar muestra.\n" 
    "3. Regresar.\n"
    "Digite la opcion que desea realizar: ").strip()
    if opcion_estado == "1":
        lista_errores = avanzar_estado(muestra_encontrada)
        if len(lista_errores) != 0:
            mostrar_errores("No se ha podido modificar el estado", lista_errores)
        else:
            print(f"El estado ha sido cambiado a {muestra_encontrada['estado']}")

    elif opcion_estado == "2":
        print(f"¿Está seguro de que desea cancelar la muestra {muestra_encontrada['id']}?")
        confirmacion=input("Esta acción no se puede deshacer y debe estar autorizada por jefatura. (s/n): ").strip().lower()
        if confirmacion == "s":
            lista_errores = cancelar_muestra(muestra_encontrada)
            if len(lista_errores) != 0:
                mostrar_errores("No se ha podido modificar el estado", lista_errores)
            else:
                print("La muestra ha sido cancelada correctamente")
        elif confirmacion == "n":
            print("No se continua el procedimiento de cancelación de la muestra")
        else:
            print("Opción no valida, volviendo al menu principal")
    
    elif opcion_estado == "3":
        print("Volviendo al menu principal")
    
    else:
        print("Opcion ingresada no valida, volviendo al menu")
    pausar()

def opcion_registrar_resultado(lista_muestras):
    muestra_encontrada = pedir_muestra_existente(lista_muestras, "Digite el ID de la muestra que quiere ingresar resultado: \n")
    if muestra_encontrada is None:
        return
    if muestra_encontrada["estado"] != "confirmada":
        print(f"Para reportar resultados la muestra debe estar en estado confirmada y se encuentra en estado: {muestra_encontrada["estado"]}")
        print("Favor modificar estado antes de reportar resultados")
        print("Si no es posible modificar estado, contactar con jefatura o cliente")
        pausar()
        return
    analisis_muestra = {analisis["codigo"]: analisis for analisis in muestra_encontrada["analisis"]}
    codigo_elegido = elegir_codigo(analisis_muestra, "Seleccione un codigo de los siguientes analisis de la muestra")
    resultado_ingresado = pedir_entero("Ingresar el valor del resultado del analisis:\n")
    errores = registrar_resultado(muestra_encontrada, codigo_elegido, resultado_ingresado)
    if len(errores) != 0:
        mostrar_errores("El resultado no ha podido ser registrado", errores)

    else:
        print(f"El resultado {resultado_ingresado} ha sido ingresado correctamente en el análisis {codigo_elegido}")
        if analisis_muestra[codigo_elegido]["fuera_especificacion"]:
            print(f"El resultado quedo fuera de especificación")       
        else:
            print(f"El resultado quedo dentro de especificación")
    pausar()
    return

def opcion_listar_fuera_de_norma(lista_muestras):
    muestras_fuera_especificacion = muestras_fuera_norma(lista_muestras)
    if len(muestras_fuera_especificacion) == 0:
        print("No se tiene ninguna muestra fuera de especificación en la base de datos")
        pausar()
        return
    for estado, muestras in agrupar_por_estado(muestras_fuera_especificacion).items():
        print(f"Muestras fuera de especificación en estado: {estado}")
        print("-------------------O--------------------")
        listar_muestras(muestras)
    pausar()


def main():
    lista_muestras = muestras_de_ejemplo_ampliadas()

    comandos = {
        "1": opcion_agregar_muestra,
        "2": opcion_listar_muestras,
        "3": opcion_buscar_muestra,
        "4": opcion_cambiar_estado,
        "5": opcion_registrar_resultado,
        "6": opcion_listar_fuera_de_norma
    }

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        if opcion in comandos:
            comandos[opcion](lista_muestras)
                
        elif opcion == "7":
            print("\nAdios...")
            pausar()
            break

        else:
            print("\nOpcion invalida, pruebe nuevamente")
            pausar()

if __name__ == "__main__":
    main()


