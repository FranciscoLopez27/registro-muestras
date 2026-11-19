from models import Analisis, Muestra
from constants import CATALOGO_ANALISIS
from exceptions import (ErrorValor, ErrorNoEncontrado, ErrorEstado, ErrorLaboratorio)

ESTADOS_QUE_PASAN_POR_CONFIRMADA = ("confirmada", "liberada", "cancelada")


def crear_muestra_ejemplo(id_muestra, cliente, descripcion, fecha_ingreso, lista_analisis, estado_buscado):
    """Crea una muestra de ejemplo llevándola por el flujo real del laboratorio
    hasta el estado indicado, respetando todas las reglas de la clase Muestra.

    lista_analisis: lista de tuplas (codigo, unidad, limite, resultado).
        El nombre y la norma de cada análisis se toman de CATALOGO_ANALISIS.
        resultado puede ser None si el análisis no tiene resultado.
    estado_buscado: "enviada", "confirmada", "liberada" o "cancelada".

    Pasos: agrega los análisis mientras la muestra está enviada; si el estado
    buscado lo requiere, la confirma y registra los resultados que no son None;
    por último, la libera o la cancela según corresponda. Las muestras
    canceladas se cancelan después de confirmarlas, para conservar sus resultados.

    Si alguna regla impide llegar al estado buscado (por ejemplo, liberar con un
    resultado pendiente), muestra un aviso y devuelve la muestra en el estado
    al que alcanzó a llegar. Un código que no existe en el catálogo produce un
    KeyError, para detectar de inmediato una receta mal escrita.
    """
    muestra = Muestra(id_muestra, cliente, descripcion, fecha_ingreso)
    errores = []
    
    for codigo, unidad, limite, _ in lista_analisis:
        datos = CATALOGO_ANALISIS[codigo]
        nombre = datos["nombre"]
        norma = datos["norma"]
        errores.extend(muestra.agregar_analisis(Analisis(codigo, nombre, norma, unidad, limite)))

    if estado_buscado in ESTADOS_QUE_PASAN_POR_CONFIRMADA:
        errores.extend(muestra.avanzar_estado())
        for codigo, _, _, resultado in lista_analisis:
            if resultado is not None:
                try:
                    muestra.registrar_resultado(codigo, resultado)
                except ErrorLaboratorio as error:
                    errores.append(str(error))
                    
    if estado_buscado == "cancelada":
        errores.extend(muestra.cancelar())
    elif estado_buscado == "liberada":
        errores.extend(muestra.avanzar_estado())

    if errores:
        print(f"Aviso: la muestra de ejemplo {id_muestra} tuvo errores: {errores}")
    return muestra



def muestras_de_ejemplo():
    """Devuelve una lista de muestras de ejemplo para probar el programa."""
    return [
        crear_muestra_ejemplo("M-0001", "0042", "Jugo de naranja lote 55", "2026-10-27", 
                            [("A012", "UFC/ml", 10, None,), ("A019", "UFC/ml", 100, None)], "enviada"),
        crear_muestra_ejemplo("M-0002", "0044", "Carne molida lote 12", "2026-10-27", 
                            [("A012", "UFC/g", 100, 250), ("A013", "UFC/ml", 50, None)], "confirmada"),
        crear_muestra_ejemplo("M-0003", "0047", "Lechuga escarola", "2026-10-26", 
                            [("A019", "UFC/g", 1000, 0)], "liberada"),
        crear_muestra_ejemplo("M-0004", "0042", "Néctar de durazno", "2026-10-28", 
                            [("A013", "UFC/ml", 10, None)], "cancelada")
    ]

def muestras_de_ejemplo_ampliadas():
    """Devuelve más muestras de ejemplo, con varias fuera de especificación, para probar a mano."""
    return muestras_de_ejemplo() + [
        crear_muestra_ejemplo("M-0005", "0047", "Queso fresco lote 7", "2026-11-02", 
                            [("A012", "UFC/g", 100, 80),("A019", "UFC/g", 1000, 1500)], "confirmada"),
        crear_muestra_ejemplo("M-0006", "0044", "Hamburguesa de vacuno lote 3", "2026-10-30", 
                            [("A012", "UFC/g", 100, 400), ("A013", "UFC/ml", 50, 120)], "liberada"),
        crear_muestra_ejemplo("M-0007", "0042", "Yogur natural lote 21", "2026-10-29", 
                            [("A012", "UFC/g", 100, 30), ("A019", "UFC/g", 1000, 200)], "liberada"),
        crear_muestra_ejemplo("M-0008", "0047", "Frutillas congeladas lote 9", "2026-11-01", 
                            [("A019", "UFC/g", 1000, 5000)], "cancelada")
        ]
