# Ruta de aprendizaje: de contador a contador que programa

Orden pensado para que cada etapa produzca algo usable en el trabajo, no solo ejercicios.
No pases a la siguiente hasta que hayas construido la entrega de la etapa anterior.

---

## Etapa 1 · Fundamentos de pandas (2–3 semanas)

**Material:** `01_kit_pandas_contable/` — 15 ejercicios con datos contables reales.

| Debes poder | Comprobación |
|---|---|
| Leer CSV y Excel con los tipos correctos | `dtype=str` en códigos PUC y NIT |
| Filtrar con condiciones compuestas | `(a) & (b)` con paréntesis |
| Limpiar texto, nulos y duplicados | `.str.strip()`, `.fillna()`, `.drop_duplicates()` |
| Agrupar y hacer tablas dinámicas | `groupby`, `pivot_table` |
| Cruzar dos archivos | `merge(..., how="outer", indicator=True)` |
| Exportar a Excel multi-hoja | `pd.ExcelWriter` |

**Entrega de la etapa:** tomar un archivo real de tu trabajo (un auxiliar, un reporte del
software contable) y producir un resumen en Excel que hoy hagas a mano.

---

## Etapa 2 · Automatizar una tarea propia (3–4 semanas)

**Material:** `02_plantillas/` y los proyectos de las carpetas 01 y 02 de este espacio.

Elige **una** tarea que hagas todos los meses y conviértela en script. Buenos candidatos,
en orden de dificultad:

1. Cruce de un reporte contra otro (dos archivos, un `merge`, una hoja de diferencias).
2. Cálculo de retenciones de un lote de facturas.
3. Conciliación bancaria del mes.
4. Informe mensual a gerencia.

Reglas que valen para todos: los parámetros van en un JSON aparte, nunca dentro del código;
el script no modifica el archivo original, escribe uno nuevo; y cada resultado se valida
contra algo que ya sabes que está bien.

**Entrega:** una tarea del cierre mensual que antes te tomaba horas y ahora es un comando.

---

## Etapa 3 · Estructura y calidad (4–6 semanas)

- Funciones con un solo propósito y nombre claro, en vez de un script largo.
- `argparse` para pasar rutas y parámetros desde la terminal.
- Manejo de errores: qué pasa si falta una columna o el archivo está abierto en Excel.
- Pruebas: un archivo pequeño con resultado conocido que confirme que el cálculo sigue bien.
- Git: versiona tus proyectos y súbelos a GitHub. Es tu portafolio verificable.

**Entrega:** un repositorio público con README, datos de ejemplo y un script que cualquiera
pueda correr.

---

## Etapa 4 · Análisis y visualización (4–6 semanas)

- Series de tiempo: tendencia, estacionalidad, variación mes a mes y año contra año.
- Segmentación: Pareto de clientes, proveedores, líneas de producto.
- Indicadores con lectura, no solo el número: qué decisión cambia si el indicador cambia.
- Gráficos con las reglas de `02_plantillas/plantilla_graficos.py`.

**Entrega:** un tablero mensual (Excel o HTML) que gerencia abra sin pedirte explicación.

---

## Etapa 5 · Producto (cuando las anteriores estén sólidas)

Aquí caben los proyectos que ya tienes en mente: software de inventarios con causación de
costos, aplicación de conciliación, calculadora tributaria publicada. Lo que cambia en esta
etapa es que dejas de escribir scripts para ti y empiezas a escribir software para otros:
interfaz, validación de entradas, manejo de errores, documentación e instalación.

---

## Qué NO hacer

- Estudiar sintaxis suelta sin un archivo real encima. La sintaxis se olvida; el problema resuelto no.
- Empezar por machine learning. El 95 % del valor que un contador saca de Python está en limpiar, cruzar y resumir datos.
- Copiar código sin ejecutarlo línea por línea. Si no puedes explicar qué hace cada línea, no es tuyo.
- Guardar todo en un solo archivo gigante. Una carpeta por proyecto, un archivo por responsabilidad.

## Ritmo realista

Entre 4 y 6 horas por semana sostenidas rinden más que un fin de semana intensivo cada mes.
La curva se siente lenta durante las primeras seis semanas y después se acelera de golpe,
cuando dejas de pelear con la sintaxis y empiezas a pensar en el problema.
