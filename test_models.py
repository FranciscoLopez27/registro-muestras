from models import (Analisis, Muestra)
from datetime import date

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

a._registrar_resultado(-1)
assert a.resultado == 0
assert len(a._registrar_resultado(-1)) != 0
assert a.fuera_especificacion is False

a._registrar_resultado(200)
assert a.resultado == 200
assert a.fuera_especificacion is True
a._registrar_resultado(10)
assert a.resultado == 10
assert a.fuera_especificacion is False

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
assert m.agregar_analisis(nuevo_analisis("A012")) == []
assert len(m.analisis) == 1
assert len(m.agregar_analisis(nuevo_analisis("A012"))) == 1   # código repetido
assert len(m.analisis) == 1                                    # no se agregó
assert m.agregar_analisis(nuevo_analisis("A013")) == []
assert len(m.analisis) == 2
assert isinstance(m.analisis, tuple)
print("Muestra (análisis): pruebas pasaron")

# ---------- Avanzar estado ----------
sin_analisis = Muestra("M-0003", "0047", "Lechuga escarola")
assert len(sin_analisis.avanzar_estado()) == 1
assert sin_analisis.estado == "enviada"

m = muestra_con_analisis("A012", "A013")
assert m.avanzar_estado() == []
assert m.estado == "confirmada"

m.registrar_resultado("A012",50)                    # un resultado pendiente
assert m.tiene_resultados_pendientes() is True
assert len(m.avanzar_estado()) == 1
assert m.estado == "confirmada"

m.registrar_resultado("A013",30)                    # todos con resultado
assert m.tiene_resultados_pendientes() is False
assert m.avanzar_estado() == []
assert m.estado == "liberada"

assert len(m.avanzar_estado()) == 1                      # ya está liberada
assert m.estado == "liberada"
print("Muestra (avanzar estado): pruebas pasaron")

# ---------- Cancelar ----------
enviada = muestra_con_analisis("A012")
assert enviada.cancelar() == []
assert enviada.estado == "cancelada"

confirmada = muestra_con_analisis("A012")
confirmada.avanzar_estado()
assert confirmada.cancelar() == []
assert confirmada.estado == "cancelada"

liberada = muestra_con_analisis("A012")
liberada.avanzar_estado()
liberada.registrar_resultado("A012",10)
liberada.avanzar_estado()
assert len(liberada.cancelar()) == 1
assert liberada.estado == "liberada"

assert len(enviada.cancelar()) == 1                      # ya está cancelada
assert len(enviada.avanzar_estado()) == 1                # y no puede avanzar
assert enviada.estado == "cancelada"
print("Muestra (cancelar): pruebas pasaron")

# ---------- Registrar resultados desde Muestras ----------

p = muestra_con_analisis("A012")
assert len(p.registrar_resultado("A012",200)) == 1
assert p.analisis[0].resultado is None
print("Muestra (registrar resultado en muestra enviada): pruebas pasaron")
p.avanzar_estado()
assert len(p.registrar_resultado("A012",200)) == 0
assert p.analisis[0].resultado == 200
print("Muestra (registrar resultado): pruebas pasaron")

assert len(p.registrar_resultado("A013", 100)) == 1
print("Muestra (registrar resultado en analisis que no esta en la muestra): pruebas pasaron")
assert len(p.registrar_resultado("A012", -10)) == 1
assert p.analisis[0].resultado == 200
print("Muestra (registrar valor negativo): pruebas pasaron")

assert len(p.registrar_resultado("A012",10)) == 0
assert p.analisis[0].resultado == 10
print("Muestra (modificar resultado): pruebas pasaron")

# ---------- Registrar resultado: muestras liberadas y canceladas ----------
liberada = muestra_con_analisis("A012")
liberada.avanzar_estado()                                  # confirmada
liberada.registrar_resultado("A012", 10)
liberada.avanzar_estado()                                  # liberada
assert liberada.estado == "liberada"
assert len(liberada.registrar_resultado("A012", 99)) == 1  # resultados bloqueados
assert liberada.analisis[0].resultado == 10                # conserva el anterior

cancelada = muestra_con_analisis("A012")
cancelada.avanzar_estado()                                 # confirmada
cancelada.registrar_resultado("A012", 20)
cancelada.cancelar()
assert cancelada.estado == "cancelada"
assert len(cancelada.registrar_resultado("A012", 50)) == 1
assert cancelada.analisis[0].resultado == 20
print("Muestra (registrar en liberada y cancelada): pruebas pasaron")

# ---------- Agregar análisis: solo en muestras enviadas ----------
confirmada = muestra_con_analisis("A012")
confirmada.avanzar_estado()
assert confirmada.estado == "confirmada"
assert len(confirmada.agregar_analisis(nuevo_analisis("A013"))) == 1
assert len(confirmada.analisis) == 1                       # no se agregó
print("Muestra (agregar en confirmada): pruebas pasaron")