import json

def guardar_muestras(lista_muestras, ruta):
    """Guarda la lista de muestras en un archivo JSON, en la ruta indicada.

    Cada muestra se convierte a diccionario con su método a_diccionario.
    Si el archivo ya existe, se reemplaza completo.
    """
    lista_diccionarios_muestras = [muestra.a_diccionario() for muestra in lista_muestras]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(lista_diccionarios_muestras, archivo, indent=4, ensure_ascii=False)