from models import Analisis

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

