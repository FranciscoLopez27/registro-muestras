# Pseudocodigo del registro de muestras

## Agregar muestras (version 1)
'''
Algoritmo: Agregar_muestra

Entrada: Nombre muestra, descripción muestra, análisis para la muestra en formato de lista, límite de conteo, unidades de resultados, número de cliente.

Salida: ID de la muestra, o mensaje de error en caso de que alguno o algunos datos de entrada no sean válidos.

ID_indice_global←0

lista_unidades←[UFC/g, UFC/ml, UFC/swab, NMP/g, NMP/ml]

SI nombre_muestra este vacío ENTONCES:

	DEVOLVER “ERROR: La muestra necesita tener un nombre valido no vacío”

FIN SI

SI unidades no está EN lista_unidades ENTONCES:

	DEVOLVER “ERROR: La unidad de medida debe ser válida”

FIN SI

SI longitud (código_cliente) ≠ 4 0 codigo_cliente no solo tiene digito 

ENTONCES:

	DEVOLVER “Error: El código debe ser válido en formato de 4 dígitos”

FIN SI

SI limite<0 ENTONCES:

	DEVOLVER: “Error: El limite deber ser positivo”

FIN SI

SI largo (análisis) ==0 ENTONCES:

	DEVOLVER “Error: La muestra necesita mínimo un análisis”

FIN SI

muestra_nueva←Nueva muestra con

	id←ID_indice_global
	cliente←codigo_cliente
	descripcion←descripcion_muestra
	analisis←lista_analisis
	limite←limite_conteo
	unidades←unidades_resultado
	estado←"SENT"
	fecha_ingreso←fecha_actual

ID_indice_global←ID_indice_global+1

AGREGAR muestra_nueva A lista_muestras

DEVOLVER muestra_nueva.ID

'''

## Lista_muestras (version 1)
 
Algoritmo: listar_muestras

Entrada: Lista de muestras registradas en la base de datos.

Salida: ninguna (muestra en pantalla listado de muestras o un aviso si no hay muestras ingresadas)

SI largo(lista_muestras)==0 ENTONCES:

	MOSTRAR "No se encuentran muestras registradas en la base de datos"

SINO:

	PARA CADA muestra EN lista_muestras HACER:

		MOSTRAR muestra.id || muestra.cliente || muestra.estado || muestra.fecha_ingreso

		PARA CADA analisis EN muestra.analisis HACER:

			MOSTRAR analisis.nombre_analisis || analisis.limite_conteo || analsis.unidades_analisis

		FIN PARA

	FIN PARA

FIN SI
