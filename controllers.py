from lab_rules import(
    agregar_muestra, avanzar_estado, cancelar_muestra,
    registrar_resultado, muestras_fuera_norma, agrupar_por_estado
)
from formatters import (
    listar_muestras, mostrar_errores, pausar
)
from inputs import(
    pedir_datos_muestra, pedir_muestra_existente, 
    elegir_codigo, pedir_entero, pedir_si_no
)

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
        if pedir_si_no("Esta acción no se puede deshacer y debe estar autorizada por jefatura."):
            lista_errores = cancelar_muestra(muestra_encontrada)
            if len(lista_errores) != 0:
                mostrar_errores("No se ha podido modificar el estado", lista_errores)
            else:
                print("La muestra ha sido cancelada correctamente")
        else:
            print("No se continua el procedimiento de cancelación de la muestra")
    
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