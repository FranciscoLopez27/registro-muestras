class Analisis:
    """Un análisis solicitado para una muestra, con una copia de los datos
    vigentes del catálogo al momento del registro."""

    def __init__(self, codigo, nombre, norma, unidad, limite):
        """Crea el análisis sin resultado.

        codigo, nombre y norma: datos del método, copiados del catálogo.
        unidad: unidad elegida entre las permitidas para el método.
        limite: límite de conteo definido por el cliente (mayor o igual a 0).
        """
        self.codigo = codigo
        self.nombre = nombre
        self.norma = norma
        self.unidad = unidad        
        self.limite = limite
        self._resultado = None

    @property
    def resultado(self):
        """El resultado registrado, o None si todavía no hay resultado.
        Solo se modifica mediante registrar_resultado."""
        return self._resultado

    @property
    def fuera_especificacion(self):
        """Indica si el resultado supera el límite. Se calcula en cada consulta.

        None: todavía no hay resultado.
        True: el resultado supera el límite.
        False: el resultado es menor o igual al límite.
        """
        if self._resultado is None:
            return None
        return self._resultado > self.limite

    def registrar_resultado(self, valor):
        """Registra o corrige el resultado del análisis.

        Devuelve una lista de errores, vacía si el resultado se registró.
        Si hay errores, el resultado anterior se conserva.
        """
        lista_errores = []
        if valor < 0:
            lista_errores.append("El resultado tiene que ser un valor mayor o igual a 0")
        if len(lista_errores) != 0:
            return lista_errores
        self._resultado = valor
        return lista_errores
