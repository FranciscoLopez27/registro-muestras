warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/README.md b/README.md[m
[1mindex 3cf14be..d134532 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -30,10 +30,13 @@[m [mPersonal del equipo de microbiología encargado de registrar las muestras que so[m
 - Registro del analista encargado del análisis.[m
 - Registro de resultado por análisis de muestra.[m
 - Definición de fecha límite para reporte.[m
[32m+[m[32m- Busqueda de muestras por ID.[m
[32m+[m[32m- Despliegue de análisis y resultados de muestra.[m
[32m+[m[32m- Listado de muestras fuera de norma.[m
 [m
 ## Reglas[m
 - Una muestra se encuentra fuera de norma cuando el resultado es superior al límite indicado por el cliente (generalmente el del RSA).[m
[31m-- Los resultados de análisis pueden ser Cualitativos o Cuantitativos.[m
[32m+[m[32m- Se consideran solo analisis Cuantitativos, es decir se ralizan conteos.[m
 - Una muestra puede estar en estado de enviada, confirmada por el laboratorio (entro a análisis) y liberada.[m
 - ID de cada muestra es único.[m
 - Los estados de las muestras solo pueden cambiar linealmente de enviada a confirmada a liberada.[m
[36m@@ -43,5 +46,6 @@[m [mPersonal del equipo de microbiología encargado de registrar las muestras que so[m
 ## Fuera del alcance (por ahora)[m
 - Agrupación de muestras por análisis y por día de análisis[m
 - Ingreso de usuarios diferenciado por cargo.[m
[31m-Generación de informe con los resultados para cliente[m
[32m+[m[32m- Generación de informe con los resultados para cliente[m
 - Generación de tiempo fin de reporte de forma automática en base a análisis.[m
[32m+[m[32m- Integrar análisis cualitativo para las muestras.[m
