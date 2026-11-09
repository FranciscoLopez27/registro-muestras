from datetime import date
from lab_rules import(
    generar_id, validar_muestra, siguiente_estado, tiene_resultado_pendiente,
    esta_fuera_de_especificacion, normalizar_codigo, unidad_desde_opcion,
    codigo_ya_agregado, buscar_muestra, avanzar_estado, cancelar_muestra,
    registrar_resultado, muestras_fuera_norma, agrupar_por_estado,
)
from controllers import(agregar_muestra)
from constants import(CATALOGO_CLIENTES, CATALOGO_ANALISIS,)

from sample_data import(muestras_de_ejemplo)
from formatters import listar_muestras

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
assert muestras[0]["estado"] == "enviada"
assert muestras[0]["cliente"] == "0042"
assert muestras[0]["fecha_ingreso"] == date.today().isoformat()

# Datos inválidos: no se agrega
id_nuevo, errores = agregar_muestra(muestras, {**datos_ok, "cliente": "99"})
assert id_nuevo is None and len(errores) == 1
assert len(muestras) == 1

# Mismo diccionario dos veces: deben ser muestras distintas
id_nuevo, _ = agregar_muestra(muestras, datos_ok)
assert id_nuevo == "M-0002"
assert muestras[0]["id"] == "M-0001"          # la primera no cambió
assert "id" not in datos_ok                   # los datos originales no se modificaron

# Copia profunda: cambiar los datos originales no altera la muestra registrada
datos_otro = {
    "cliente": "0044",
    "descripcion": "Queso fresco",
    "analisis": [{"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832", "unidad": "UFC/ml", "limite": 100}],
}
agregar_muestra(muestras, datos_otro)
datos_otro["analisis"].append({"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidad": "UFC/g", "limite": 100})
assert len(muestras[2]["analisis"]) == 1
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
assert buscar_muestra(muestras, "M-0002")["id"] == "M-0002"
assert buscar_muestra(muestras, "m-0002")["id"] == "M-0002"     # minúsculas
assert buscar_muestra(muestras, " M-0002 ")["id"] == "M-0002"   # espacios en los extremos
assert buscar_muestra(muestras, "M- 0002")["id"] == "M-0002"    # espacio en el medio
assert buscar_muestra(muestras, "M-9999") is None               # no existe
assert buscar_muestra(muestras, "") is None                     # vacío
assert buscar_muestra([], "M-0001") is None                     # lista vacía
print("buscar_muestra: todas las pruebas pasaron")

# ---------- siguiente_estado ----------
assert siguiente_estado("enviada") == "confirmada"
assert siguiente_estado("confirmada") == "liberada"
assert siguiente_estado("liberada") is None       # último estado
assert siguiente_estado("cancelada") is None      # fuera de la secuencia
assert siguiente_estado("desconocido") is None
print("siguiente_estado: todas las pruebas pasaron")

assert all(analisis["resultado"] is None for analisis in muestras[0]["analisis"])

# ---------- tiene_resultado_pendiente ----------
ejemplos = muestras_de_ejemplo()

assert tiene_resultado_pendiente(ejemplos[0]) is True    # M-0001: ningún resultado
assert tiene_resultado_pendiente(ejemplos[1]) is True    # M-0002: uno con resultado y otro pendiente
assert tiene_resultado_pendiente(ejemplos[2]) is False   # M-0003: resultado 0, no está pendiente
assert tiene_resultado_pendiente(ejemplos[3]) is True    # M-0004: ningún resultado

# Todos los análisis con resultado
completa = ejemplos[1]
completa["analisis"][1]["resultado"] = 30
assert tiene_resultado_pendiente(completa) is False
print("tiene_resultado_pendiente: todas las pruebas pasaron")

# ---------- avanzar_estado ----------
ejemplos = muestras_de_ejemplo()
enviada, confirmada, liberada, cancelada = ejemplos

# Enviada → confirmada
assert avanzar_estado(enviada) == []
assert enviada["estado"] == "confirmada"

# Confirmada con un resultado pendiente: no se puede liberar
assert len(avanzar_estado(confirmada)) == 1
assert confirmada["estado"] == "confirmada"

# Confirmada con todos los resultados: se libera
confirmada["analisis"][1]["resultado"] = 30
assert avanzar_estado(confirmada) == []
assert confirmada["estado"] == "liberada"

# Liberada: no puede avanzar
assert len(avanzar_estado(liberada)) == 1
assert liberada["estado"] == "liberada"

# Cancelada: no puede avanzar
assert len(avanzar_estado(cancelada)) == 1
assert cancelada["estado"] == "cancelada"
print("avanzar_estado: todas las pruebas pasaron")

# ---------- cancelar_muestra ----------
enviada, confirmada, liberada, cancelada = muestras_de_ejemplo()

