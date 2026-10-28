from datetime import date
from registro import (
    generar_id, validar_muestra, agregar_muestra, listar_muestras,
    normalizar_codigo, unidad_desde_opcion, CATALOGO_CLIENTES, CATALOGO_ANALISIS, codigo_ya_agregado
)

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