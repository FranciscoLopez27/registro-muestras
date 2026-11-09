def muestras_de_ejemplo():
    """Devuelve una lista de muestras de ejemplo para probar el programa."""
    return [
        {
            "id": "M-0001", "cliente": "0042", "descripcion": "Jugo de naranja lote 55",
            "estado": "enviada", "fecha_ingreso": "2026-10-27",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/ml", "limite": 10, "resultado": None, "fuera_especificacion": None},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/ml", "limite": 100, "resultado": None, "fuera_especificacion": None},
            ],
        },
        {
            "id": "M-0002", "cliente": "0044", "descripcion": "Carne molida lote 12",
            "estado": "confirmada", "fecha_ingreso": "2026-10-27",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 250, "fuera_especificacion": True},
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                "unidad": "UFC/ml", "limite": 50, "resultado": None, "fuera_especificacion": None},
            ],
        },
        {
            "id": "M-0003", "cliente": "0047", "descripcion": "Lechuga escarola",
            "estado": "liberada", "fecha_ingreso": "2026-10-26",
            "analisis": [
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 0, "fuera_especificacion": False},
            ],
        },
        {
            "id": "M-0004", "cliente": "0042", "descripcion": "Néctar de durazno",
            "estado": "cancelada", "fecha_ingreso": "2026-10-28",
            "analisis": [
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                "unidad": "UFC/ml", "limite": 10, "resultado": None, "fuera_especificacion": None},
            ],
        },
    ]

def muestras_de_ejemplo_ampliadas():
    """Devuelve más muestras de ejemplo, con varias fuera de especificación, para probar a mano."""
    return muestras_de_ejemplo() + [
        {
            "id": "M-0005", "cliente": "0047", "descripcion": "Queso fresco lote 7",
            "estado": "confirmada", "fecha_ingreso": "2026-11-02",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 80, "fuera_especificacion": False},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 1500, "fuera_especificacion": True},
            ],
        },
        {
            "id": "M-0006", "cliente": "0044", "descripcion": "Hamburguesa de vacuno lote 3",
            "estado": "liberada", "fecha_ingreso": "2026-10-30",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 400, "fuera_especificacion": True},
                {"codigo": "A013", "nombre": "Conteo Coliformes", "norma": "ISO 4832",
                "unidad": "UFC/ml", "limite": 50, "resultado": 120, "fuera_especificacion": True},
            ],
        },
        {
            "id": "M-0007", "cliente": "0042", "descripcion": "Yogur natural lote 21",
            "estado": "liberada", "fecha_ingreso": "2026-10-29",
            "analisis": [
                {"codigo": "A012", "nombre": "Conteo Enterobacterias", "norma": "ISO 21528-2",
                "unidad": "UFC/g", "limite": 100, "resultado": 30, "fuera_especificacion": False},
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 200, "fuera_especificacion": False},
            ],
        },
        {
            "id": "M-0008", "cliente": "0047", "descripcion": "Frutillas congeladas lote 9",
            "estado": "cancelada", "fecha_ingreso": "2026-11-01",
            "analisis": [
                {"codigo": "A019", "nombre": "Conteo Mohos y levaduras", "norma": "ISO 21527-2",
                "unidad": "UFC/g", "limite": 1000, "resultado": 5000, "fuera_especificacion": True},
            ],
        },
    ]