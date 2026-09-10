# Pandas para contadores — kit de práctica

Ejercicios de `pandas` sobre datos contables colombianos simulados
(**COMERCIALIZADORA ANDINA S.A.S.**, enero–marzo 2026).

## Contenido

```
pandas_contable/
├── 01_ejercicios.ipynb      <- empieza aquí (celdas con TODO para que escribas tú)
├── 02_soluciones.ipynb      <- soluciones comentadas
├── generar_datos.py         <- script que creó los datos (puedes regenerarlos)
├── datos/
│   ├── libro_auxiliar.csv        1.268 movimientos con partida doble
│   ├── balance_prueba.csv        30 cuentas del PUC con saldo inicial, movimientos y final
│   ├── facturas_proveedores.csv  41 facturas con retefuente y reteICA (a propósito, sucias)
│   └── extracto_bancario.csv     149 movimientos del banco para conciliar
└── salidas/                 <- aquí queda el Excel del ejercicio 15
```

## Instalación en VS Code (una sola vez)

1. Instala **Python 3.11+** desde python.org (marca *Add Python to PATH*).
2. En VS Code instala las extensiones **Python** y **Jupyter** (de Microsoft).
3. Abre una terminal en VS Code (``Ctrl + ` ``) y ejecuta:

```bash
pip install pandas openpyxl jupyter
```

4. **Abre la carpeta**, no el archivo suelto: *Archivo → Abrir carpeta →* `pandas_contable`.
   Si abres solo el `.ipynb`, las rutas `datos/...` no se encuentran y te sale `FileNotFoundError`.
5. Abre `01_ejercicios.ipynb`, arriba a la derecha haz clic en **Select Kernel → Python 3**,
   y ejecuta la primera celda con `Shift + Enter`.

### Si prefieres Google Colab

Sube la carpeta `datos/` a tu Drive, abre el `.ipynb` en Colab y cambia la primera línea a:

```python
from google.colab import drive; drive.mount('/content/drive')
RUTA = "/content/drive/MyDrive/pandas_contable/datos/"
```

## Ruta sugerida (unas 6 horas en total)

| Sesión | Ejercicios | Qué aprendes |
|---|---|---|
| 1 | 1 – 3 | leer archivos, tipos de datos, validar partida doble |
| 2 | 4 – 5 | selección de columnas y filtros compuestos |
| 3 | 6 – 7 | limpieza de datos y recálculo de retenciones |
| 4 | 8 – 10 | `groupby` y `pivot_table` (la tabla dinámica de Python) |
| 5 | 11 – 13 | `merge`, ecuación contable y estado de resultados |
| 6 | 14 – 15 | conciliación bancaria y exportación a Excel |

Al final del cuaderno hay cinco retos adicionales (cartera por edades, certificados de
retención, exógena formato 1001, indicadores financieros y gráficos) y una chuleta de pandas.

## Regla de estudio

Escribe el código tú mismo antes de mirar `02_soluciones.ipynb`. Copiar y pegar
se siente productivo y no deja nada; equivocarse con un `KeyError` sí.
