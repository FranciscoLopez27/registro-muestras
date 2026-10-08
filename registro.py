from datetime import date
import copy

#Codigo de unidades de conteo
UNIDADES_VALIDAS = {"UFC/g", "UFC/ml", "UFC/swab", "NMP/g", "NMP/ml"}
UNIDADES_VALIDAS_MINUSCULAS = {unidad.lower() for unidad in UNIDADES_VALIDAS}

#Codigos de clientes registrados
CLIENTES_REGISTRADOS = {"0042", "1234", "5678"}

def es_cliente_valido(cliente):
    return len(cliente) == 4 and cliente.isdigit() and cliente in CLIENTES_REGISTRADOS 

def es_unidad_valida(unidad):
    return unidad.lower() in UNIDADES_VALIDAS_MINUSCULAS

def generar_id(numero):
    return f"M-{numero:04d}"

def validar_muestra(datos_muestra):
    cliente = datos_muestra["cliente"] 
    descripcion = datos_muestra["descripcion"]
    analisis = datos_muestra["analisis"]
    lista_errores = []

    if not descripcion.strip():
        lista_errores.append("La muestra necesita obligatoriamente una descripcion")

    if not cliente.isdigit():
        lista_errores.append("El codigo del cliente ingresado no es numerico")

    elif len(cliente) != 4:
        lista_errores.append("El codigo del cliente debe ser de 4 digitos")

    elif not cliente in CLIENTES_REGISTRADOS:
        lista_errores.append("El codigo del cliente no corresponde a un cliente registrado en la base de datos")

    if len(analisis) == 0:
        lista_errores.append("La muestras creadas deben tener asociado minimo un analisis para registrarse")
    
    for analisis_individual in analisis:

        if  not analisis_individual["nombre"].strip():
            lista_errores.append("Todos los analisis ingresados deben tener nombre")

        if analisis_individual["limite"] < 0:
            lista_errores.append("El limite de conteo ingresado debe ser mayor o igual a 0")

        if not es_unidad_valida(analisis_individual["unidad"]):
            lista_errores.append(f"La unidad de conteo del analisis {analisis_individual["nombre"]} ingresados no esta registrada")

    return lista_errores


def agregar_muestra(lista_muestras, datos_muestra):
    
    lista_errores = validar_muestra(datos_muestra)
    
    if not lista_errores:
        nueva_muestra = copy.deepcopy(datos_muestra)
        nueva_muestra.update({
            "id": generar_id(len(lista_muestras)+1),
            "estado": "enviada",
            "fecha_ingreso": date.today().isoformat()
        })
        lista_muestras.append(nueva_muestra)
        return (nueva_muestra["id"],lista_errores)
    
    return(None, lista_errores)
    

def listar_muestras(lista_muestras):
    if len(lista_muestras) == 0:
        print("No se encuentran muestras registradas en la base de datos")
    else:
        for muestra in lista_muestras:
            print(
                f"id: {muestra['id']} || cliente: {muestra['cliente']} || descripcion: {muestra['descripcion']} ||"
                f" estado: {muestra['estado']} || fecha: {muestra['fecha_ingreso']}"
                )
            for analisis in muestra["analisis"]:
                print(f"Nombre analisis: {analisis['nombre']} || Limite conteo: {analisis['limite']} || Unidad: {analisis['unidad']}")
            print("")
    return

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