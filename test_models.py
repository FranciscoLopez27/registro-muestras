from models import (Analisis, Muestra)
from datetime import date

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
assert a.resultado is None
assert a.fuera_especificacion is None

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
a.registrar_resultado(200)
assert a.resultado == 200
assert a.fuera_especificacion is True

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
a.registrar_resultado(100)
assert a.resultado == 100
assert a.fuera_especificacion is False

a = Analisis("A012","Conteo Enterobacterias", "ISO 21528-2", "UFC/g", 100)
a.registrar_resultado(0)
assert a.resultado == 0
assert a.fuera_especificacion is False

a.registrar_resultado(-1)
assert a.resultado == 0
assert len(a.registrar_resultado(-1)) != 0
assert a.fuera_especificacion is False

a.registrar_resultado(200)
assert a.resultado == 200
assert a.fuera_especificacion is True
a.registrar_resultado(10)
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

m.analisis[0].registrar_resultado(50)                    # un resultado pendiente
assert m.tiene_resultados_pendientes() is True
assert len(m.avanzar_estado()) == 1
assert m.estado == "confirmada"

m.analisis[1].registrar_resultado(30)                    # todos con resultado
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
liberada.analisis[0].registrar_resultado(10)
liberada.avanzar_estado()
assert len(liberada.cancelar()) == 1
assert liberada.estado == "liberada"

assert len(enviada.cancelar()) == 1                      # ya está cancelada
assert len(enviada.avanzar_estado()) == 1                # y no puede avanzar
assert enviada.estado == "cancelada"
print("Muestra (cancelar): pruebas pasaron")


