from sample_data import(muestras_de_ejemplo_ampliadas)
from formatters import (mostrar_menu, pausar)
from controllers import(
    opcion_agregar_muestra, opcion_listar_muestras, opcion_buscar_muestra,
    opcion_cambiar_estado, opcion_registrar_resultado, opcion_listar_fuera_de_norma
)

def main():
    lista_muestras = muestras_de_ejemplo_ampliadas()

    comandos = {
        "1": opcion_agregar_muestra,
        "2": opcion_listar_muestras,
        "3": opcion_buscar_muestra,
        "4": opcion_cambiar_estado,
        "5": opcion_registrar_resultado,
        "6": opcion_listar_fuera_de_norma
    }

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        if opcion in comandos:
            comandos[opcion](lista_muestras)
                
        elif opcion == "7":
            print("\nAdios...")
            pausar()
            break

        else:
            print("\nOpcion invalida, pruebe nuevamente")
            pausar()

if __name__ == "__main__":
    main()


