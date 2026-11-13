from datetime import date

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

class Muestra:
    def __init__(self, id_muestra, cliente, descripcion, fecha_ingreso=None):
        self.id_muestra = id_muestra
        self.cliente = cliente
        self.descripcion = descripcion
        if fecha_ingreso is None:
            fecha_ingreso = date.today().isoformat()
        self.fecha_ingreso = fecha_ingreso
        self._estado = "enviada"
        self._analisis = []

    @property
    def estado(self):
        return self._estado
    
    @property
    def analisis(self):
        return tuple(self._analisis)

    def agregar_analisis(self, analisis):
        lista_errores = []
        if any(analisis.codigo == analisis_registrado.codigo for analisis_registrado in self._analisis):
            lista_errores.append("No pueden haber analisis repetidos para una muestra")
            return lista_errores
        self._analisis.append(analisis)
        return lista_errores
