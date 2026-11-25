TEXTOS_EN_BASE_A_RESULTADOS = {None: "|| Especificación: pendiente", 
                            True: "|| Especificación: fuera",
                            False: "|| Especificación: dentro"
                            }

from constants import CATALOGO_CLIENTES, RUTA_DATOS

def listar_muestras(lista_muestras):
    if not lista_muestras:
        print("\nNo se encuentran muestras registradas en la base de datos")
    else:
        for muestra in lista_muestras:
            codigo_cliente = muestra.cliente
            nombre_cliente = CATALOGO_CLIENTES.get(codigo_cliente, {}).get('nombre', "Cliente desconocido")
            print(
                f"\nID: {muestra.id_muestra} || Cliente: {codigo_cliente} - {nombre_cliente} || "
                f" Descripcion: {muestra.descripcion} || Estado: {muestra.estado} || Fecha: {muestra.fecha_ingreso}\n"
                )
            print("Analisis asociados a la muestra: ")
            for analisis in muestra.analisis:
                print(f"\n--> Nombre analisis: {analisis.nombre} || Codigo: {analisis.codigo} || Norma: {analisis.norma} || "
                    f"Limite conteo: {analisis.limite} || Unidad: {analisis.unidad}")
                texto_resultado = "no registrado" if analisis.resultado is None else analisis.resultado
                print(f"\nResultado: {texto_resultado} {TEXTOS_EN_BASE_A_RESULTADOS[analisis.fuera_especificacion]}")
            print("")
            print("-------------------O--------------------")

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

def mostrar_alerta_cuarentena(cuarentena):
    if not cuarentena:
        return
    largo_registro_cuarentena = len(cuarentena)
    if largo_registro_cuarentena == 1:
        print(f"!!! ATENCIÓN: {largo_registro_cuarentena} registro en cuarentena !!!")
    else:
        print(f"!!! ATENCIÓN: {largo_registro_cuarentena} registros en cuarentena !!!")
    print("Los siguientes registros del archivo de datos no pasaron la validación")
    print("y no se cargaron. Se conservan sin cambios hasta que sean revisados:")
    for registro in cuarentena:
        if isinstance(registro, dict):
            print(f"- {registro.get("id_muestra", "sin id")}")
        else:
            print("- Registro sin formato válido")
    print(f"Revise y corrija el archivo {RUTA_DATOS}")