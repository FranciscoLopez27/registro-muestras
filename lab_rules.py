import copy
from datetime import date
from constants import (
    CATALOGO_CLIENTES, CATALOGO_ANALISIS, ESTADOS_POSIBLES, ESTADOS_CANCELABLES, ESTADOS_EN_ORDEN
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

