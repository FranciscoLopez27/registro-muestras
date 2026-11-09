from formatters import (pausar)
from lab_rules import(
    normalizar_codigo, unidad_desde_opcion, codigo_ya_agregado, buscar_muestra
)
from constants import (CATALOGO_CLIENTES, CATALOGO_ANALISIS,)



def pedir_entero(mensaje):
    while True:
        valor_entero = input(mensaje).strip()
        if valor_entero.isdigit():
            return int(valor_entero)
        print("\nError: Valor ingresado debe ser un numero entero mayor o igual a 0")
        print("Ingresar nuevamente\n")

def pedir_muestra_existente(lista_muestras, mensaje):
    id_muestra=input(mensaje)
    resultado_encontrado = buscar_muestra(lista_muestras, id_muestra)
    if resultado_encontrado is None:
        print("La muestra digitada no se encuentra registrada...")
        pausar()
    return resultado_encontrado

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