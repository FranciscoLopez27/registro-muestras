from models import (Analisis, Muestra)
from constants import (
    CATALOGO_CLIENTES, CATALOGO_ANALISIS, ESTADOS_EN_ORDEN
    )


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
    """Registra una muestra nueva a partir de los datos ingresados por el usuario.

    datos_muestra: diccionario con el cliente, la descripción y la lista de
    análisis (cada uno con código, nombre, norma, unidad y límite).

    Primero valida los datos con validar_muestra. Si son válidos, construye un
    objeto Muestra con un id nuevo y le agrega cada análisis como objeto
    Analisis, mediante agregar_analisis. La muestra queda en estado "enviada",
    con la fecha de ingreso de hoy, y se agrega a lista_muestras.

    Devuelve una tupla (id, errores): el id de la muestra nueva y una lista
    vacía si se registró, o (None, errores) si los datos no son válidos.

    Los errores de agregar_analisis no se atrapan: como validar_muestra ya
    revisó los datos, si ocurrieran indicarían un error del programa.
    """
    lista_errores = validar_muestra(datos_muestra)
    if not lista_errores:
        id_muestra = generar_id(len(lista_muestras)+1)
        nueva_muestra = Muestra(id_muestra, datos_muestra["cliente"], datos_muestra["descripcion"])
        for analisis in datos_muestra["analisis"]:
            nuevo_analisis = Analisis(analisis["codigo"], analisis["nombre"], analisis["norma"],
                                    analisis["unidad"], analisis["limite"])
            nueva_muestra.agregar_analisis(nuevo_analisis)
        lista_muestras.append(nueva_muestra)
        return(nueva_muestra.id_muestra, lista_errores)
    return(None, lista_errores)

def normalizar_codigo(texto, catalogo):
    """Limpia el texto ingresado y devuelve el código si existe en el catálogo, o None si no."""
    codigo = texto.strip().upper()
    return codigo if codigo in catalogo else None

def unidad_desde_opcion(texto,unidades):
    opcion_usuario = texto.strip()
    if opcion_usuario.isdigit():
        opcion_transformada = int(opcion_usuario)
        if opcion_transformada <= 0 or opcion_transformada > len(unidades):
            return None
        unidad_elegida = unidades[opcion_transformada - 1]
        return unidad_elegida        
    return None

def codigo_ya_agregado(lista_analisis, codigo):
    return any(analisis["codigo"] == codigo for analisis in lista_analisis)

def buscar_muestra(lista_muestras, id_muestra):
    id_muestra = id_muestra.upper().replace(" ","")
    return next((muestra for muestra in lista_muestras if id_muestra == muestra.id_muestra), None)

def muestras_fuera_norma(lista_muestras):
    return [muestra for muestra in lista_muestras 
            if any(analisis.fuera_especificacion for analisis in muestra.analisis)]

def agrupar_por_estado(lista_muestras):
    por_estado = {}
    for muestra in lista_muestras:
        por_estado.setdefault(muestra.estado, []).append(muestra)
    ordenado = {estado: por_estado[estado] for estado in ESTADOS_EN_ORDEN if estado in por_estado}
    return ordenado

