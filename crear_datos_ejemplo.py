import os
from sample_data import muestras_de_ejemplo_ampliadas
from storage import guardar_muestras
from inputs import pedir_si_no
from constants import RUTA_DATOS

if os.path.exists(RUTA_DATOS):
    if not pedir_si_no(f"El archivo {RUTA_DATOS} ya existe y se reemplazará por las muestras de ejemplo. ¿Continuar?"):
        print("No se modificó el archivo.")
        exit()

guardar_muestras(muestras_de_ejemplo_ampliadas(), RUTA_DATOS)
print(f"Muestras de ejemplo guardadas en {RUTA_DATOS}.")