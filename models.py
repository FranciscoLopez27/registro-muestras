from datetime import date
from constants import (ESTADOS_POSIBLES, ESTADOS_CANCELABLES)
from exceptions import (ErrorEstado, ErrorLaboratorio, ErrorValor, ErrorNoEncontrado)

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

    def _registrar_resultado(self, valor):
        """Uso interno: registra o corrige el resultado del análisis.

        Los resultados se registran mediante Muestra.registrar_resultado,
        que verifica que la muestra esté confirmada antes de llamar a este
        método. Por eso no debe llamarse directamente desde fuera de models.py.

        Lanza ErrorValor si el valor es negativo; en ese caso, el resultado
        anterior se conserva.
        """
        if valor < 0:
            raise ErrorValor("El resultado tiene que ser un valor mayor o igual a 0")
        self._resultado = valor
        

class Muestra:
    """Una muestra ingresada al laboratorio, con sus análisis y su estado.

    El estado y los análisis están protegidos: solo cambian mediante los
    métodos de la clase, que aplican las reglas del laboratorio.
    """
    def __init__(self, id_muestra, cliente, descripcion, fecha_ingreso=None):
        """Crea la muestra en estado "enviada" y sin análisis.

        fecha_ingreso: fecha en formato AAAA-MM-DD. Si no se indica, se usa
        la fecha de hoy (por ejemplo, al cargar muestras ya registradas se
        indica su fecha original).
        """
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
        """Estado actual de la muestra. Solo cambia con avanzar_estado o cancelar."""
        return self._estado
    
    @property
    def analisis(self):
        """Los análisis de la muestra, como tupla de solo lectura.
        Para agregar análisis se usa agregar_analisis."""
        return tuple(self._analisis)

    def agregar_analisis(self, analisis):
        """Agrega un análisis a la muestra.

        Devuelve una lista de errores, vacía si se agregó.
        No se permiten dos análisis con el mismo código.
        No se puede agregar un análisis nuevo si no esta en estado enviada.
        """
        lista_errores = []
        if self._estado != "enviada":
            lista_errores.append(f"La muestra esta en estado {self._estado}, solo en estado enviada se puede agregar analisis")
            return lista_errores
        if any(analisis.codigo == analisis_registrado.codigo for analisis_registrado in self._analisis):
            lista_errores.append("No pueden haber analisis repetidos para una muestra")
            return lista_errores
        self._analisis.append(analisis)
        return lista_errores

    def _siguiente_estado(self):
        """Uso interno: el estado que sigue al actual en el flujo del
        laboratorio, o None si no hay uno siguiente."""
        if self._estado not in ESTADOS_POSIBLES:
            return None
        indice = ESTADOS_POSIBLES.index(self._estado)
        if indice == len(ESTADOS_POSIBLES)-1:
            return None
        return ESTADOS_POSIBLES[indice + 1]

    def tiene_resultados_pendientes(self):
        """True si algún análisis de la muestra todavía no tiene resultado."""
        return any(analisis.resultado is None for analisis in self._analisis)

    
    def avanzar_estado(self):
        """Avanza la muestra al siguiente estado: enviada, confirmada, liberada.

        Devuelve una lista de errores, vacía si el estado cambió.
        No avanza si la muestra no tiene análisis, si ya está en el último
        estado o cancelada, ni se libera si hay resultados pendientes.
        """
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
        """Cancela la muestra, solo si está enviada o confirmada.

        Devuelve una lista de errores, vacía si se canceló.
        La cancelación no se puede deshacer.
        """
        lista_errores = []
        if self._estado not in ESTADOS_CANCELABLES:
            lista_errores.append(f"La muestra no puede ser cancelada ya que se encuentra en estado: {self._estado}")
        if len(lista_errores) == 0:
            self._estado = "cancelada"
        return lista_errores

    def registrar_resultado(self, codigo_analisis, resultado):
        """Registra o corrige el resultado de uno de los análisis de la muestra.

        Solo es posible mientras la muestra está confirmada. Lanza:
        - ErrorEstado: si la muestra no está confirmada.
        - ErrorNoEncontrado: si la muestra no tiene un análisis con ese código.
        - ErrorValor: si el resultado no es válido (por ejemplo, negativo).
        Este error lo lanza el propio análisis y llega sin cambios.

        Si se lanza cualquiera de estos errores, ningún resultado se modifica.
        """
        if self._estado != "confirmada":
            raise ErrorEstado("La muestra debe estar en estado confirmada para asociarle resultados")
        analisis_buscado = next((analisis for analisis in self._analisis if codigo_analisis == analisis.codigo), None)
        if analisis_buscado is None:
            raise ErrorNoEncontrado(f"La muestra ingresada no tiene el analisis {codigo_analisis} registrado")
        analisis_buscado._registrar_resultado(resultado)
        


