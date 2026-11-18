from datetime import date
from lab_rules import(
    generar_id, validar_muestra, normalizar_codigo, unidad_desde_opcion,
    codigo_ya_agregado, buscar_muestra, muestras_fuera_norma, agrupar_por_estado, agregar_muestra
)
from constants import(CATALOGO_CLIENTES, CATALOGO_ANALISIS,)
from formatters import listar_muestras
from sample_data import(muestras_de_ejemplo, crear_muestra_ejemplo)

analisis_ok = [
    {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidad": "UFC/g", "limite": 100},
    {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2", "unidad": "UFC/ml", "limite": 1000},
]
analisis_malo = [{"codigo": "A099", "nombre": "", "norma": "", "unidad": "kg", "limite": -5}]

datos_ok = {
    "cliente": "0042",
    "descripcion": "Leche entera lote 123",
    "analisis": analisis_ok,
}

assert generar_id(1) == "M-0001"
assert generar_id(42) == "M-0042"
print("generar_id: todas las pruebas pasaron")

assert validar_muestra(datos_ok) == []

# Cliente: un solo error por causa
assert len(validar_muestra({**datos_ok, "cliente": "99"})) == 1      # largo incorrecto
assert len(validar_muestra({**datos_ok, "cliente": "12a4"})) == 1    # no numérico
assert len(validar_muestra({**datos_ok, "cliente": "9999"})) == 1    # no registrado

# Descripción
assert len(validar_muestra({**datos_ok, "descripcion": ""})) == 1
assert len(validar_muestra({**datos_ok, "descripcion": "   "})) == 1  # solo espacios

# Análisis
assert len(validar_muestra({**datos_ok, "analisis": []})) == 1        # sin análisis
assert len(validar_muestra({**datos_ok, "analisis": analisis_malo})) == 3
assert len(validar_muestra({**datos_ok, "cliente": "99", "analisis": analisis_malo})) == 4

# Casos válidos en el borde
limite_cero = [{"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2", "unidad": "UFC/g", "limite": 0}]
assert validar_muestra({**datos_ok, "analisis": limite_cero}) == []   # 0 es válido

# Unidades según el análisis
coliformes_ok = [{"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832", "unidad": "UFC/ml", "limite": 100}]
coliformes_mal = [{"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832", "unidad": "UFC/g", "limite": 100}]
assert validar_muestra({**datos_ok, "analisis": coliformes_ok}) == []
assert len(validar_muestra({**datos_ok, "analisis": coliformes_mal})) == 1   # unidad no permitida para ese análisis

# Código de análisis inexistente
codigo_inexistente = [{"codigo": "A099", "nombre": "Desconocido", "norma": "", "unidad": "UFC/g", "limite": 10}]
assert len(validar_muestra({**datos_ok, "analisis": codigo_inexistente})) == 1

# Análisis repetido
repetido = [analisis_ok[0], analisis_ok[0]]
assert len(validar_muestra({**datos_ok, "analisis": repetido})) == 1
print("validar_muestra: todas las pruebas pasaron")

# ---------- agregar_muestra ----------
muestras = []

id_nuevo, errores = agregar_muestra(muestras, datos_ok)
assert id_nuevo == "M-0001" and errores == []
assert len(muestras) == 1
assert muestras[0].estado == "enviada"
assert muestras[0].cliente == "0042"
assert muestras[0].fecha_ingreso == date.today().isoformat()

# Datos inválidos: no se agrega
id_nuevo, errores = agregar_muestra(muestras, {**datos_ok, "cliente": "99"})
assert id_nuevo is None and len(errores) == 1
assert len(muestras) == 1

# Mismo diccionario dos veces: deben ser muestras distintas
id_nuevo, _ = agregar_muestra(muestras, datos_ok)
assert id_nuevo == "M-0002"
assert muestras[0].id_muestra == "M-0001"          # la primera no cambió
assert "id" not in datos_ok                   # los datos originales no se modificaron

datos_otro = {
    "cliente": "0044",
    "descripcion": "Queso fresco",
    "analisis": [{"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832", "unidad": "UFC/ml", "limite": 100}],
}
agregar_muestra(muestras, datos_otro)
datos_otro["analisis"].append({"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidad": "UFC/g", "limite": 100})
assert len(muestras[2].analisis) == 1
print("agregar_muestra: todas las pruebas pasaron")

# ---------- listar_muestras (revisión visual) ----------
print("\n--- Listado con muestras ---")
listar_muestras(muestras)
print("\n--- Listado vacío ---")
listar_muestras([])

assert normalizar_codigo("A012", CATALOGO_ANALISIS) == "A012"     # válido
assert normalizar_codigo("a012", CATALOGO_ANALISIS) == "A012"     # minúsculas
assert normalizar_codigo("  A012  ", CATALOGO_ANALISIS) == "A012" # espacios
assert normalizar_codigo("A099", CATALOGO_ANALISIS) is None       # no existe
assert normalizar_codigo("", CATALOGO_ANALISIS) is None           # vacío
assert normalizar_codigo("   ", CATALOGO_ANALISIS) is None        # solo espacios
assert normalizar_codigo("0044", CATALOGO_CLIENTES) == "0044"     # sirve para clientes
print("normalizar_codigo: todas las pruebas pasaron")

# ---------- unidad_desde_opcion ----------
unidades = ["UFC/g", "UFC/ml"]

assert unidad_desde_opcion("1", unidades) == "UFC/g"
assert unidad_desde_opcion("2", unidades) == "UFC/ml"
assert unidad_desde_opcion(" 2 ", unidades) == "UFC/ml"    # espacios
assert unidad_desde_opcion("3", unidades) is None          # fuera de rango
assert unidad_desde_opcion("0", unidades) is None
assert unidad_desde_opcion("-1", unidades) is None         # negativo
assert unidad_desde_opcion("UFC/g", unidades) is None      # no es un número
assert unidad_desde_opcion("", unidades) is None           # vacío
assert unidad_desde_opcion("1", ["UFC/ml"]) == "UFC/ml"    # una sola unidad
print("unidad_desde_opcion: todas las pruebas pasaron")


# ---------- codigo_ya_agregado ----------
agregados = [
    {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidad": "UFC/g", "limite": 100},
    {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2", "unidad": "UFC/g", "limite": 500},
]

assert codigo_ya_agregado([], "A012") is False          # lista vacía
assert codigo_ya_agregado(agregados, "A012") is True    # presente
assert codigo_ya_agregado(agregados, "A019") is True    # presente, no en la primera posición
assert codigo_ya_agregado(agregados, "A013") is False   # ausente
assert codigo_ya_agregado(agregados, "A01") is False    # parecido, pero no igual
print("codigo_ya_agregado: todas las pruebas pasaron")

# ---------- buscar_muestra ----------
assert buscar_muestra(muestras, "M-0002").id_muestra == "M-0002"
assert buscar_muestra(muestras, "m-0002").id_muestra == "M-0002"     # minúsculas
assert buscar_muestra(muestras, " M-0002 ").id_muestra == "M-0002"   # espacios en los extremos
assert buscar_muestra(muestras, "M- 0002").id_muestra == "M-0002"    # espacio en el medio
assert buscar_muestra(muestras, "M-9999") is None               # no existe
assert buscar_muestra(muestras, "") is None                     # vacío
assert buscar_muestra([], "M-0001") is None                     # lista vacía
print("buscar_muestra: todas las pruebas pasaron")

# ---------- Funciones auxiliares ----------
def muestra_con(id_muestra, estado, analisis):
    """Crea una muestra de prueba llevándola por el flujo real hasta el estado indicado.
    analisis: lista de tuplas (codigo, unidad, limite, resultado)."""
    return crear_muestra_ejemplo(id_muestra, "0042", "Prueba", "2026-11-05", analisis, estado)

def ids(muestras):
    return [muestra.id_muestra for muestra in muestras]

# ---------- muestras_fuera_norma ----------
# Con las muestras de ejemplo, solo M-0002 tiene un resultado fuera (250 con límite 100)
assert ids(muestras_fuera_norma(muestras_de_ejemplo())) == ["M-0002"]

# Se incluyen sin importar el estado, incluidas liberadas y canceladas
liberada_fuera = muestra_con("M-0101", "liberada", [("A012", "UFC/g", 100, 500)])
cancelada_fuera = muestra_con("M-0102", "cancelada", [("A012", "UFC/g", 100, 500)])
dentro = muestra_con("M-0103", "confirmada", [("A012", "UFC/g", 100, 50)])
assert ids(muestras_fuera_norma([liberada_fuera, dentro, cancelada_fuera])) == ["M-0101", "M-0102"]

# Dos análisis fuera de especificación: la muestra aparece una sola vez
doble_fuera = muestra_con("M-0104", "confirmada",
                        [("A012", "UFC/g", 100, 500), ("A019", "UFC/g", 1000, 1500)])
assert ids(muestras_fuera_norma([doble_fuera])) == ["M-0104"]

# Sin resultado no cuenta como fuera de norma
pendiente = muestra_con("M-0105", "confirmada", [("A012", "UFC/g", 100, None)])
assert muestras_fuera_norma([pendiente]) == []

# Lista vacía
assert muestras_fuera_norma([]) == []
print("muestras_fuera_norma: todas las pruebas pasaron")

# ---------- agrupar_por_estado ----------
ejemplos = muestras_de_ejemplo()
grupos = agrupar_por_estado(ejemplos)
assert list(grupos) == ["enviada", "confirmada", "liberada", "cancelada"]
assert ids(grupos["confirmada"]) == ["M-0002"]

# El orden de los grupos no depende del orden de la lista
grupos_invertidos = agrupar_por_estado(list(reversed(ejemplos)))
assert list(grupos_invertidos) == ["enviada", "confirmada", "liberada", "cancelada"]

# Los estados sin muestras no aparecen (cada muestra necesita un análisis con resultado para liberarse)
solo_liberadas = [muestra_con("M-0201", "liberada", [("A012", "UFC/g", 100, 10)]),
                muestra_con("M-0202", "liberada", [("A012", "UFC/g", 100, 10)])]
assert list(agrupar_por_estado(solo_liberadas)) == ["liberada"]
assert ids(agrupar_por_estado(solo_liberadas)["liberada"]) == ["M-0201", "M-0202"]

# Lista vacía
assert agrupar_por_estado([]) == {}
print("agrupar_por_estado: todas las pruebas pasaron")