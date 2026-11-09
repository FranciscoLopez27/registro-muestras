# Organización del código en módulos

## Objetivo
El archivo `registro.py` creció hasta contener funciones con responsabilidades
muy distintas: datos fijos, reglas del laboratorio, interacción con el usuario,
presentación y menú. Separarlas en módulos permite encontrar cada cosa más rápido,
modificar una parte sin afectar a las demás, y probar las reglas del laboratorio
de forma independiente.

## Criterio de separación
Cada módulo agrupa funciones con una misma responsabilidad. La pregunta principal
para decidir dónde va una función es si usa `input`, `print` o ninguno de los dos,
considerando también las funciones que llama.

## Módulos

| Archivo | Responsabilidad | Contenido |
|---|---|---|
| `constants.py` | Datos fijos del laboratorio | CATALOGO_CLIENTES, CATALOGO_ANALISIS, ESTADOS_POSIBLES, ESTADOS_CANCELABLES, ESTADOS_EN_ORDEN |
| `lab_rules.py` | Reglas del laboratorio, sin `input` ni `print` | generar_id, validar_muestra, agregar_muestra, normalizar_codigo, unidad_desde_opcion, codigo_ya_agregado, buscar_muestra, siguiente_estado, tiene_resultado_pendiente, avanzar_estado, cancelar_muestra, esta_fuera_de_especificacion, registrar_resultado, muestras_fuera_norma, agrupar_por_estado |
| `inputs.py` | Pedir datos al usuario | pedir_entero, pedir_muestra_existente, elegir_codigo, elegir_unidad, pedir_analisis_catalogo, pedir_analisis, pedir_datos_muestra |
| `formatters.py` | Mostrar información en pantalla | TEXTOS_EN_BASE_A_RESULTADOS, listar_muestras, mostrar_errores, mostrar_menu, pausar |
| `controllers.py` | Coordinar cada opción del menú | opcion_agregar_muestra, opcion_listar_muestras, opcion_buscar_muestra, opcion_cambiar_estado, opcion_registrar_resultado, opcion_listar_fuera_de_norma |
| `sample_data.py` | Muestras de ejemplo para pruebas | muestras_de_ejemplo, muestras_de_ejemplo_ampliadas |
| `main.py` | Punto de entrada del programa | main |

## Decisiones sobre casos dudosos
- `TEXTOS_EN_BASE_A_RESULTADOS` va en `formatters.py` y no en `constants.py`,
  porque define cómo se muestra la información y no una regla del laboratorio.
- `normalizar_codigo` y `unidad_desde_opcion` van en `lab_rules.py` porque no usan
  `input` y tienen pruebas automáticas, aunque su propósito es interpretar lo que
  escribe el usuario.
- `pausar` va en `formatters.py`: usa `input`, pero no pide un dato, solo detiene
  la pantalla para que el usuario lea.
- Las muestras de ejemplo van en un archivo propio porque no son parte del
  sistema real; solo se usan para probar.

## Regla de dependencias
Cada módulo solo puede importar de los módulos que están más abajo en esta lista:

1. El punto de entrada importa de `controllers`.
2. `controllers` importa de `inputs`, `formatters`, `lab_rules` y `constants`.
3. `inputs` importa de `formatters`, `lab_rules` y `constants`.
4. `formatters` importa de `constants`.
5. `lab_rules` importa solo de `constants`.
6. `constants` no importa de ningún módulo del proyecto.

Las reglas del laboratorio nunca dependen de la interacción ni de la presentación.
Así se evitan importes circulares, y las reglas pueden reutilizarse aunque cambie
la forma de interactuar con el usuario, por ejemplo con una interfaz web.

## Idioma
Los nombres de los archivos están en inglés, siguiendo una convención común en la
industria, mientras que las funciones y variables se mantienen en español.