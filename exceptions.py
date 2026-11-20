class ErrorLaboratorio(Exception):
    """Error general de las reglas del laboratorio."""

class ErrorEstado(ErrorLaboratorio):
    """La operación no está permitida en el estado actual de la muestra."""

class ErrorValor(ErrorLaboratorio):
    """Un dato no cumple las reglas del laboratorio."""

class ErrorNoEncontrado(ErrorLaboratorio):
    """Se buscó un dato que no existe, por ejemplo un análisis que no está en la muestra."""

class ErrorDuplicado(ErrorLaboratorio):
    """Un dato no puede estar duplicado para esta operación"""
