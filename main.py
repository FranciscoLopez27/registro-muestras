from formatters import (mostrar_menu, pausar, mostrar_alerta_cuarentena)
from controllers import(
    opcion_agregar_muestra, opcion_listar_muestras, opcion_buscar_muestra,
    opcion_cambiar_estado, opcion_registrar_resultado, opcion_listar_fuera_de_norma
)
from storage import guardar_muestras, cargar_muestras
from exceptions import ErrorIntegridad
from constants import RUTA_DATOS, OPCIONES_QUE_MODIFICAN

def main():
    try:
        lista_muestras, cuarentena = cargar_muestras(RUTA_DATOS)
        
    except ErrorIntegridad as error:
        print("Las muestras no pudieron ser cargadas:")
        print(f"{error}")
        return

    comandos = {
        "1": opcion_agregar_muestra,
        "2": opcion_listar_muestras,
        "3": opcion_buscar_muestra,
        "4": opcion_cambiar_estado,
        "5": opcion_registrar_resultado,
        "6": opcion_listar_fuera_de_norma
        }
    
    while True:
        mostrar_alerta_cuarentena(cuarentena)
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        if opcion in comandos:
            comandos[opcion](lista_muestras, cuarentena)
            if opcion in OPCIONES_QUE_MODIFICAN:
                guardar_muestras(lista_muestras, RUTA_DATOS, cuarentena)
                
        elif opcion == "7":
            print("\nAdios...")
            pausar()
            break

        else:
            print("\nOpcion invalida, pruebe nuevamente")
            pausar()

if __name__ == "__main__":
    main()


