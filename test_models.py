from models import (Analisis, Muestra)
from datetime import date
from exceptions import (ErrorLaboratorio,ErrorEstado,ErrorNoEncontrado,ErrorValor,ErrorDuplicado)

def lanza(tipo_error, funcion, *argumentos):
    """Devuelve True si llamar a funcion(*argumentos) lanza un error del tipo indicado."""
    try:
        funcion(*argumentos)
    except tipo_error:
        return True
    return False

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
assert a.resultado is None
assert a.fuera_especificacion is None

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
a._registrar_resultado(200)
assert a.resultado == 200
assert a.fuera_especificacion is True

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
a._registrar_resultado(100)
assert a.resultado == 100
assert a.fuera_especificacion is False

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
a._registrar_resultado(0)
assert a.resultado == 0
assert a.fuera_especificacion is False

assert lanza(ErrorValor, a._registrar_resultado, -1)
assert a.resultado == 0
assert a.fuera_especificacion is False

a._registrar_resultado(200)
assert a.resultado == 200
assert a.fuera_especificacion is True
a._registrar_resultado(10)
assert a.resultado == 10
assert a.fuera_especificacion is False

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 0)
a._registrar_resultado(1)
assert a.resultado == 1
assert a.fuera_especificacion is True

print("Todas las pruebas de Analisis pasaron")

# ---------- Funciones auxiliares ----------
def nuevo_analisis(codigo="A012", limite=100):
    return Analisis(codigo, "Conteo de prueba", "ISO 0000", "UFC/g", limite)

def muestra_con_analisis(*codigos):
    m = Muestra("M-0001", "0042", "Leche entera lote 123")
    for codigo in codigos:
        m.agregar_analisis(nuevo_analisis(codigo))
    return m

# ---------- Creación ----------
m = Muestra("M-0001", "0042", "Leche entera lote 123")
assert m.estado == "enviada"
assert m.analisis == ()
assert m.fecha_ingreso == date.today().isoformat()

m_antigua = Muestra("M-0002", "0044", "Queso fresco", "2026-11-01")
assert m_antigua.fecha_ingreso == "2026-11-01"
print("Muestra (creación): pruebas pasaron")

# ---------- Análisis ----------
m = Muestra("M-0001", "0042", "Leche entera lote 123")
m.agregar_analisis(nuevo_analisis("A012"))
assert len(m.analisis) == 1
assert lanza(ErrorDuplicado, m.agregar_analisis, nuevo_analisis("A012"))
assert len(m.analisis) == 1                                    # no se agregó
m.agregar_analisis(nuevo_analisis("A013"))
assert len(m.analisis) == 2
assert isinstance(m.analisis, tuple)
print("Muestra (análisis): pruebas pasaron")

# ---------- Avanzar estado ----------
sin_analisis = Muestra("M-0003", "0047", "Lechuga escarola")
assert lanza(ErrorEstado, sin_analisis.avanzar_estado)
assert sin_analisis.estado == "enviada"

m = muestra_con_analisis("A012", "A013")
m.avanzar_estado()
assert m.estado == "confirmada"

m.registrar_resultado("A012",50)                    # un resultado pendiente
assert m.tiene_resultados_pendientes() is True
assert lanza(ErrorEstado,m.avanzar_estado)
assert m.estado == "confirmada"

m.registrar_resultado("A013",30)                    # todos con resultado
assert m.tiene_resultados_pendientes() is False
m.avanzar_estado()
assert m.estado == "liberada"
assert lanza(ErrorEstado, m.avanzar_estado)                   # ya está liberada
assert m.estado == "liberada"
print("Muestra (avanzar estado): pruebas pasaron")

# ---------- Cancelar ----------
enviada = muestra_con_analisis("A012")
enviada.cancelar()
assert enviada.estado == "cancelada"

confirmada = muestra_con_analisis("A012")
confirmada.avanzar_estado()
confirmada.cancelar()
assert confirmada.estado == "cancelada"

liberada = muestra_con_analisis("A012")
liberada.avanzar_estado()
liberada.registrar_resultado("A012",10)
liberada.avanzar_estado()
assert lanza(ErrorEstado, liberada.cancelar)
assert liberada.estado == "liberada"

assert lanza(ErrorEstado, enviada.cancelar)                 # ya está cancelada
assert lanza(ErrorEstado, enviada.avanzar_estado)           # y no puede avanzar
assert enviada.estado == "cancelada"
print("Muestra (cancelar): pruebas pasaron")

# ---------- Registrar resultados desde Muestras ----------

p = muestra_con_analisis("A012")
assert lanza(ErrorEstado, p.registrar_resultado, "A012", 200)
assert p.analisis[0].resultado is None
print("Muestra (registrar resultado en muestra enviada): pruebas pasaron")
p.avanzar_estado()
p.registrar_resultado("A012", 200)
assert p.analisis[0].resultado == 200
print("Muestra (registrar resultado): pruebas pasaron")

assert lanza(ErrorNoEncontrado, p.registrar_resultado, "A013", 100)
print("Muestra (registrar resultado en analisis que no esta en la muestra): pruebas pasaron")
assert lanza(ErrorValor, p.registrar_resultado, "A012", -10)
assert p.analisis[0].resultado == 200
print("Muestra (registrar valor negativo): pruebas pasaron")

p.registrar_resultado("A012",10)
assert p.analisis[0].resultado == 10
print("Muestra (modificar resultado): pruebas pasaron")

# ---------- Registrar resultado: muestras liberadas y canceladas ----------
liberada = muestra_con_analisis("A012")
liberada.avanzar_estado()                                  # confirmada
liberada.registrar_resultado("A012", 10)
liberada.avanzar_estado()                                  # liberada
assert liberada.estado == "liberada"
assert lanza(ErrorEstado, liberada.registrar_resultado, "A012", 99)# resultados bloqueados
assert liberada.analisis[0].resultado == 10                # conserva el anterior

cancelada = muestra_con_analisis("A012")
cancelada.avanzar_estado()                                 # confirmada
cancelada.registrar_resultado("A012", 20)
cancelada.cancelar()
assert cancelada.estado == "cancelada"
assert lanza(ErrorEstado, cancelada.registrar_resultado, "A012", 50)
assert cancelada.analisis[0].resultado == 20
print("Muestra (registrar en liberada y cancelada): pruebas pasaron")

# ---------- Registrar resultado: modificar un resultado y comprobar que cambia fuera de especificacion ----------
p = muestra_con_analisis("A012")
p.avanzar_estado()
p.registrar_resultado("A012", 200)
assert p.analisis[0].fuera_especificacion is True
p.registrar_resultado("A012", 10)
assert p.analisis[0].fuera_especificacion is False
print("Muestra (modificar resultado y actualizacion de especificación): pruebas pasaron")

# ---------- Agregar análisis: solo en muestras enviadas ----------
confirmada = muestra_con_analisis("A012")
confirmada.avanzar_estado()
assert confirmada.estado == "confirmada"
assert lanza(ErrorEstado, confirmada.agregar_analisis, nuevo_analisis("A013"))
assert len(confirmada.analisis) == 1                       # no se agregó
print("Muestra (agregar en confirmada): pruebas pasaron")