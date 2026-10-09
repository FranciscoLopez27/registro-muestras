from datetime import date
import copy
from registro import generar_id, validar_muestra, agregar_muestra, listar_muestras

analisis_ok = [{"nombre": "Aerobios mesófilos", "limite": 10000, "unidad": "UFC/g"}, {"nombre": "Enterobacterias", "limite": 100, "unidad": "UFC/ml"}]
analisis_malo = [{"nombre": "", "limite": -5, "unidad": "kg"}]

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
limite_cero = [{"nombre": "Salmonella", "limite": 0, "unidad": "UFC/g"}]
assert validar_muestra({**datos_ok, "analisis": limite_cero}) == []   # 0 es válido
unidad_minuscula = [{"nombre": "Coliformes", "limite": 100, "unidad": "nmp/g"}]
assert validar_muestra({**datos_ok, "analisis": unidad_minuscula}) == []
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
    "cliente": "1234",
    "descripcion": "Queso fresco",
    "analisis": [{"nombre": "Coliformes", "limite": 100, "unidad": "NMP/g"}],
}
agregar_muestra(muestras, datos_otro)
datos_otro["analisis"].append({"nombre": "Hongos", "limite": 50, "unidad": "UFC/g"})
assert len(muestras[2]["analisis"]) == 1
print("agregar_muestra: todas las pruebas pasaron")

# ---------- listar_muestras (revisión visual) ----------
print("\n--- Listado con muestras ---")
listar_muestras(muestras)
print("\n--- Listado vacío ---")
listar_muestras([])