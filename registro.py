from lab_rules import(
    normalizar_codigo, unidad_desde_opcion, codigo_ya_agregado,
    buscar_muestra, agregar_muestra, avanzar_estado, cancelar_muestra,
    registrar_resultado, muestras_fuera_norma, agrupar_por_estado
)
from constants import (
    CATALOGO_CLIENTES, CATALOGO_ANALISIS,
    ESTADOS_POSIBLES, ESTADOS_CANCELABLES, ESTADOS_EN_ORDEN,
)

from sample_data import(
    muestras_de_ejemplo, muestras_de_ejemplo_ampliadas
)

from formatters import (
    listar_muestras, mostrar_errores, mostrar_menu, pausar
)


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


def pedir_muestra_existente(lista_muestras, mensaje):
    id_muestra=input(mensaje)
    resultado_encontrado = buscar_muestra(lista_muestras, id_muestra)
    if resultado_encontrado is None:
        print("La muestra digitada no se encuentra registrada...")
        pausar()
    return resultado_encontrado

def pedir_entero(mensaje):
    while True:
        valor_entero = input(mensaje).strip()
        if valor_entero.isdigit():
            return int(valor_entero)
        print("\nError: Valor ingresado debe ser un numero entero mayor o igual a 0")
        print("Ingresar nuevamente\n")



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


