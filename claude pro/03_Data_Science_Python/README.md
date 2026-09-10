# 03 · Data Science y Python

Donde aprendes y donde guardas las piezas reutilizables.

| Carpeta | Qué contiene |
|---|---|
| `01_kit_pandas_contable/` | 15 ejercicios progresivos + soluciones, con datos contables simulados (auxiliar, balance, facturas, extracto). Empieza por `01_ejercicios.ipynb`. |
| `02_plantillas/` | Dos plantillas que se copian y se adaptan: análisis y gráficos. |
| `03_ruta_aprendizaje.md` | Las cinco etapas, con la entrega esperada en cada una. |

---

## 02_plantillas/plantilla_analisis_contable.py

Caja de herramientas para atacar cualquier archivo nuevo. Funciona como script o como
módulo importable:

```bash
python plantilla_analisis_contable.py archivo.csv --columna-valor debito
```

```python
from plantilla_analisis_contable import cargar, diagnostico, resumen_por, edades, pareto

df = cargar("cartera.xlsx")
diagnostico(df)                                  # tipos, nulos, duplicados, ejemplo por columna
edades(df, "fecha_factura", "saldo")             # cartera por edades: 0-30, 31-60, 61-90, +90
pareto(df, "cliente", "saldo")                   # los clientes que explican el 80% del saldo
```

Trae resuelto lo que siempre estorba: normalización de nombres de columna (tildes, espacios,
mayúsculas), conversión de importes en texto con separadores colombianos (`"1.234.567,89"`),
y detección automática del formato de fecha para no confundir día con mes.

## 02_plantillas/plantilla_graficos.py

```bash
python plantilla_graficos.py ../01_kit_pandas_contable/datos/libro_auxiliar.csv
```

Cuatro gráficos listos para pegar en Word o PowerPoint, con reglas de diseño aplicadas:

- **Un solo eje Y.** Nunca dos escalas en un gráfico: si comparas magnitudes distintas, son dos gráficos. Es el error más común en informes financieros.
- **Paleta fija y validada** para daltonismo y contraste; los colores se asignan en orden y no se reciclan.
- Rótulos directos en vez de leyenda cuando hay pocas series; rejilla tenue; sin efectos 3D ni tortas.
- Categorías ordenadas por magnitud, nunca alfabéticamente.

Requiere `pip install matplotlib`.
