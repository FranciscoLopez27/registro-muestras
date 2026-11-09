TEXTOS_EN_BASE_A_RESULTADOS = {None: "|| Especificación: pendiente", 
                            True: "|| Especificación: fuera",
                            False: "|| Especificación: dentro"
                            }

from constants import CATALOGO_CLIENTES

def listar_muestras(lista_muestras):
    if len(lista_muestras) == 0:
        print("\nNo se encuentran muestras registradas en la base de datos")
    else:
        for muestra in lista_muestras:
            codigo_cliente = muestra['cliente']
            nombre_cliente = CATALOGO_CLIENTES.get(codigo_cliente, {}).get('nombre', "Cliente desconocido")
            print(
                f"\nID: {muestra['id']} || Cliente: {codigo_cliente} - {nombre_cliente} || "
                f" Descripcion: {muestra['descripcion']} || Estado: {muestra['estado']} || Fecha: {muestra['fecha_ingreso']}\n"
                )
            print("Analisis asociados a la muestra: ")
            for analisis in muestra["analisis"]:
                print(f"\n--> Nombre analisis: {analisis['nombre']} || Codigo: {analisis['codigo']} || Norma: {analisis['norma']} || "
                    f"Limite conteo: {analisis['limite']} || Unidad: {analisis['unidad']}")
                texto_resultado = "no registrado" if analisis["resultado"] is None else analisis["resultado"]
                print(f"\nResultado: {texto_resultado} {TEXTOS_EN_BASE_A_RESULTADOS[analisis['fuera_especificacion']]}")
            print("")
            print("-------------------O--------------------")
    return

def mostrar_errores(titulo, errores):
    print(titulo)
    for error in errores:
        print(error)

def mostrar_menu():
    print("\n--------   Registro de muestras   --------")
    print("1. Agregar muestra")
    print("2. Listar muestras")
    print("3. Buscar muestra")
    print("4. Cambiar estado de muestra")
    print("5. Registrar resultado")
    print("6. Listar muestras fuera de especificación")
    print("7. Salir\n")

def pausar():
    input("Presione enter para continuar...")