class ErrorLaboratorio(Exception):
    """Error general de las reglas del laboratorio."""

class ErrorEstado(ErrorLaboratorio):
    """La operación no está permitida en el estado actual de la muestra."""

class ErrorValor(ErrorLaboratorio):
    """Un dato no cumple las reglas del laboratorio."""

class ErrorNoEncontrado(ErrorLaboratorio):
    """Un dato no se encontro dentro del sistema de almacenamiento que se esta buscando"""