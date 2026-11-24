import json
from exceptions import ErrorIntegridad
from models import Muestra
def guardar_muestras(lista_muestras, ruta, lista_cuarentena=()):
    """Guarda las muestras y los registros en cuarentena en un archivo JSON.

    Cada muestra se convierte a diccionario con su método a_diccionario.
    Los registros en cuarentena se escriben sin modificar, en la misma lista,
    para que nunca se pierdan y vuelvan a la cuarentena en la próxima carga.
    Si el archivo ya existe, se reemplaza completo.
    """
    lista_diccionarios_muestras = [muestra.a_diccionario() for muestra in lista_muestras]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(lista_diccionarios_muestras + list(lista_cuarentena), archivo, indent=4, ensure_ascii=False)

def cargar_muestras(ruta):
    """Carga las muestras desde un archivo JSON.

    Devuelve una tupla (muestras, cuarentena): las muestras restauradas y
    los registros que no pasaron la validación de integridad, sin modificar.
    Si el archivo no existe, devuelve dos listas vacías.
    Lanza ErrorIntegridad si el archivo está dañado y no se puede leer.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
    except FileNotFoundError:
        return [], []
    except json.JSONDecodeError:
        raise ErrorIntegridad(f"El archivo {ruta} está dañado y no se puede leer. Revíselo antes de continuar.")

    muestras = []
    cuarentena = []
    for registro in registros:
        try:
            muestras.append(Muestra.desde_diccionario(registro))
        except (ErrorIntegridad, KeyError, TypeError):
            cuarentena.append(registro)
    return muestras, cuarentena