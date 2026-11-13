from datetime import date
from constants import (ESTADOS_POSIBLES, ESTADOS_CANCELABLES)

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

    def _siguiente_estado(self):
        if self._estado not in ESTADOS_POSIBLES:
            return None
        indice = ESTADOS_POSIBLES.index(self._estado)
        if indice == len(ESTADOS_POSIBLES)-1:
            return None
        return ESTADOS_POSIBLES[indice + 1]

    def tiene_resultados_pendientes(self):
        return any(analisis.resultado is None for analisis in self._analisis)

    
    def avanzar_estado(self):
        lista_errores = []
        estado_actual = self._estado
        nuevo_estado = self._siguiente_estado()
        if nuevo_estado is None:
            lista_errores.append(f"El estado actual de la muestra se encuentra {estado_actual}, por lo que no se puede modificar")
            return lista_errores
        if len(self._analisis) == 0:
            lista_errores.append(f"La actual muestra no tiene ningun analisis asociado por lo que no se puede modificar su estado de {self._estado}")
            return lista_errores
        if nuevo_estado == "liberada" and self.tiene_resultados_pendientes():
            lista_errores.append("No todos los analisis tienen resultado, por lo que no puede ser liberada")
        if len(lista_errores) == 0:
            self._estado = nuevo_estado
        return lista_errores

    def cancelar(self):
        lista_errores = []
        if self._estado not in ESTADOS_CANCELABLES:
            lista_errores.append(f"La muestra no puede ser cancelada ya que se encuentra en estado: {self._estado}")
        if len(lista_errores) == 0:
            self._estado = "cancelada"
        return lista_errores