assert cancelar_muestra(enviada) == []
assert enviada["estado"] == "cancelada"

assert cancelar_muestra(confirmada) == []
assert confirmada["estado"] == "cancelada"

assert len(cancelar_muestra(liberada)) == 1
assert liberada["estado"] == "liberada"

assert len(cancelar_muestra(cancelada)) == 1
assert cancelada["estado"] == "cancelada"
print("cancelar_muestra: todas las pruebas pasaron")

# ---------- esta_fuera_de_especificacion ----------
def analisis_con(resultado, limite=100):
    return {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
            "unidad": "UFC/g", "limite": limite, "resultado": resultado}

assert esta_fuera_de_especificacion(analisis_con(250)) is True     # supera el límite
assert esta_fuera_de_especificacion(analisis_con(100)) is False    # igual al límite
assert esta_fuera_de_especificacion(analisis_con(0)) is False      # recuento 0
assert esta_fuera_de_especificacion(analisis_con(None)) is False   # sin resultado
assert esta_fuera_de_especificacion(analisis_con(1, limite=0)) is True   # límite 0
print("esta_fuera_de_especificacion: todas las pruebas pasaron")

# ---------- registrar_resultado ----------
enviada, confirmada, liberada, cancelada = muestras_de_ejemplo()

def analisis_de(muestra, codigo):
    return next(analisis for analisis in muestra["analisis"] if analisis["codigo"] == codigo)

# Registrar un resultado dentro de especificación
assert registrar_resultado(confirmada, "A013", 30) == []
assert analisis_de(confirmada, "A013")["resultado"] == 30
assert analisis_de(confirmada, "A013")["fuera_especificacion"] is False

# Registrar un resultado fuera de especificación
assert registrar_resultado(confirmada, "A012", 500) == []
assert analisis_de(confirmada, "A012")["resultado"] == 500
assert analisis_de(confirmada, "A012")["fuera_especificacion"] is True

# Corregir un resultado: el fuera de especificación se recalcula
assert registrar_resultado(confirmada, "A012", 50) == []
assert analisis_de(confirmada, "A012")["fuera_especificacion"] is False

# Código que no pertenece a la muestra
assert len(registrar_resultado(confirmada, "A019", 10)) == 1

# Resultado negativo: no se modifica el valor anterior
assert len(registrar_resultado(confirmada, "A013", -5)) == 1
assert analisis_de(confirmada, "A013")["resultado"] == 30

# Varios errores a la vez: negativo y código inexistente
assert len(registrar_resultado(confirmada, "A019", -5)) == 2

# Muestra enviada: aún no se pueden registrar resultados
assert len(registrar_resultado(enviada, "A012", 10)) == 1
assert analisis_de(enviada, "A012")["resultado"] is None

# Muestra liberada: los resultados están bloqueados
assert len(registrar_resultado(liberada, "A019", 5)) == 1
assert analisis_de(liberada, "A019")["resultado"] == 0
print("registrar_resultado: todas las pruebas pasaron")

# ---------- muestras_fuera_norma ----------
def muestra_con(id_muestra, estado, analisis):
    return {"id": id_muestra, "cliente": "0042", "descripcion": "Prueba",
            "estado": estado, "fecha_ingreso": "2026-11-05", "analisis": analisis}

def ids(muestras):
    return [muestra["id"] for muestra in muestras]

# Con las muestras de ejemplo, solo M-0002 tiene un resultado fuera (250 con límite 100)
assert ids(muestras_fuera_norma(muestras_de_ejemplo())) == ["M-0002"]

# Se incluyen sin importar el estado, incluidas liberadas y canceladas
liberada_fuera = muestra_con("M-0101", "liberada", [analisis_con(500)])
cancelada_fuera = muestra_con("M-0102", "cancelada", [analisis_con(500)])
dentro = muestra_con("M-0103", "confirmada", [analisis_con(50)])
assert ids(muestras_fuera_norma([liberada_fuera, dentro, cancelada_fuera])) == ["M-0101", "M-0102"]

# Dos análisis fuera de especificación: la muestra aparece una sola vez
doble_fuera = muestra_con("M-0104", "confirmada", [analisis_con(500), analisis_con(300)])
assert ids(muestras_fuera_norma([doble_fuera])) == ["M-0104"]

# Sin resultado no cuenta como fuera de norma
pendiente = muestra_con("M-0105", "confirmada", [analisis_con(None)])
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

# Los estados sin muestras no aparecen
solo_liberadas = [muestra_con("M-0201", "liberada", []), muestra_con("M-0202", "liberada", [])]
assert list(agrupar_por_estado(solo_liberadas)) == ["liberada"]
assert ids(agrupar_por_estado(solo_liberadas)["liberada"]) == ["M-0201", "M-0202"]

# Lista vacía
assert agrupar_por_estado([]) == {}
print("agrupar_por_estado: todas las pruebas pasaron")