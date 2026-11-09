#Catalogos

CATALOGO_CLIENTES = {
    "0042": {"nombre": "FrutasNorte S.A."},
    "0044": {"nombre": "CarnesSur S.A."},
    "0047": {"nombre": "VerdurasCentro S.A."},
}

CATALOGO_ANALISIS = {
    "A012": {"nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2", "unidades": ["UFC/g", "UFC/ml"]},
    "A013": {"nombre": "Conteo Coliformes", "norma": "ISO 4832", "unidades": ["UFC/ml"]},
    "A019": {"nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2", "unidades": ["UFC/g", "UFC/ml"]},
}

ESTADOS_POSIBLES = ("enviada","confirmada","liberada")

ESTADOS_CANCELABLES = ("enviada", "confirmada")

ESTADOS_EN_ORDEN = ESTADOS_POSIBLES + ("cancelada",)