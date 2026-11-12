class Analisis:
    def __init__(self, codigo, nombre, norma, unidad, limite):
        self.codigo = codigo
        self.nombre = nombre
        self.unidad = unidad
        self.norma = norma
        self.limite = limite
        self._resultado = None

    @property
    def resultado(self):
        return self._resultado

    @property
    def fuera_especificacion(self):
        if self._resultado is None:
            return None
        return self._resultado > self.limite

    def registrar_resultado(self, valor):
        lista_errores = []
        if valor < 0:
            lista_errores.append("El resultado tiene que ser un valor mayor o igual a 0")
        if len(lista_errores) != 0:
            return lista_errores
        self._resultado = valor
        return lista_errores
