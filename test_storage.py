import json
import os
from storage import guardar_muestras, cargar_muestras
from sample_data import muestras_de_ejemplo
from exceptions import ErrorIntegridad

RUTA_PRUEBA = "prueba_storage.json"

def lanza(tipo_error, funcion, *argumentos):
    """Devuelve True si llamar a funcion(*argumentos) lanza un error del tipo indicado."""
    try:
        funcion(*argumentos)
    except tipo_error:
        return True
    return False

def escribir_archivo(contenido):
    """Escribe una lista de registros directamente en el archivo de prueba,
    simulando un archivo editado a mano."""
    with open(RUTA_PRUEBA, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, indent=4, ensure_ascii=False)


# ---------- Ida y vuelta ----------
originales = muestras_de_ejemplo()
guardar_muestras(originales, RUTA_PRUEBA)
cargadas, cuarentena = cargar_muestras(RUTA_PRUEBA)

assert len(cargadas) == len(originales)
assert cuarentena == []
for original, cargada in zip(originales, cargadas):
    assert cargada.a_diccionario() == original.a_diccionario()
print("Storage (ida y vuelta): pruebas pasaron")

# ---------- Archivo inexistente ----------
os.remove(RUTA_PRUEBA)
assert cargar_muestras(RUTA_PRUEBA) == ([],[])
print("Storage (archivo inexistente): pruebas pasaron")

# ---------- Registro dañado: va a la cuarentena ----------
valida = muestras_de_ejemplo()[0].a_diccionario()
danada = muestras_de_ejemplo()[1].a_diccionario()
danada["estado"] = "perdida"
escribir_archivo([valida, danada])

cargadas, cuarentena = cargar_muestras(RUTA_PRUEBA)
assert len(cargadas) == 1
assert cargadas[0].id_muestra == valida["id_muestra"]
assert cuarentena == [danada]
print("Storage (registro dañado en cuarentena): pruebas pasaron")

# ---------- La cuarentena sobrevive al guardado ----------
guardar_muestras(cargadas, RUTA_PRUEBA, cuarentena)
cargadas, cuarentena = cargar_muestras(RUTA_PRUEBA)
assert len(cargadas) == 1
assert cuarentena == [danada]
print("Storage (la cuarentena sobrevive al guardado): pruebas pasaron")

# ---------- Archivo dañado: no se puede leer ----------
with open(RUTA_PRUEBA, "w", encoding="utf-8") as archivo:
    archivo.write('[{"id_muestra": "M-0001", ')      # JSON cortado a la mitad
assert lanza(ErrorIntegridad, cargar_muestras, RUTA_PRUEBA)
print("Storage (archivo dañado): pruebas pasaron")

os.remove(RUTA_PRUEBA)